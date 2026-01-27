<template>
  <div class="toast-container">
    <div
      v-for="t in notify.toasts"
      :key="t.id"
      class="toast"
      :class="t.type"
    >
      {{ t.message }}
    </div>
  </div>
</template>

<script setup>
import { useNotifyStore } from '../stores/notify'
const notify = useNotifyStore()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 9999;
}

.toast {
  padding: 12px 18px;
  border-radius: var(--radius);
  color: white;
  font-size: 14px;
  animation: fadeIn 0.2s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.4);
}

.success { background: #4caf50 }
.error { background: #d32f2f }
.warn { background: #ffa000 }
.info { background: #2196f3 }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-6px) }
  to { opacity: 1; transform: translateY(0) }
}
</style>
