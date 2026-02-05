<template>
  <div class="render-settings panel">

    <h2>Render Settings</h2>

    <!-- STYLE PRESET -->
    <div class="section">
      <label>Sprite Style</label>
      <select v-model="localSelectedStyle" @change="emitStyle">
        <option disabled value="">Select a style…</option>
        <option
          v-for="style in spriteStyles"
          :key="style.name"
          :value="style"
        >
          {{ style.name }}
        </option>
      </select>
    </div>

    <!-- PROMPT INPUT -->
    <div class="section">
      <label>Prompt</label>
      <textarea
        class="prompt-input"
        v-model="localPrompt"
        @input="emitPrompt"
        placeholder="Describe the sprite you want to generate…"
      />
    </div>

    <!-- REFINED PROMPT -->
    <div class="section" v-if="refinedPrompt">
      <label>Refined Prompt</label>
      <textarea
        class="refined-input"
        :value="refinedPrompt"
        readonly
      />
    </div>

    <button class="refine-btn" @click="$emit('refine-prompt')">
      Refine Prompt (AI)
    </button>

    <!-- REFERENCE IMAGES -->
    <div class="section">
      <label>Reference Images</label>

      <input
        type="file"
        accept="image/*"
        multiple
        @change="onAddReference"
      />

      <div class="reference-list">
        <div
          v-for="(ref, index) in referenceImages"
          :key="index"
          class="reference-item"
        >
          <img :src="ref.preview" class="reference-thumb" />
          <button class="remove-btn" @click="$emit('remove-reference', index)">
            ✕
          </button>
        </div>
      </div>
    </div>

    <!-- STRIDE -->
    <div class="section">
      <label>Stride</label>
      <input
        type="number"
        min="1"
        max="8"
        v-model.number="localStride"
        @input="emitStride"
      />
    </div>

    <!-- SETTINGS -->
    <div class="section">
      <label>Resolution</label>
      <input
        type="number"
        min="64"
        max="2048"
        v-model.number="localSettings.resolution"
        @input="emitSettings"
      />
    </div>

    <div class="section">
      <label>Variants</label>
      <input
        type="number"
        min="1"
        max="8"
        v-model.number="localSettings.variants"
        @input="emitSettings"
      />
    </div>

    <div class="section">
      <label>Seed</label>
      <input
        type="number"
        v-model.number="localSettings.seed"
        @input="emitSettings"
      />
    </div>

    <div class="section">
      <label>Background</label>
      <select v-model="localSettings.background" @change="emitSettings">
        <option value="transparent">Transparent</option>
        <option value="white">White</option>
        <option value="black">Black</option>
      </select>
    </div>

    <!-- MODEL SELECTION -->
    <div class="section">
      <label>Render Model</label>
      <select v-model="localSettings.render_model" @change="emitSettings">
        <option disabled value="">Select a model…</option>
        <option
          v-for="model in models"
          :key="model"
          :value="model"
        >
          {{ model }}
        </option>
      </select>
    </div>

    <!-- GENERATE -->
    <button class="generate-btn" @click="$emit('generate')">
      Generate Sprite
    </button>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

/* PROPS */
const props = defineProps({
  selectedMotion: Object,
  spriteStyles: Array,
  selectedStyle: Object,
  models: Array,
  settings: Object,
  referenceImages: Array,
  stride: Number,
  prompt: String,
  refinedPrompt: String,
})

/* EMITS */
const emit = defineEmits([
  'select-style',
  'update-settings',
  'add-reference',
  'remove-reference',
  'update-prompt',
  'refine-prompt',
  'update-stride',
  'generate',
])

/* LOCAL STATE */
const localSelectedStyle = ref(props.selectedStyle || "")
const localSettings = ref({ ...props.settings })
const localStride = ref(props.stride)
const localPrompt = ref(props.prompt)

/* WATCHERS */
watch(() => props.selectedStyle, v => localSelectedStyle.value = v)
watch(() => props.settings, v => localSettings.value = { ...v })
watch(() => props.stride, v => localStride.value = v)
watch(() => props.prompt, v => localPrompt.value = v)

/* EMITTERS */
function emitStyle() {
  emit('select-style', localSelectedStyle.value)
}

function emitSettings() {
  emit('update-settings', { ...localSettings.value })
}

function emitStride() {
  emit('update-stride', localStride.value)
}

function emitPrompt() {
  emit('update-prompt', localPrompt.value)
}

/* REFERENCE IMAGE UPLOAD */
function onAddReference(e) {
  const files = Array.from(e.target.files)
  for (const file of files) {
    const preview = URL.createObjectURL(file)
    emit('add-reference', { file, preview })
  }
}
</script>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.prompt-input,
.refined-input {
  width: 100%;
  min-height: 80px;
  padding: 8px;
  border-radius: 6px;
}

.reference-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.reference-item {
  position: relative;
}

.reference-thumb {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 4px;
}

.remove-btn {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #c00;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.generate-btn,
.refine-btn {
  padding: 10px 14px;
  border-radius: 6px;
  cursor: pointer;
}
</style>
