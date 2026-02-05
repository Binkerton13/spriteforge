<template>
  <div class="preset-details">

    <!-- NAME -->
    <div class="section">
      <label>Preset Name</label>
      <input
        type="text"
        v-model="localName"
        class="name-input"
        @input="emitName"
      />
    </div>

    <!-- SEGMENTS -->
    <div class="section">
      <label>Segments</label>

      <div
        v-for="(seg, index) in segments"
        :key="index"
        class="segment-block"
      >
        <h4>Segment {{ index + 1 }}</h4>

        <SegmentViewer
          :label="'Segment ' + (index + 1)"
          :value="seg"
          @update="val => emitField(index, val)"
        />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import SegmentViewer from './SegmentViewer.vue'

/* PROPS */
const props = defineProps({
  preset: { type: Object, required: true },
  segments: { type: Array, default: () => [] },
})

/* EMITS */
const emit = defineEmits([
  'update:name',
  'update:field',
])

/* LOCAL STATE */
const localName = ref(props.preset.name || '')

/* WATCH FOR EXTERNAL CHANGES */
watch(
  () => props.preset.name,
  v => localName.value = v
)

/* EMITTERS */
function emitName() {
  emit('update:name', localName.value)
}

function emitField(index, value) {
  emit('update:field', { seg: index, value })
}
</script>

<style scoped>
.preset-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: #f3f4f6;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.name-input {
  padding: 8px;
  border-radius: 6px;
  background: #1a1a1a;
  border: 1px solid #333;
  color: #eee;
}

.segment-block {
  background: #1e1e1e;
  border: 1px solid #333;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.segment-block h4 {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}
</style>
