<template>
  <div class="preview" v-if="url">
    
    <!-- Image preview -->
    <img
      v-if="isImage"
      :src="url"
      alt="Preview"
    />

    <!-- Video preview -->
    <video
      v-else-if="isVideo"
      :src="url"
      controls
    />

    <!-- Text preview -->
    <iframe
      v-else-if="isText"
      :src="url"
      class="text-frame"
    ></iframe>

    <!-- Fallback -->
    <div v-else class="unsupported">
      Cannot preview this file.
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps(['url'])

const isImage = computed(() =>
  /\.(png|jpg|jpeg|gif|webp)$/i.test(props.url || '')
)

const isVideo = computed(() =>
  /\.(mp4|webm|mov)$/i.test(props.url || '')
)

const isText = computed(() =>
  /\.(txt|json|yaml|yml|md)$/i.test(props.url || '')
)
</script>

<style scoped>
.preview {
  margin-top: 20px;
}

.preview img,
.preview video,
.text-frame {
  max-width: 100%;
  border-radius: 4px;
}

.text-frame {
  height: 300px;
  border: 1px solid var(--bg-3);
}

.unsupported {
  opacity: 0.6;
  font-style: italic;
  padding: 10px;
}
</style>
