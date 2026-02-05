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
  background: linear-gradient(
    135deg,
    var(--bg-2),
    rgba(61, 218, 215, 0.04),
    rgba(138, 79, 255, 0.04)
  );
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
  border-left: 4px solid var(--accent-active);
  transition: border-color var(--transition), box-shadow var(--transition);
}

.task.done {
  border-left-color: var(--accent-green);
  box-shadow: var(--glow-green);
}

.task.error {
  border-left-color: var(--accent-orange-deep);
  box-shadow: var(--glow-orange-deep);
}

.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  color: var(--fg-0);
}

.progress-bar {
  height: 6px;
  background: var(--bg-3);
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: var(--accent-active);
  transition: width 0.2s ease, background var(--transition);
  box-shadow: var(--glow);
}

.error {
  margin-top: 6px;
  color: var(--accent-orange-deep);
  font-size: 13px;
  text-shadow: var(--glow-orange-deep);
}

</style>
