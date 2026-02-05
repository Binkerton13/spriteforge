import { defineStore } from 'pinia'

export const useSpritePresetsStore = defineStore('spritePresets', {
  state: () => ({
    presets: [],          // [{ id, name, prompt, settings, style }]
    selectedPresetId: null,
  }),

  getters: {
    selectedPreset(state) {
      return state.presets.find(p => p.id === state.selectedPresetId) || null
    }
  },

  actions: {
    loadPresets(list) {
      this.presets = list
    },

    setPreset(id) {
      this.selectedPresetId = id
    },

    createPreset() {
      const id = 'preset_' + Date.now()
      this.presets.push({
        id,
        name: 'New Sprite Preset',
        prompt: '',
        settings: {
          resolution: 512,
          variants: 1,
          seed: null,
          background: 'transparent',
          render_model: null,
        },
        style: null,
      })
      this.selectedPresetId = id
    },

    deletePreset(id) {
      this.presets = this.presets.filter(p => p.id !== id)
      if (this.selectedPresetId === id) this.selectedPresetId = null
    },

    updateName(name) {
      if (!this.selectedPreset) return
      this.selectedPreset.name = name
    },

    updateField(key, value) {
      if (!this.selectedPreset) return
      this.selectedPreset[key] = value
    },

    updateSettings(settings) {
      if (!this.selectedPreset) return
      this.selectedPreset.settings = { ...settings }
    },

    updateStyle(style) {
      if (!this.selectedPreset) return
      this.selectedPreset.style = style
    }
  }
})
