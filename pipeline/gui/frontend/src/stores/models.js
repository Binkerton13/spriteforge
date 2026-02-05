// src/stores/models.js
import { defineStore } from 'pinia'
import {
  listModels,
  uploadModel,
  deleteModel,
  setActiveModel
} from '../api/models'

export const useModelsStore = defineStore('models', {
  state: () => ({
    models: [],
    activeModel: null,
    loading: false,
  }),

  actions: {
    async loadModels() {
      this.loading = true
      const data = await listModels()
      this.models = data.models || []
      this.activeModel = data.active || null
      this.loading = false
    },

    async upload(formData) {
      await uploadModel(formData)
      await this.loadModels()
    },

    async remove(name) {
      await deleteModel(name)
      await this.loadModels()
    },

    async setActive(model) {
      await setActiveModel(model)
      this.activeModel = model
    }
  }
})
