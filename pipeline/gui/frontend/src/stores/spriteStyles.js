// src/stores/spriteStyles.js
import { defineStore } from 'pinia'

export const useSpriteStylesStore = defineStore('spriteStyles', {
  state: () => ({
    spriteStyles: [],
    loading: false,
  }),

  actions: {
    async loadDefaultStyles() {
      this.spriteStyles = [
        { name: 'Pixel Art', detail: 'Low-res, crisp pixel edges' },
        { name: 'Anime', detail: 'Clean lines, cel shading' },
        { name: 'Painterly', detail: 'Soft brush strokes, textured' },
      ]
    },

    ensureLoaded() {
      if (!this.spriteStyles.length) this.loadDefaultStyles()
    }
  }
})
