<template>
  <div class="prompt-editor">

    <!-- HEADER -->
    <div class="header">
      <h3>Prompt</h3>

      <button class="refine-btn" @click="$emit('refine-prompt')">
        Refine (AI)
      </button>
    </div>

    <!-- RAW PROMPT INPUT -->
    <textarea
      class="prompt-input"
      v-model="localPrompt"
      @input="emitPrompt"
      placeholder="Describe the motion or sprite you want to generate…"
    ></textarea>

    <!-- REFINED PROMPT (READ-ONLY) -->
    <div v-if="refinedPrompt" class="refined-block">
      <label>Refined Prompt</label>
      <textarea
        class="refined-input"
        :value="refinedPrompt"
        readonly
      ></textarea>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

/* PROPS */
const props = defineProps({
  prompt: { type: String, default: '' },
  refinedPrompt: { type: String, default: '' },
})

/* EMITS */
const emit = defineEmits(['update-prompt', 'refine-prompt'])

/* LOCAL STATE */
const localPrompt = ref(props.prompt)

/* WATCH FOR EXTERNAL CHANGES */
watch(
  () => props.prompt,
  v => localPrompt.value = v
)

/* EMITTER */
function emitPrompt() {
  emit('update-prompt', localPrompt.value)
}
</script>

<style scoped>
.prompt-editor {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100%;
  gap: 14px;
  background: #1a1a1a;
  border: 1px solid #333;
  padding: 14px;
  border-radius: 8px;
  color: #eee;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.refine-btn {
  padding: 6px 12px;
  background: #4b4b7a;
  border: none;
  border-radius: 4px;
  color: #eee;
  cursor: pointer;
}

.refine-btn:hover {
  background: #5a5a8a;
}

.prompt-input,
.refined-input {
  max-width: 100%;
  width: 100%;
  box-sizing: border-box;
  min-height: 100px;
  padding: 10px;
  border-radius: 6px;
  background: #111;
  border: 1px solid #444;
  color: #eee;
  font-family: monospace;
  resize: vertical;
}
.refined-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.refined-block label {
  font-size: 14px;
  opacity: 0.8;
}
</style>
