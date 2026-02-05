<template>
  <div
    v-if="visible"
    class="node-menu"
    :style="{ top: position.y + 'px', left: position.x + 'px' }"
    @click.stop
  >
    <div class="menu-header">
      <strong>Create Node</strong>
      <button class="close-btn" @click="$emit('close')">✕</button>
    </div>

    <div class="menu-list">
      <div
        v-for="node in nodeTypes"
        :key="node.type"
        class="menu-item"
        @click="select(node.type)"
      >
        {{ node.label }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

/* PROPS */
const props = defineProps({
  visible: Boolean,
  position: { type: Object, default: () => ({ x: 0, y: 0 }) },
})

/* EMITS */
const emit = defineEmits(['close', 'create'])

/* NODE TYPES */
const nodeTypes = [
  { type: 'load_image', label: 'Load Image' },
  { type: 'load_motion', label: 'Load Motion' },
  { type: 'ip_adapter', label: 'IP Adapter' },
  { type: 'controlnet', label: 'ControlNet' },
  { type: 'render', label: 'Render Sprite' },
  { type: 'save_output', label: 'Save Output' },
]

/* ACTION */
function select(type) {
  emit('create', type)
  emit('close')
}
</script>

<style scoped>
.node-menu {
  position: absolute;
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 6px;
  padding: 8px;
  width: 180px;
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  animation: fadeIn 0.12s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}

.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 6px;
  border-bottom: 1px solid #333;
  margin-bottom: 6px;
}

.close-btn {
  background: none;
  border: none;
  color: #aaa;
  cursor: pointer;
  font-size: 14px;
}

.menu-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-item {
  padding: 6px 8px;
  border-radius: 4px;
  background: #2a2a2a;
  cursor: pointer;
  transition: background 0.15s;
}

.menu-item:hover {
  background: #3a3a3a;
}
</style>
