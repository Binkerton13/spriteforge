import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    theme: 'dark',
    defaultModel: '',
    defaultResolution: 512,
    showGrid: true,
    autoSaveProjects: true
  }),

  actions: {
    load() {
      const saved = localStorage.getItem('spriteforge_settings')
      if (saved) {
        Object.assign(this, JSON.parse(saved))
      }
    },

    save() {
      localStorage.setItem('spriteforge_settings', JSON.stringify(this.$state))
    },

    update(key, value) {
      this[key] = value
      this.save()
    }
  }
})
