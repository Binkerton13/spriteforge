<template>
  <div>
    <button class="upload" @click="open = true">Upload Model</button>

    <div v-if="open" class="modal">
      <div class="modal-content">

        <h3>Upload Model</h3>

        <!-- Model Type Selector -->
        <label>Model Type</label>
        <select v-model="modelType">
          <option disabled value="">Select type...</option>
          <option value="checkpoints">Checkpoint</option>
          <option value="loras">LoRA</option>
          <option value="vae">VAE</option>
          <option value="controlnet">ControlNet</option>
          <option value="ipadapter">IP‑Adapter</option>
          <option value="animatediff">AnimateDiff</option>
        </select>

        <!-- File Browser Trigger -->
        <button @click="fileBrowserOpen = true">
          Choose File
        </button>

        <p v-if="file">Selected: {{ file.name }}</p>

        <!-- Upload Button -->
        <button
          :disabled="!file || !modelType"
          @click="upload"
        >
          Upload
        </button>

        <button @click="close">Cancel</button>
      </div>
    </div>

    <!-- Your existing file browser -->
    <FileBrowserModal
      :visible="fileBrowserOpen"
      @cancel="fileBrowserOpen = false"
      @choose="onChoose"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import FileBrowserModal from './FileBrowser/FileBrowserModal.vue'

const emit = defineEmits(['uploaded'])

const open = ref(false)
const fileBrowserOpen = ref(false)
const file = ref(null)
const modelType = ref('')

function onChoose(selected) {
  file.value = selected
  fileBrowserOpen.value = false
}

function close() {
  open.value = false
  file.value = null
  modelType.value = ''
}

async function upload() {
  const form = new FormData()
  form.append("file", file.value)
  form.append("type", modelType.value)

  await axios.post("/api/models/upload", form)

  emit("uploaded")
  close()
}
</script>

<style scoped>
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 6px;
  width: 300px;
}
</style>
