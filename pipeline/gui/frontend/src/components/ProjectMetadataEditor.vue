<template>
  <div class="panel">
    <h2>Metadata</h2>

    <label>Name</label>
    <input v-model="model.metadata.name" />

    <label>Description</label>
    <textarea v-model="model.metadata.description"></textarea>
  </div>
</template>

<script setup>
const model = defineProps(['model']).model
</script>

<style scoped>
input, textarea {
  width: 100%;
  background: #1e1e1e;
  color: #ddd;
  border: 1px solid #444;
  padding: 8px;
  border-radius: 4px;
  margin-bottom: 10px;
}
textarea {
  height: 100px;
}
</style>
