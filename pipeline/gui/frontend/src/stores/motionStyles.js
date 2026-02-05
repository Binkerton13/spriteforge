// src/stores/motionStyles.js
import { defineStore } from 'pinia'

export const useMotionStylesStore = defineStore('motionStyles', {
  state: () => ({
    styles: [],
    loading: false,
  }),

  actions: {
    async loadDefaultStyles() {
      // Hardcoded defaults for now — can be loaded from backend later
      this.styles = [
        { name: 'Natural', description: 'Smooth, realistic motion' },
        { name: 'Exaggerated', description: 'Cartoon-like, expressive motion' },
        { name: 'Mechanical', description: 'Rigid, robotic motion' },
      ]
    },

    ensureLoaded() {
      if (!this.styles.length) this.loadDefaultStyles()
    }
  }
})
