<template>
  <div class="sprite-output panel">

    <h2>Output</h2>

    <!-- GENERATION STATUS -->
    <div v-if="generating" class="status">
      <div class="spinner"></div>
      <span>Generating sprite…</span>
    </div>

    <!-- FRAMES -->
    <div v-if="frames?.length" class="frames-section">
      <h3>Frames ({{ frames.length }})</h3>

      <div class="frame-grid">
        <img
          v-for="(frame, index) in frames"
          :key="index"
          :src="frame"
          class="frame-thumb"
        />
      </div>
    </div>

    <!-- SPRITE SHEET -->
    <div v-if="sheet" class="sheet-section">
      <h3>Sprite Sheet</h3>
      <img :src="sheet" class="sheet-image" />
    </div>

    <!-- HISTORY -->
    <div v-if="history?.length" class="history-section">
      <h3>History</h3>

      <div class="history-list">
        <div
          v-for="(entry, index) in history"
          :key="index"
          class="history-item"
          @click="$emit('select-history', entry)"
        >
          <div class="history-meta">
            <strong>{{ formatTimestamp(entry.timestamp) }}</strong>
            <span>{{ entry.frames?.length || 0 }} frames</span>
          </div>

          <img
            v-if="entry.sheet"
            :src="entry.sheet"
            class="history-thumb"
          />
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

/* PROPS */
const props = defineProps({
  frames: Array,
  sheet: String,
  history: Array,
  generating: Boolean,
})

/* EMITS */
defineEmits(['select-history'])

/* HELPERS */
function formatTimestamp(ts) {
  const d = new Date(ts)
  return d.toLocaleString()
}
</script>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 3px solid #ccc;
  border-top-color: #444;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.frames-section,
.sheet-section,
.history-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.frame-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 64px);
  gap: 8px;
}

.frame-thumb {
  width: 64px;
  height: 64px;
  object-fit: contain;
  border-radius: 4px;
  background: #222;
}

.sheet-image {
  width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 6px;
  background: #222;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 6px;
  background: #1a1a1a;
  cursor: pointer;
  transition: background 0.2s;
}

.history-item:hover {
  background: #2a2a2a;
}

.history-meta {
  display: flex;
  flex-direction: column;
}

.history-thumb {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 4px;
  background: #222;
}
</style>
