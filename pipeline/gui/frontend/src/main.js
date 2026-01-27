import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import './theme.css'

import { registerShortcuts } from './shortcuts'

// Stores
import { useMotionStore } from './stores/motion'
import { useSpritesStore } from './stores/sprites'
import { useModelsStore } from './stores/models'
import { useWorkflowsStore } from './stores/workflows'
import { useProjectsStore } from './stores/projects'
import { useFilesStore } from './stores/files'
import { useSettingsStore } from './stores/settings'

const app = createApp(App)
const pinia = createPinia()
const settings = useSettingsStore()
settings.load()

app.use(pinia)
app.use(router)

// Register stores globally for shortcuts
app.config.globalProperties.$motion = useMotionStore()
app.config.globalProperties.$sprites = useSpritesStore()
app.config.globalProperties.$models = useModelsStore()
app.config.globalProperties.$workflows = useWorkflowsStore()
app.config.globalProperties.$projects = useProjectsStore()
app.config.globalProperties.$files = useFilesStore()

// Register global keyboard shortcuts
registerShortcuts(app)

app.mount('#app')

watch(() => settings.theme, (theme) => {
  document.documentElement.classList.toggle('light', theme === 'light')
})
