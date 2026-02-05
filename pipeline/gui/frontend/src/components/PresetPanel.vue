<template>
  <div class="preset-panel">

    <!-- HEADER -->
    <div class="header">
      <h3>Motion Presets</h3>

      <button class="new-btn" @click="createPreset">
        New
      </button>
    </div>

    <!-- PRESET LIST -->
    <div class="preset-list">
      <div
        v-for="(p, index) in presets"
        :key="index"
        class="preset-item"
        :class="{ active: p === selectedPreset }"
        @click="select(p)"
      >
        {{ p.name }}
      </div>
    </div>

    <!-- PRESET EDITOR -->
    <div v-if="selectedPreset" class="editor">

      <label>Name</label>
      <input
        v-model="localPreset.name"
        @input="emitUpdate"
        class="name-input"
      />

      <h4>Preset Fields</h4>

      <!-- OVERALL -->
      <SegmentField
        label="Overall"
        :value="localPreset.overall"
        @input="updateField('overall', $event)"
      />

      <!-- SEGMENTS -->
      <h4>Segments</h4>
      <SegmentField
        v-for="(val, key) in localPreset.segments"
        :key="key"
        :label="key"
        :value="val"
        @input="updateSegment(key, $event)"
      />

      <!-- TIMING -->
      <h4>Timing</h4>
      <SegmentField
        label="Timing"
        :value="localPreset.timing"
        @input="updateField('timing', $event)"
      />

      <!-- STYLE -->
      <h4>Style</h4>
      <SegmentField
        label="Style"
        :value="localPreset.style"
        @input="updateField('style', $event)"
      />

      <!-- CONSTRAINTS -->
      <h4>Constraints</h4>
      <SegmentField
        label="Constraints"
        :value="localPreset.constraints"
        @input="updateField('constraints', $event)"
      />

      <!-- ACTIONS -->
      <div class="actions">
        <button class="save-btn" @click="savePreset">Save</button>
        <button class="delete-btn" @click="deletePreset">Delete</button>
        <button class="apply-btn" @click="applyPreset">Apply to Motion</button>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import SegmentField from './SegmentField.vue'

const props = defineProps({
  presets: Array,
  selectedPreset: Object
})

const emit = defineEmits([
  'select-preset',
  'update-preset',
  'create-preset',
  'delete-preset',
  'apply-preset'
])

const localPreset = ref({})

watch(
  () => props.selectedPreset,
  p => {
    localPreset.value = JSON.parse(JSON.stringify(p || {}))
  }
)

function select(p) {
  emit('select-preset', p)
}

function createPreset() {
  emit('create-preset')
}

function savePreset() {
  emit('update-preset', localPreset.value)
}

function deletePreset() {
  emit('delete-preset', localPreset.value)
}

function applyPreset() {
  emit('apply-preset', localPreset.value)
}

function updateField(field, value) {
  localPreset.value[field] = value
  emit('update-preset', localPreset.value)
}

function updateSegment(key, value) {
  localPreset.value.segments[key] = value
  emit('update-preset', localPreset.value)
}
</script>

<style scoped>
.preset-panel {
  background: #1a1a1a;
  border: 1px solid #333;
  padding: 14px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.preset-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.preset-item {
  padding: 6px 10px;
  background: #222;
  border-radius: 4px;
  cursor: pointer;
}
.preset-item.active {
  background: #333;
  border-left: 4px solid #4da3ff;
}
.editor {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.actions {
  display: flex;
  gap: 10px;
}
</style>
