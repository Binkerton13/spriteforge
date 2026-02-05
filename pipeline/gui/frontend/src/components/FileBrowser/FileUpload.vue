<template>
  <div class="upload">
    <input
      type="file"
      accept=".safetensors,.ckpt,.pth"
      @change="onChange"
    />
  </div>
</template>

<script setup>
const emit = defineEmits(['upload'])

function onChange(e) {
  const file = e.target.files[0]
  if (file) emit('upload', file)

  // Reset input so selecting the same file twice still triggers change
  e.target.value = ""
}
</script>

<style scoped>
.upload {
  margin-bottom: 10px;
}
</style>
