<template>
  <div class="segment-field">
    <label class="label">{{ label }}</label>

    <textarea
      ref="textarea"
      class="editor"
      v-model="localText"
      @input="onInput"
    ></textarea>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'

const props = defineProps({
  label: { type: String, default: '' },
  value: { type: [String, Array, Object], default: '' },
})

const emit = defineEmits(['input'])

const localText = ref(safeStringify(props.value))
const textarea = ref(null)

/* Resize textarea to fit content */
function autoResize() {
  const el = textarea.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = el.scrollHeight + 'px'
}

watch(
  () => props.value,
  v => {
    localText.value = safeStringify(v)
    nextTick(autoResize)
  }
)

onMounted(() => nextTick(autoResize))

function safeStringify(v) {
  try {
    return typeof v === 'string'
      ? v
      : JSON.stringify(v, null, 2)
  } catch {
    return ''
  }
}

function safeParse(text) {
  try {
    return JSON.parse(text)
  } catch {
    return text
  }
}

function onInput() {
  autoResize()
  emit('input', safeParse(localText.value))
}
</script>

<style scoped>
.segment-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}

.label {
  font-size: 13px;
  opacity: 0.75;
  padding-left: 2px;
}

.editor {
  width: 100%;
  min-height: 40px;       /* Much smaller initial height */
  max-height: 200px;      /* Prevents giant fields */
  overflow-y: auto;       /* Scroll if too large */
  box-sizing: border-box;
  padding: 6px 8px;
  border-radius: 6px;
  background: #111;
  color: #eee;
  border: 1px solid #333;
  font-family: monospace;
  font-size: 13px;
  line-height: 1.35;
  resize: none;           /* We handle resizing automatically */
}
.name-input {
  width: 100%;
}
</style>
