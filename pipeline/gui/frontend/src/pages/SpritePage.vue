<template>
    <div class="sprite-page">

      <!-- LEFT COLUMN -->
      <div class="left-column">

        <!-- TABS -->
        <div class="tabs">
          <button
            class="tab"
            :class="{ active: activeTab === 'motion' }"
            @click="activeTab = 'motion'"
          >
            Motion Sources
          </button>

          <button
            class="tab"
            :class="{ active: activeTab === 'presets' }"
            @click="activeTab = 'presets'"
          >
            Presets
          </button>
        </div>

        <!-- TAB CONTENT -->
        <div class="tab-content">
          <MotionSourcePanel
            v-if="activeTab === 'motion'"
            :motions="motions"
            :selectedMotion="selectedMotion"
            @select-motion="selectMotion"
            @import-motion="importMotion"
          />

          <SpritePresetPanel
            v-else
            @update:name="updatePresetName"
            @update:prompt="applyPresetPrompt"
            @update:settings="applyPresetSettings"
            @update:style="applyPresetStyle"
          />
        </div>

      </div>

      <!-- CENTER COLUMN -->
      <RenderSettingsPanel
        :selectedMotion="selectedMotion"
        :spriteStyles="spriteStyles"
        :selectedStyle="selectedStyle"
        :models="models"
        :settings="settings"
        :referenceImages="referenceImages"
        :stride="stride"
        :prompt="prompt"
        :refinedPrompt="refinedPrompt"

        @update-settings="updateSettings"
        @select-style="selectStyle"
        @add-reference="addReference"
        @remove-reference="removeReference"
        @update-prompt="updatePrompt"
        @refine-prompt="refinePrompt"
        @update-stride="updateStride"
        @generate="runGeneration"
      />

      <!-- RIGHT COLUMN -->
      <SpriteOutputPanel
        :frames="frames"
        :sheet="sheet"
        :history="history"
        :generating="generating"
        @select-history="loadHistory"
      />

    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

import MotionSourcePanel from '../components/MotionSourcePanel.vue'
import RenderSettingsPanel from '../components/RenderSettingsPanel.vue'
import SpriteOutputPanel from '../components/SpriteOutputPanel.vue'
import SpritePresetPanel from '../components/SpritePresetPanel.vue'

import { useProjectsStore } from '../stores/projects'
import { useMotionStore } from '../stores/motion'
import { useSpritesStore } from '../stores/sprites'
import { useModelsStore } from '../stores/models'
import { useSpriteStylesStore } from '../stores/spriteStyles'
import { useSpritePresetsStore } from '../stores/spritePresets'

import { uploadReference, describeReferences } from '../api/reference'

/* STORES */
const projects = useProjectsStore()
const motionStore = useMotionStore()
const spritesStore = useSpritesStore()
const modelsStore = useModelsStore()
const spriteStylesStore = useSpriteStylesStore()
const spritePresetsStore = useSpritePresetsStore()

/* UI STATE */
const activeTab = ref('motion') // "motion" or "presets"

/* LOCAL STATE */
const selectedMotion = ref(null)
const selectedStyle = ref(null)

const prompt = ref("")
const refinedPrompt = ref("")

const referenceImages = ref([])

const stride = ref(1)

const settings = ref({
  resolution: 512,
  variants: 1,
  seed: null,
  background: 'transparent',
  render_model: null,
})

/* DERIVED DATA */
const motions = motionStore.motions
const models = modelsStore.models
const spriteStyles = spriteStylesStore.spriteStyles

const frames = spritesStore.frames
const sheet = spritesStore.sheet
const history = spritesStore.history
const generating = spritesStore.generating

/* ACTIONS */
function selectMotion(motion) {
  selectedMotion.value = motion
}

function importMotion(file) {
  motionStore.importMotion(file)
}

function selectStyle(style) {
  selectedStyle.value = style
}

function updateSettings(newSettings) {
  settings.value = { ...settings.value, ...newSettings }
}

function updatePrompt(text) {
  prompt.value = text
}

/* PRESET APPLICATION */
function updatePresetName(name) {
  spritePresetsStore.updateName(name)
}

function applyPresetPrompt(text) {
  prompt.value = text
}

function applyPresetSettings(newSettings) {
  settings.value = { ...newSettings }
}

function applyPresetStyle(style) {
  selectedStyle.value = style
}

/* REFERENCE IMAGE HANDLING */
async function addReference(fileObj) {
  const project_id = projects.activeProjectId

  const uploadRes = await uploadReference(project_id, fileObj.file)
  const serverPath = uploadRes.reference.serverPath

  const descRes = await describeReferences([serverPath])
  const description = descRes.descriptions?.[0] || {}

  referenceImages.value.push({
    ...fileObj,
    serverPath,
    description,
  })
}

function removeReference(index) {
  referenceImages.value.splice(index, 1)
}

/* STRIDE */
function updateStride(value) {
  stride.value = value
}

/* PROMPT REFINEMENT */
async function refinePrompt() {
  const paths = referenceImages.value.map(r => r.serverPath)
  const descriptions = referenceImages.value.map(r => r.description)

  const res = await fetch('/api/ai/sprite/refine', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: prompt.value,
      existing_prompt: {},
      reference_descriptions: descriptions,
    })
  })

  const data = await res.json()
  refinedPrompt.value = data.sprite_prompt || data.refined_prompt || ""
}

/* GENERATION */
async function runGeneration() {
  if (!selectedMotion.value) return

  const payload = {
    project_id: projects.activeProjectId,
    motion: selectedMotion.value,
    prompt: prompt.value,
    refined_prompt: refinedPrompt.value,
    reference_images: referenceImages.value.map(r => r.serverPath),
    reference_descriptions: referenceImages.value.map(r => r.description),
    stride: stride.value,
    settings: settings.value,
    style: selectedStyle.value,
  }

  await spritesStore.generate(payload)
}

function loadHistory(entry) {
  spritesStore.loadHistory(entry)
}

/* INITIAL LOAD */
onMounted(async () => {
  projects.ensureLoaded()
  spriteStylesStore.ensureLoaded()
  modelsStore.loadModels()
  spritesStore.reset()
})
</script>

<style scoped>
.sprite-page {
  display: grid;
  grid-template-columns: 280px 1fr 380px;
  gap: 20px;
  height: 100%;
  padding: 20px;
}

/* LEFT COLUMN */
.left-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* TABS */
.tabs {
  display: flex;
  gap: 8px;
}

.tab {
  padding: 6px 14px;
  border-radius: 20px;
  background: #2a2a2a;
  border: 1px solid #444;
  color: #ddd;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.15s, color 0.15s;
}

.tab.active {
  background: #6b5a82;
  color: #fff;
  border-color: #6b5a82;
}

.tab:hover {
  background: #3a3a3a;
}

.tab-content {
  flex: 1;
  overflow-y: auto;
}
</style>
