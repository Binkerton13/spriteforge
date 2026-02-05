<template>
  <div class="motion-prompt-editor">
    <h3>Motion Prompt</h3>

    <!-- OVERALL -->
    <SegmentField
      label="Overall Description"
      :value="motion.overall"
      @input="update('overall', $event)"
    />

    <!-- SEGMENTS -->
    <h4>Segments</h4>

    <SegmentField
      v-for="(val, key) in motion.segments"
      :key="key"
      :label="key"
      :value="val"
      @input="updateSegment(key, $event)"
    />

    <!-- TIMING -->
    <h4>Timing</h4>
    <SegmentField
      label="Timing"
      :value="motion.timing"
      @input="update('timing', $event)"
    />

    <!-- STYLE -->
    <h4>Style</h4>
    <SegmentField
      label="Style"
      :value="motion.style"
      @input="update('style', $event)"
    />

    <!-- CONSTRAINTS -->
    <h4>Constraints</h4>
    <SegmentField
      label="Constraints"
      :value="motion.constraints"
      @input="update('constraints', $event)"
    />
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import SegmentField from './SegmentField.vue'

const props = defineProps({
  motion: { type: Object, required: true }
})

const emit = defineEmits(['update-motion'])

function update(field, value) {
  const updated = { ...props.motion, [field]: value }
  emit('update-motion', updated)
}

function updateSegment(key, value) {
  const updated = {
    ...props.motion,
    segments: {
      ...props.motion.segments,
      [key]: value
    }
  }
  emit('update-motion', updated)
}
</script>

<style scoped>
.motion-prompt-editor {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
