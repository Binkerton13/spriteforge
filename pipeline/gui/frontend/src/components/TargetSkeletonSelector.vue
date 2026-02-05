<!-- TargetSkeletonSelector.vue -->
<script setup>
defineProps({
  modelValue: String,
  options: Array
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div class="target-skeleton-selector">
    <label>Translate To</label>
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option
        v-for="sk in options"
        :key="sk.id"
        :value="sk.id"
      >
        {{ sk.name }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.target-skeleton-selector {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
</style>
