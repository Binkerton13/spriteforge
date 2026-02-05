<template>
  <div class="tabs">
    <div
      v-for="t in types"
      :key="t"
      class="tab"
      :class="{ active: t === activeType }"
      @click="$emit('select', t)"
    >
      {{ labels[t] || t }}
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['types', 'activeType'])

const labels = {
  checkpoints: "Checkpoints",
  loras: "LoRAs",
  vae: "VAEs",
  controlnet: "ControlNet",
  ipadapter: "IP‑Adapter",
  animatediff: "AnimateDiff"
}
</script>
