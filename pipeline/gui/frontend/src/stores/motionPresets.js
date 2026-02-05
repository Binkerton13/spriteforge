import { defineStore } from 'pinia'
import {
  loadMotionPresets,
  saveAllMotionPresets,
  deleteMotionPreset
} from '../api/presets'

export const useMotionPresetsStore = defineStore('motionPresets', {
  state: () => ({
    presets: [],
    loaded: false
  }),

  actions: {
    async ensureLoaded() {
      if (this.loaded) return
      const data = await loadMotionPresets()
      this.presets = data.presets || []
      this.loaded = true
    },

    async saveAll() {
      await saveAllMotionPresets(this.presets)
    },

    async deletePreset(name) {
      this.presets = this.presets.filter(p => p.name !== name)
      await deleteMotionPreset(name)
    }
  }
})
