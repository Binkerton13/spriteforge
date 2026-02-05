<template>
  <div class="overlay" v-if="visible">
    <div class="modal">
      <h2>File Browser</h2>

      <FileUpload @upload="onUpload" />

      <FileList
        :items="store.items"
        :selected="store.selected"
        @select="store.select"
        @open="store.load"
        @delete="store.remove"
      />

      <FilePreview :url="store.previewUrl" />

      <div class="actions">
        <button @click="$emit('cancel')">Cancel</button>
        <button @click="choose" :disabled="!store.selected">Choose</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useFilesStore } from '../../stores/files'
import FileList from './FileList.vue'
import FilePreview from './FilePreview.vue'
import FileUpload from './FileUpload.vue'

const props = defineProps(['visible'])
const emit = defineEmits(['cancel', 'choose'])

const store = useFilesStore()

// NEW: store actual uploaded file separately
const uploadedFile = ref(null)

// Reset selection when modal opens
watch(() => props.visible, (v) => {
  if (v) {
    store.selected = null
    uploadedFile.value = null
  }
})

function choose() {
  // If user uploaded a file, return that
  if (uploadedFile.value) {
    emit('choose', uploadedFile.value)
    return
  }

  // Otherwise return the selected file path
  emit('choose', store.selected)
}

function onUpload(file) {
  uploadedFile.value = file
  store.upload(file)
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: var(--bg-2);
  padding: 20px;
  border-radius: var(--radius);
  width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}
.actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}
</style>
