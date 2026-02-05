<script setup>
defineProps({
  presets: Array,
  selected: Object
})

defineEmits(['select'])
</script>

<template>
  <div class="preset-dropdown">
    <label>Preset</label>
    <select
      :value="selected?.id || ''"
      @change="$emit('select', $event.target.value)"
    >
      <option value="">Select a preset</option>
      <option
        v-for="p in presets"
        :key="p.id"
        :value="p.id"
      >
        {{ p.name }}
      </option>
    </select>
  </div>
</template>
