<template>
  <div class="panel">
    <h2>Active {{ labels[type] || type }}</h2>
    <p>{{ model || "None selected" }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  model: { type: String, required: false },
  type: { type: String, required: true }
})

const labels = {
  checkpoints: "Checkpoint",
  loras: "LoRA",
  vae: "VAE",
  controlnet: "ControlNet",
  ipadapter: "IP‑Adapter",
  animatediff: "AnimateDiff"
}
</script>

<style scoped>
</style>
