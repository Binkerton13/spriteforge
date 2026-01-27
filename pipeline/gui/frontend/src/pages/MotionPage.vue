<template>
  <div class="page">
    <h1>Motion Generator</h1>

    <div class="panel">
      <h2>Preset</h2>
      <select v-model="store.selectedPreset">
        <option disabled value="">Select a preset</option>
        <option v-for="p in store.presets" :key="p" :value="p">
          {{ p }}
        </option>
      </select>
    </div>

    <div class="panel">
      <h2>Seed</h2>
      <input type="number" v-model="store.seed" />
    </div>

    <button @click="store.runGeneration" :disabled="store.loading">
      {{ store.loading ? "Generating..." : "Generate Motion" }}
    </button>

    <div v-if="store.videoUrl" class="panel">
      <h2>Preview</h2>
      <video controls :src="store.videoUrl" width="480"></video>
    </div>

    <div v-if="store.frames.length" class="panel">
      <h2>Frames</h2>
      <div class="frames">
        <img v-for="f in store.frames" :key="f" :src="f" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMotionStore } from '../stores/motion'

const store = useMotionStore()

onMounted(() => {
  store.loadPresets()
})
</script>

<style scoped>
.page {
  padding: 24px;
  min-height: 100vh;
  background: var(--bg-0);
  color: var(--fg-0);
}


.panel {
  background: #2d2d30;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 6px;
}

.frames {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.frames img {
  width: 96px;
  height: auto;
  border-radius: 4px;
}
</style>
