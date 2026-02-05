<template>
  <div class="motion-page">

    <!-- LEFT: Available Motions -->
    <aside class="left-panel">
      <h3>Available Motions</h3>

      <button class="create-btn" @click="createNewMotion">
        + New Motion
      </button>

      <MotionList
        :motions="motionStore.motions"
        @select="selectMotion"
      />
    </aside>

    <!-- CENTER PANEL -->
    <main class="center-panel">

      <!-- Guard the entire editor, but NOT the name field -->
      <div v-if="selectedMotion">

        <!-- Motion Name -->
        <div class="field-block">
          <label>Name</label>
          <input v-model="motionName" class="text-input" />
        </div>

        <!-- Motion Description -->
        <div class="field-block">
          <label>Motion Description</label>
          <SegmentField
            :value="selectedMotion.overall"
            @input="v => updateMotionField('overall', v)"
          />
        </div>

        <!-- Style -->
        <div class="field-block">
          <label>Style</label>
          <SegmentField
            :value="selectedMotion.style"
            @input="v => updateMotionField('style', v)"
          />
        </div>

        <!-- AI Actions -->
        <div class="ai-actions">
          <button @click="suggestMotion">Suggest</button>
          <button @click="refineMotion">Refine</button>
          <button @click="applyStyle">Style</button>
        </div>

        <!-- Segments -->
        <details class="segments-block" open>
          <summary>Segments</summary>

          <div class="segments-grid">
            <SegmentField
              v-for="(val, key) in selectedMotion.segments"
              :key="key"
              :label="key"
              :value="val"
              @input="v => updateSegment(key, v)"
            />
          </div>
        </details>

        <!-- HY-Motion Actions -->
        <div class="hy-actions">
          <button @click="generateMotion">Generate Motion</button>
          <button @click="previewMotion">Preview</button>
          <button @click="saveMotion">Save Motion</button>
        </div>

        <!-- Preset Utility -->
        <div class="preset-utility">
          <button @click="openPresetMenu">Load Preset</button>
          <button @click="saveAsPreset">Save as Preset</button>
          <button @click="deletePreset">Delete Preset</button>
        </div>

      </div>

      <!-- If selectedMotion is null -->
      <div v-else class="empty-state">
        <p>No motion selected. Create or load one from the left panel.</p>
      </div>

    </main>

    <!-- RIGHT: Preview -->
    <aside class="right-panel">
      <MotionPreview :motion="selectedMotion" />
    </aside>

  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue'

import SegmentField from '../components/SegmentField.vue'
import MotionPreview from '../components/MotionPreview.vue'

import { useMotionStore } from '../stores/motion'
import { useMotionStylesStore } from '../stores/motionStyles'
import { useProjectsStore } from '../stores/projects'
import { useMotionPresetsStore } from '../stores/motionPresets'

/* STORES */
const projects = useProjectsStore()
const motionStore = useMotionStore()
const motionStylesStore = useMotionStylesStore()
const presetStore = useMotionPresetsStore() 
const presets = presetStore.presets 


/* LOCAL STATE */
const selectedMotion = ref(null)
const selectedStyle = ref(null)
const motionName = ref("New Motion")
const selectedPreset = ref(null)
const prompt = ref("")
const refinedPrompt = ref("")

/* DERIVED DATA */
const motions = motionStore.motions
const motionStyles = motionStylesStore.styles

/* SKELETONS */
const skeletons = ref([])
const selectedSkeleton = ref('human')

/* ACTIONS */
function createNewMotion() {
  const empty = createEmptyMotionForSkeleton(selectedSkeleton.value)

  const newMotion = {
  id: crypto.randomUUID(),
  name: "New Motion",
  ...empty
}


  selectedMotion.value = newMotion
  motionName.value = "New Motion"

  // Add to store list
  motionStore.motions.push(newMotion)
}

function selectMotion(motion) {
  selectedMotion.value = JSON.parse(JSON.stringify(motion))
  motionName.value = motion.name || "New Motion"
}

function saveMotion() {
  if (!selectedMotion.value) return

  selectedMotion.value.name = motionName.value

  const index = motionStore.motions.findIndex(
    m => m.id === selectedMotion.value.id
  )

  if (index !== -1) {
    motionStore.motions[index] = JSON.parse(JSON.stringify(selectedMotion.value))
  } else {
    motionStore.motions.push(JSON.parse(JSON.stringify(selectedMotion.value)))
  }
}

function updateSegment(key, value) {
  if (!selectedMotion.value) return
  selectedMotion.value.segments[key] = value
}

