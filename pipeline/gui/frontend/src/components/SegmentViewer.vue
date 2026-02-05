<template>
  <div class="segment-viewer">

    <!-- HEADER -->
    <div class="header">
      <h3>{{ label }}</h3>

      <button class="edit-btn" @click="toggleEdit">
        {{ editing ? 'Done' : 'Edit' }}
      </button>
    </div>

    <!-- EDIT MODE -->
    <div v-if="editing" class="edit-mode">
      <textarea
        v-model="localText"
        class="editor"
        @input="onEdit"
      ></textarea>
    </div>

    <!-- VIEW MODE -->
    <div v-else class="view-mode">
      <div v-if="isString" class="string-view">
        {{ value }}
      </div>

      <ul v-else-if="isArray" class="array-view">
        <li v-for="(item, index) in value" :key="index">
          <strong>{{ index }}:</strong> {{ format(item) }}
        </li>
      </ul>

      <ul v-else-if="isObject" class="object-view">
        <li v-for="(item, key) in value" :key="key">
          <strong>{{ key }}:</strong> {{ format(item) }}
        </li>
      </ul>

      <div v-else class="unknown-view">
        {{ format(value) }}
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

/* PROPS */
const props = defineProps({
  label: { type: String, default: '' },
  value: { type: [String, Array, Object], default: '' },
})

/* EMITS */
const emit = defineEmits(['update'])

/* LOCAL STATE */
const editing = ref(false)
const localText = ref(safeStringify(props.value))

/* WATCH FOR EXTERNAL CHANGES */
watch(
  () => props.value,
  v => {
    if (!editing.value) {
      localText.value = safeStringify(v)
    }
  }
)

/* TYPE CHECKS */
const isString = computed(() => typeof props.value === 'string')
const isArray = computed(() => Array.isArray(props.value))
const isObject = computed(() => props.value && typeof props.value === 'object' && !Array.isArray(props.value))

/* HELPERS */
function safeStringify(v) {
  try {
    return typeof v === 'string' ? v : JSON.stringify(v, null, 2)
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

function format(v) {
  if (typeof v === 'object') return JSON.stringify(v)
  return String(v)
}

/* EDIT HANDLERS */
function toggleEdit() {
  editing.value = !editing.value

  if (!editing.value) {
    // Leaving edit mode → emit parsed value
    emit('update', safeParse(localText.value))
  }
}

function onEdit() {
  // Live update while typing (optional)
  // emit('update', safeParse(localText.value))
}
</script>

<style scoped>
.segment-viewer {
  background: #1a1a1a;
  border: 1px solid #333;
  padding: 12px;
  border-radius: 8px;
  color: #eee;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.edit-btn {
  background: #444;
  border: none;
  padding: 4px 10px;
  border-radius: 4px;
  color: #eee;
  cursor: pointer;
}

.editor {
  width: 100%;
  min-height: 120px;
  background: #111;
  color: #eee;
  border: 1px solid #444;
  border-radius: 6px;
  padding: 8px;
  font-family: monospace;
}

.view-mode ul {
  list-style: none;
  padding-left: 0;
}

.view-mode li {
  padding: 2px 0;
}

.string-view {
  white-space: pre-wrap;
}
</style>
