<template>
  <div class="topbar">
    <div class="left">
      <span class="label">Model:</span>
      <span class="value">{{ models.activeModel || "None" }}</span>

      <span class="label" style="margin-left:20px;">Project:</span>
      <span class="value">{{ projects.metadata.name || "None" }}</span>
    </div>

    <div class="right">
      <span
        class="status"
        :class="health.online ? 'online' : 'offline'"
      ></span>
      <span class="label">
        {{ health.online ? "Online" : "Offline" }}
      </span>
    </div>
    <div class="right">
      <span
        class="status"
        :class="health.online ? 'online' : 'offline'"
      ></span>

      <button class="settings-btn" @click="openSettings = true">⚙</button>
    </div>
    <SettingsModal :visible="openSettings" @close="openSettings = false" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useModelsStore } from '../stores/models'
import { useProjectsStore } from '../stores/projects'
import { useHealthStore } from '../stores/health'
import SettingsModal from '../components/SettingsModal.vue'

const models = useModelsStore()
const projects = useProjectsStore()
const health = useHealthStore()

const openSettings = ref(false)

onMounted(() => {
  health.startPolling()
})
</script>


<style scoped>
.topbar {
  height: 48px;
  background: var(--bg-2);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.label {
  color: var(--fg-muted);
  margin-right: 6px;
}

.value {
  color: var(--fg-0);
  font-weight: 500;
}

.status {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
  display: inline-block;
}

.online {
  background: #4caf50;
  box-shadow: 0 0 6px #4caf50;
}

.offline {
  background: #d32f2f;
  box-shadow: 0 0 6px #d32f2f;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--fg-muted);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.flash {
  animation: flash 0.3s ease;
}

@keyframes flash {
  0% { background: var(--accent); }
  100% { background: var(--bg-2); }
}

.settings-btn {
  background: transparent;
  border: none;
  color: var(--fg-0);
  font-size: 18px;
  cursor: pointer;
  margin-left: 12px;
}
.settings-btn:hover {
  color: var(--accent);
}

</style>
