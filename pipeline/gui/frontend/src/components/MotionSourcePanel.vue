<template>
  <div class="motion-source panel">

    <h2>Motion Sources</h2>

    <!-- IMPORT -->
    <div class="section">
      <label>Import Motion</label>
      <input
        type="file"
        accept=".json,.motion,.txt"
        @change="onImport"
      />
    </div>

    <!-- LIST -->
    <div class="section">
      <label>Available Motions</label>

      <div class="motion-list">
        <div
          v-for="(motion, index) in motions"
          :key="index"
          class="motion-item"
          :class="{ active: motion === selectedMotion }"
          @click="$emit('select-motion', motion)"
        >
          <strong>{{ motion.name || 'Imported Motion' }}</strong>
          <span class="meta">
            {{ motion.segments?.length || 0 }} segments
          </span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

/* PROPS */
const props = defineProps({
  motions: Array,
  selectedMotion: Object,
})

/* EMITS */
const emit = defineEmits([
  'select-motion',
  'import-motion',
])

/* IMPORT HANDLER */
function onImport(e) {
  const file = e.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    try {
      const json = JSON.parse(reader.result)
      emit('import-motion', json)
    } catch (err) {
      console.error('Invalid motion file:', err)
    }
  }
  reader.readAsText(file)
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
  gap: 8px;
}

.motion-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.motion-item {
  padding: 10px;
  border-radius: 6px;
  background: #1a1a1a;
  cursor: pointer;
  transition: background 0.2s;
}

.motion-item:hover {
  background: #2a2a2a;
}

.motion-item.active {
  background: #333;
  border-left: 4px solid #4da3ff;
}

.meta {
  font-size: 12px;
  opacity: 0.7;
}
</style>
