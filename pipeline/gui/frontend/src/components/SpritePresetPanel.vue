<template>
  <div class="sprite-preset-panel">

    <!-- LEFT: PRESET LIST -->
    <aside class="preset-list">
      <h2>Sprite Presets</h2>

      <ul>
        <li
          v-for="p in presets"
          :key="p.id"
          :class="{ active: p.id === selectedPresetId }"
          @click="selectPreset(p.id)"
        >
          {{ p.name }}
        </li>
      </ul>

      <div class="buttons">
        <button @click="createPreset">New Preset</button>
        <button @click="deletePreset" :disabled="!selectedPreset">Delete</button>
      </div>
    </aside>

    <!-- RIGHT: DETAILS -->
    <section class="details" v-if="selectedPreset">
      <SpritePresetDetails
        :preset="selectedPreset"
        @update:name="updateName"
        @update:prompt="updatePrompt"
        @update:settings="updateSettings"
        @update:style="updateStyle"
      />
    </section>

    <section v-else class="empty">
      Select or create a preset.
    </section>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSpritePresetsStore } from '@/stores/spritePresets'
import SpritePresetDetails from './SpritePresetDetails.vue'

const store = useSpritePresetsStore()

const presets = computed(() => store.presets)
const selectedPreset = computed(() => store.selectedPreset)
const selectedPresetId = computed(() => store.selectedPresetId)

function selectPreset(id) { store.setPreset(id) }
function createPreset() { store.createPreset() }
function deletePreset() { store.deletePreset(selectedPresetId.value) }

function updateName(name) { store.updateName(name) }
function updatePrompt(prompt) { store.updateField('prompt', prompt) }
function updateSettings(settings) { store.updateSettings(settings) }
function updateStyle(style) { store.updateStyle(style) }
</script>

<style scoped>
/* same styling as Motion Preset Panel */
</style>
