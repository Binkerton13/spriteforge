<template>
  <div class="topbar">
    <div class="left">
      <span class="label">Model:</span>
      <span class="value">{{ models.activeModel || "None" }}</span>

      <span class="label" style="margin-left:20px;">Project:</span>
      <span class="value">{{ "None" }}</span>
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
  background: var(--accent-green);
  box-shadow: var(--glow-green);
  transition: background var(--transition), box-shadow var(--transition);
}

:deep(body.offline) .status {
  background: var(--accent-orange);
  box-shadow: var(--glow-orange);
}

.settings-btn {
  background: transparent;
  border: none;
  color: var(--fg-0);
  font-size: 18px;
  cursor: pointer;
  margin-left: 12px;
  transition: color var(--transition), text-shadow var(--transition);
}

.settings-btn:hover {
  color: var(--accent-active);
  text-shadow: var(--glow);
}

</style>
