import { defineStore } from 'pinia'
import {
  fetchStyles,
  fetchModels,
  generateSprites,
  assembleSheet,
  fetchFrames,
  sheetPreviewUrl
} from '../api/sprites'
import { useNotifyStore } from './notify'

export const useSpritesStore = defineStore('sprites', {
  state: () => ({
    styles: [],
    models: [],
    selectedStyle: '',
    selectedModel: '',
    resolution: 512,
    frames: [],
    sheetUrl: null,
    loading: false
  }),

  actions: {
    async loadInitial() {
      this.styles = await fetchStyles()
      this.models = await fetchModels()
    },

    async runGeneration() {
      const notify = useNotifyStore()
      const tasks = useTaskStore()
      const taskId = tasks.add("Generating sprites")

      try {
        this.loading = true
        await generateSprites({
          style: this.selectedStyle,
          model: this.selectedModel,
          resolution: this.resolution
        })

        tasks.update(taskId, { progress: 60 })

        this.frames = await fetchFrames()

        tasks.complete(taskId)
        notify.success("Sprites generated")
      } catch (err) {
        tasks.fail(taskId, "Sprite generation failed")
        notify.error("Sprite generation failed")
      } finally {
        this.loading = false
      }
    },

    async assemble() {
      const tasks = useTaskStore()
      const notify = useNotifyStore()
      const taskId = tasks.add("Assembling sprite sheet")

      try {
        this.loading = true
        await assembleSheet({ frames: this.frames })
        this.sheetUrl = sheetPreviewUrl()

        tasks.complete(taskId)
        notify.success("Sprite sheet assembled")
      } catch (err) {
        tasks.fail(taskId, "Failed to assemble sprite sheet")
        notify.error("Failed to assemble sprite sheet")
      } finally {
        this.loading = false
      }
    }
  }
})
