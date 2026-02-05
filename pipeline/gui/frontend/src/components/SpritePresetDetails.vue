<template>
  <div class="sprite-preset-details">

    <!-- NAME -->
    <div class="section">
      <label>Name</label>
      <input
        type="text"
        v-model="localName"
        @input="$emit('update:name', localName)"
      />
    </div>

    <!-- PROMPT -->
    <div class="section">
      <label>Prompt</label>
      <textarea
        v-model="localPrompt"
        @input="$emit('update:prompt', localPrompt)"
      ></textarea>
    </div>

    <!-- STYLE -->
    <div class="section">
      <label>Style</label>
      <StyleSelector
        :styles="spriteStyles"
        :selected="preset.style"
        @select="style => $emit('update:style', style)"
      />
    </div>

    <!-- SETTINGS -->
    <div class="section">
      <label>Render Settings</label>
      <SegmentViewer
        :label="'Settings'"
        :value="preset.settings"
        @update="val => $emit('update:settings', val)"
      />
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useSpriteStylesStore } from '@/stores/spriteStyles'
import StyleSelector from '@/components/StyleSelector.vue'
import SegmentViewer from '@/components/SegmentViewer.vue'

const props = defineProps({
  preset: Object,
})

const spriteStylesStore = useSpriteStylesStore()
const spriteStyles = spriteStylesStore.spriteStyles

const localName = ref(props.preset.name)
const localPrompt = ref(props.preset.prompt)

watch(() => props.preset.name, v => localName.value = v)
watch(() => props.preset.prompt, v => localPrompt.value = v)
</script>

<style scoped>
/* consistent with PresetDetails.vue */
</style>
