<template>
  <div class="panel">
    <h3>Upload</h3>
    <input type="file" @change="onFile" />
  </div>
</template>

<script setup>
const emit = defineEmits(['upload'])

function onFile(e) {
  const file = e.target.files[0]
  if (file) emit('upload', file)
}
</script>
