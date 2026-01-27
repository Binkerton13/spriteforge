<template>
  <div class="task-panel">
    <h3>Tasks</h3>

    <div v-for="t in tasks.tasks" :key="t.id" class="task" :class="t.status">
      <div class="row">
        <span class="label">{{ t.label }}</span>
        <span class="status">{{ t.status }}</span>
      </div>

      <div class="progress-bar">
        <div class="progress" :style="{ width: t.progress + '%' }"></div>
      </div>

      <div v-if="t.error" class="error">{{ t.error }}</div>
    </div>
  </div>
</template>

<script setup>
import { useTaskStore } from '../stores/tasks'
const tasks = useTaskStore()
</script>

<style scoped>
.task-panel {
  background: var(--bg-2);
  padding: 16px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  max-height: 300px;
  overflow-y: auto;
}

.task {
  padding: 10px;
  margin-bottom: 12px;
  border-radius: var(--radius);
  background: var(--bg-1);
}

.task.done {
  border-left: 4px solid #4caf50;
}

.task.error {
  border-left: 4px solid #d32f2f;
}

.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.progress-bar {
  height: 6px;
  background: var(--bg-3);
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: var(--accent);
  transition: width 0.2s ease;
}

.error {
  margin-top: 6px;
  color: #d32f2f;
  font-size: 13px;
}
</style>
