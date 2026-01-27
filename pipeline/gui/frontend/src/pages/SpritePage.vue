<template>
  <div class="page">
    <h1>Sprite Generator</h1>

    <SpriteStyleSelector :model="store" />
    <SpriteModelSelector :model="store" />
    <SpriteGenerationSettings :model="store" />

    <button @click="store.runGeneration" :disabled="store.loading">
      {{ store.loading ? "Generating..." : "Generate Sprites" }}
    </button>

    <SpriteFrameGrid :frames="store.frames" />

    <button v-if="store.frames.length" @click="store.assemble" :disabled="store.loading">
      {{ store.loading ? "Assembling..." : "Assemble Sprite Sheet" }}
    </button>

    <SpriteSheetAssembler :sheetUrl="store.sheetUrl" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useSpritesStore } from '../stores/sprites'

import SpriteStyleSelector from '../components/SpriteStyleSelector.vue'
import SpriteModelSelector from '../components/SpriteModelSelector.vue'
import SpriteGenerationSettings from '../components/SpriteGenerationSettings.vue'
import SpriteFrameGrid from '../components/SpriteFrameGrid.vue'
import SpriteSheetAssembler from '../components/SpriteSheetAssembler.vue'

const store = useSpritesStore()

onMounted(() => {
  store.loadInitial()
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
</style>