function updateMotionField(field, value) {
  if (!selectedMotion.value) return
  selectedMotion.value[field] = value
}

function importMotion(fileObj) {
  motionStore.importMotion(fileObj)
}

function selectStyle(style) {
  selectedStyle.value = style
}

function updatePrompt(text) {
  prompt.value = text
}

function updateMotion(updated) {
  selectedMotion.value = updated
}

/* LOAD SKELETONS */
async function loadSkeletons() { 
  const res = await fetch('/api/motion/skeletons') 
  const data = await res.json() 
  skeletons.value = data.skeletons 
}

function createEmptyMotionForSkeleton(skeletonId) {
  const sk = skeletons.value.find(s => s.id === skeletonId)
  if (!sk) return null

  const segments = {}
  for (const seg of sk.segments) {
    segments[seg] = ""
  }

  return {
    skeleton: skeletonId,
    overall: "",
    segments,
    timing: {
      beats: "",
      phases: "",
      duration: 1.0
    },
    style: {
      primary: "",
      secondary: "",
      notes: ""
    },
    constraints: {
      physical: "",
      camera: "",
      notes: ""
    },
    output: null,
    preview: null,
  }
}

function onSkeletonChange() {
  selectedMotion.value = createEmptyMotionForSkeleton(selectedSkeleton.value)
}

/* PRESET MANAGEMENT */


/* AI ACTIONS */

async function suggestMotion() {
  const result = await motionStore.suggest(
    selectedMotion.value.overall,
    {
      skeleton: selectedMotion.value.skeleton || "human",
      preset: selectedPreset.value || {}
    }
  )
  selectedMotion.value = result.motion
}

async function refineMotion() {
  const result = await motionStore.refine(
    selectedMotion.value.overall,
    selectedMotion.value
  )
  selectedMotion.value = result.motion
}

async function applyStyle() {
  const result = await motionStore.style(
    selectedMotion.value.style?.primary || "",
    selectedMotion.value
  )
  selectedMotion.value = result.motion
}

async function translateMotionToEnglish() {
  if (!selectedMotion.value) return

  const result = await motionStore.translate(selectedMotion.value, "en")
  selectedMotion.value = result
}

async function generateMotion() {
  const result = await motionStore.generate(selectedMotion.value)
  selectedMotion.value.output = result
}

async function previewMotion() {
  const preview = await motionStore.loadPreview(selectedMotion.value.output)
  selectedMotion.value.preview = preview
}

function openPresetMenu() {
  // You can use a modal or dropdown
}

function saveAsPreset() {
  const preset = JSON.parse(JSON.stringify(selectedMotion.value))
  preset.name = motionName.value || "New Motion"

  presetStore.presets.push(preset)
  presetStore.saveAll()
}

function deletePreset() {
  if (!selectedPreset.value) return
  presetStore.deletePreset(selectedPreset.value.name)
  selectedPreset.value = null
}

function applyPresetToMotion(preset) {
  if (!selectedMotion.value) return

  const updated = { ...selectedMotion.value }

  updated.overall = preset.overall || updated.overall
  updated.style = { ...updated.style, ...preset.style }
  updated.timing = { ...updated.timing, ...preset.timing }
  updated.constraints = { ...updated.constraints, ...preset.constraints }

  updated.segments = {
    ...updated.segments,
    ...preset.segments
  }

  selectedMotion.value = updated
}

/* INITIAL LOAD */
onMounted(async () => {
  projects.ensureLoaded()
  motionStylesStore.ensureLoaded()

  await loadSkeletons()
  await presetStore.ensureLoaded()

  if (!selectedMotion.value) {
    createNewMotion()
  }
})
</script>

<style scoped>
.motion-page {
  display: grid;
  grid-template-columns: 240px 1fr 300px;
  gap: 20px;
  height: 100%;
  padding: 20px;
}

.left-panel,
.right-panel {
  background: #111;
  border: 1px solid #333;
  padding: 12px;
  border-radius: 8px;
  overflow-y: auto;
}

.center-panel {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.text-input {
  padding: 6px 10px;
  background: #111;
  border: 1px solid #333;
  border-radius: 6px;
  color: #eee;
}

.ai-actions,
.hy-actions,
.preset-utility {
  display: flex;
  gap: 10px;
}

.segments-block summary {
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 8px;
}

.segments-grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.hy-actions,
.preset-utility {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
}

.create-btn {
  width: 100%;
  padding: 6px 10px;
  margin-bottom: 10px;
  background: #222;
  border: 1px solid #444;
  border-radius: 6px;
  color: #eee;
  cursor: pointer;
}

.create-btn:hover {
  background: #333;
}

</style>

