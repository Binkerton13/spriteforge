<template>
  <div class="style-selector">

    <label class="label">{{ label }}</label>

    <div class="combo">
      <!-- INPUT FIELD -->
      <input
        type="text"
        v-model="query"
        class="combo-input"
        @focus="open = true"
        @input="onInput"
        @keydown.down.prevent="move(1)"
        @keydown.up.prevent="move(-1)"
        @keydown.enter.prevent="selectHighlighted"
        placeholder="Select or type a style…"
      />

      <!-- DROPDOWN -->
      <div v-if="open" class="dropdown">
        <div
          v-for="(style, index) in filtered"
          :key="style.name"
          class="item"
          :class="{ active: index === highlighted }"
          @mousedown.prevent="choose(style)"
        >
          {{ style.name }}
        </div>

        <!-- CUSTOM ENTRY -->
        <div
          v-if="allowCustom && query && !exists(query)"
          class="item custom"
          @mousedown.prevent="choose({ name: query })"
        >
          Add “{{ query }}”
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

/* PROPS */
const props = defineProps({
  styles: { type: Array, default: () => [] },   // [{ name, detail? }]
  selected: { type: Object, default: null },
  label: { type: String, default: 'Style' },
  allowCustom: { type: Boolean, default: true },
})

/* EMITS */
const emit = defineEmits(['select'])

/* STATE */
const query = ref(props.selected?.name || '')
const open = ref(false)
const highlighted = ref(0)

/* WATCH FOR EXTERNAL CHANGES */
watch(
  () => props.selected,
  v => query.value = v?.name || ''
)

/* FILTERED LIST */
const filtered = computed(() => {
  const q = query.value.toLowerCase()
  return props.styles.filter(s => s.name.toLowerCase().includes(q))
})

/* HELPERS */
function exists(name) {
  return props.styles.some(s => s.name.toLowerCase() === name.toLowerCase())
}

function onInput() {
  open.value = true
  highlighted.value = 0
}

function choose(style) {
  query.value = style.name
  open.value = false
  emit('select', style)
}

function move(dir) {
  if (!open.value) open.value = true
  const max = filtered.value.length - 1
  highlighted.value = Math.min(max, Math.max(0, highlighted.value + dir))
}

function selectHighlighted() {
  const list = filtered.value
  if (list.length) choose(list[highlighted.value])
  else if (props.allowCustom && query.value) choose({ name: query.value })
}
</script>

<style scoped>
.style-selector {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label {
  font-size: 14px;
  opacity: 0.8;
}

.combo {
  position: relative;
}

.combo-input {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  background: #1a1a1a;
  border: 1px solid #333;
  color: #eee;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 6px;
  margin-top: 4px;
  max-height: 180px;
  overflow-y: auto;
  z-index: 20;
}

.item {
  padding: 8px;
  cursor: pointer;
  transition: background 0.15s;
}

.item:hover,
.item.active {
  background: #333;
}

.item.custom {
  font-style: italic;
  opacity: 0.9;
}
</style>
