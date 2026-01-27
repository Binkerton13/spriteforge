<template>
  <div class="panel" v-if="frames.length">
    <h2>Frames</h2>
    <div class="grid">
      <img v-for="f in frames" :key="f" :src="f" />
    </div>
  </div>
</template>

<script setup>
defineProps(['frames'])
</script>

<style scoped>
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.grid img {
  width: 96px;
  border-radius: 4px;
}
</style>
