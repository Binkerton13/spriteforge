import { defineStore } from 'pinia'
import { fetchPresets, generateMotion, fetchFrames, previewVideoUrl } from '../api/motion'
import { useNotifyStore } from './notify'
import { useTaskStore } from './tasks'

export const useMotionStore = defineStore('motion', {
  state: () => ({
    presets: [],
    selectedPreset: '',
    seed: 1234,
    frames: [],
    videoUrl: null,
    loading: false
  }),

  actions: {
    async loadPresets() {
      this.presets = await fetchPresets()
    },

    async runGeneration() {
      const tasks = useTaskStore()
      const notify = useNotifyStore()
      const taskId = tasks.add("Generating motion")

      try {
        this.loading = true
        await generateMotion({
          preset: this.selectedPreset,
          seed: this.seed
        })

        tasks.update(taskId, { progress: 70 })

        this.videoUrl = previewVideoUrl()
        this.frames = await fetchFrames()

        tasks.complete(taskId)
        notify.success("Motion generated successfully")
      } catch (err) {
        tasks.fail(taskId, "Motion generation failed")
        notify.error("Motion generation failed")
      } finally {
        this.loading = false
      }
    }
  }
})
