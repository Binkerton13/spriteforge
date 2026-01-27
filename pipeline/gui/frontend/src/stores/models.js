import { defineStore } from 'pinia'
import {
  fetchModelTypes,
  fetchModelsByType,
  fetchActiveModel,
  setActiveModel
} from '../api/models'
import { useNotifyStore } from './notify'

export const useModelsStore = defineStore('models', {
  state: () => ({
    types: [],
    models: [],
    activeType: '',
    activeModel: '',
    loading: false
  }),

  actions: {
    async loadTypes() {
      this.types = await fetchModelTypes()
      if (this.types.length) {
        this.activeType = this.types[0]
        await this.loadModels()
      }
    },

    async loadModels() {
      const notify = useNotifyStore()

      try {
        this.loading = true
        this.models = await fetchModelsByType(this.activeType)
        this.activeModel = (await fetchActiveModel()).model
      } catch (err) {
        notify.error("Failed to load models")
      } finally {
        this.loading = false
      }
    },

    async setActive(model) {
      const notify = useNotifyStore()

      try {
        this.activeModel = model
        await setActiveModel(model)
        notify.success(`Active model set to ${model}`)
      } catch (err) {
        notify.error("Failed to set active model")
      }
    }
  }
})
