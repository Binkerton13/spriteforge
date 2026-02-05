<script setup>
defineProps({
  mode: String
})

defineEmits(['change'])
</script>

<template>
  <div class="mode-toggle">
    <button
      :class="{ active: mode === 'preset' }"
      @click="$emit('change', 'preset')"
    >
      Preset
    </button>

    <button
      :class="{ active: mode === 'prompt' }"
      @click="$emit('change', 'prompt')"
    >
      Prompt
    </button>
  </div>
</template>
