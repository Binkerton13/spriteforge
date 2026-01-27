<template>
  <div class="overlay" v-if="visible">
    <div class="modal">
      <h2>Settings</h2>

      <div class="section">
        <label>Theme</label>
        <select v-model="settings.theme" @change="save">
          <option value="dark">Dark</option>
          <option value="light">Light</option>
        </select>
      </div>

      <div class="section">
        <label>Default Model</label>
        <input v-model="settings.defaultModel" @input="save" />
      </div>

      <div class="section">
        <label>Default Resolution</label>
        <input type="number" v-model="settings.defaultResolution" @input="save" />
      </div>

      <div class="section">
        <label>
          <input type="checkbox" v-model="settings.showGrid" @change="save" />
          Show Grid in Editors
        </label>
      </div>

      <div class="section">
        <label>
          <input type="checkbox" v-model="settings.autoSaveProjects" @change="save" />
          Auto‑save Projects
        </label>
      </div>

      <div class="actions">
        <button @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from '../stores/settings'

const props = defineProps(['visible'])
const settings = useSettingsStore()

function save() {
  settings.save()
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: var(--bg-2);
  padding: 20px;
  border-radius: var(--radius);
  width: 400px;
}
.section {
  margin-bottom: 16px;
}
.actions {
  margin-top: 20px;
  text-align: right;
}
</style>
