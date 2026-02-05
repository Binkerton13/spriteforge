<script setup>
defineProps({
  skeleton: String,
  options: Array
})

defineEmits(['change'])
</script>

<template>
  <div class="skeleton-selector">
    <label>Skeleton</label>
    <select :value="skeleton" @change="$emit('change', $event.target.value)">
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
