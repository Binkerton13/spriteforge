// src/stores/sprites.js
import { defineStore } from 'pinia'
import { runSpriteWorkflow } from '../api/sprites'

export const useSpritesStore = defineStore('sprites', {
  state: () => ({
    frames: [],
    sheet: null,
    history: [],
    generating: false,
  }),

  actions: {
    reset() {
      this.frames = []
      this.sheet = null
    },

    async generate(payload) {
      this.generating = true
      const data = await runSpriteWorkflow(payload)
      this.generating = false

      this.frames = data.frames || []
      this.sheet = data.sheet || null

      this.history.unshift({
        timestamp: Date.now(),
        payload,
        frames: this.frames,
        sheet: this.sheet,
      })

      return data
    },

    loadHistory(entry) {
      this.frames = entry.frames
      this.sheet = entry.sheet
    }
  }
})
