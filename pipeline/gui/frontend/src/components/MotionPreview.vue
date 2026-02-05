<template>
  <div class="motion-preview">

    <!-- No preview yet -->
    <div v-if="!hasPreview" class="placeholder">
      <p>No preview generated yet</p>
    </div>

    <!-- Video preview -->
    <video
      v-else-if="motion.output?.videoUrl"
      class="video"
      :src="motion.output.videoUrl"
      controls
      autoplay
      loop
    ></video>

    <!-- Frame sequence preview -->
    <div v-else-if="motion.output?.frames?.length" class="frames">

      <!-- Frame display -->
      <div class="frame-stack">

        <!-- Previous frame -->
        <img
          v-if="onionSkin && prevFrameSrc"
          class="frame ghost"
          :src="prevFrameSrc"
          :style="{ opacity: onionOpacity }"
        />

        <!-- Next frame -->
        <img
          v-if="onionSkin && nextFrameSrc"
          class="frame ghost"
          :src="nextFrameSrc"
          :style="{ opacity: onionOpacity }"
        />

        <!-- Current frame -->
        <img
          class="frame"
          :src="motion.output.frames[currentFrame]"
        />

      </div>
      <!-- Thumbnail Timeline -->
      <div v-if="motion.output?.frames?.length" class="thumbnail-strip">
        <img
          v-for="(src, index) in motion.output.frames"
          :key="index"
          class="thumbnail"
          :src="src"
          :class="{ active: index === currentFrame }"
          @click="jumpToFrame(index)"
        />
      </div>

      <!-- Controls -->
      <div class="controls">
        <button @click="togglePlay">
          {{ isPlaying ? 'Pause' : 'Play' }}
        </button>
        <button @click="onionSkin = !onionSkin">
          {{ onionSkin ? 'Onion: On' : 'Onion: Off' }}
        </button>
        <label class="speed-label">
          Speed
          <input
            type="range"
            min="50"
            max="300"
            step="10"
            v-model="playbackSpeed"
          />
        </label>
      </div>

      <!-- Scrubber -->
      <input
        type="range"
        class="scrubber"
        :min="0"
        :max="motion.output.frames.length - 1"
        v-model="currentFrame"
        @input="pauseOnScrub"
      />
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  motion: { type: Object, default: null }
})
const onionSkin = ref(false)
const onionOpacity = ref(0.4)
const thumbSize = 60 // px

const currentFrame = ref(0)
const isPlaying = ref(false)
const playbackSpeed = ref(120) // ms per frame
let playInterval = null

const hasPreview = computed(() => {
  if (!props.motion) return false
  const out = props.motion.output
  return !!(out?.videoUrl || (out?.frames && out.frames.length))
})

/* Auto-stop when preview changes */
watch(() => props.motion?.output, () => {
  stopPlayback()
  currentFrame.value = 0
})

function togglePlay() {
  if (isPlaying.value) {
    stopPlayback()
  } else {
    startPlayback()
  }
}

function startPlayback() {
  if (!props.motion?.output?.frames) return
  isPlaying.value = true

  playInterval = setInterval(() => {
    const frames = props.motion.output.frames.length
    currentFrame.value = (currentFrame.value + 1) % frames
  }, playbackSpeed.value)
}

function stopPlayback() {
  isPlaying.value = false
  if (playInterval) clearInterval(playInterval)
  playInterval = null
}

function pauseOnScrub() {
  stopPlayback()
}

const prevFrameSrc = computed(() => {
  if (!props.motion?.output?.frames) return null
  const frames = props.motion.output.frames
  if (frames.length < 2) return null
  const index = (currentFrame.value - 1 + frames.length) % frames.length
  return frames[index]
})

const nextFrameSrc = computed(() => {
  if (!props.motion?.output?.frames) return null
  const frames = props.motion.output.frames
  if (frames.length < 2) return null
  const index = (currentFrame.value + 1) % frames.length
  return frames[index]
})

function jumpToFrame(index) {
  stopPlayback()
  currentFrame.value = index
}

watch(playbackSpeed, () => {
  if (isPlaying.value) {
    stopPlayback()
    startPlayback()
  }
})

onBeforeUnmount(() => stopPlayback())
</script>

<style scoped>
.motion-preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  height: 100%;
}

.placeholder {
  background: #111;
  border: 1px solid #333;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  color: #777;
}

.video {
  width: 100%;
  border-radius: 8px;
  border: 1px solid #333;
}

.frames {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.frame {
  width: 100%;
  border-radius: 8px;
  border: 1px solid #333;
}

.frame-stack {
  position: relative;
  width: 100%;
}

.frame-stack .frame {
  width: 100%;
  border-radius: 8px;
  border: 1px solid #333;
  display: block;
}

.frame-stack .ghost {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
}

.thumbnail-strip {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding: 4px 0;
}

.thumbnail {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #333;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.15s, transform 0.15s;
}

.thumbnail:hover {
  opacity: 1;
  transform: scale(1.05);
}

.thumbnail.active {
  opacity: 1;
  border-color: #4da3ff;
}

.controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.speed-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  opacity: 0.8;
}

.scrubber {
  width: 100%;
}
</style>
