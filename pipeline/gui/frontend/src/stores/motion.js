// src/stores/motion.js
import { defineStore } from 'pinia'
import {
  suggestMotion,
  refineMotion,
  styleMotion,
  translateMotion
} from '../api/motion'

export const useMotionStore = defineStore('motion', {
  state: () => ({
    motions: [],
    selectedMotion: null,
    generating: false,
  }),

  actions: {
    async suggest(prompt, preset) {
      this.generating = true
      const data = await suggestMotion(prompt, preset)
      this.generating = false
      return data.motion
    },

    async refine(prompt, existing_motion) {
      const data = await refineMotion(prompt, existing_motion)
      return data.motion
    },

    async applyStyle(style, existing_motion) {
      const data = await styleMotion(style, existing_motion)
      return data.motion
    },

    async translate(existing_motion, target_language) {
      const data = await translateMotion(existing_motion, target_language)
      return data.motion
    },

    importMotion(fileObj) {
      this.motions.push(fileObj)
    },

    select(motion) {
      this.selectedMotion = motion
    }
  }
})
