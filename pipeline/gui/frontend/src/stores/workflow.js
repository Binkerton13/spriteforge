// src/stores/workflow.js
import { defineStore } from 'pinia'
import { loadWorkflow, saveWorkflow } from '../api/workflows'

export const useWorkflowStore = defineStore('workflow', {
  state: () => ({
    workflows: {},
    loading: false,
  }),

  actions: {
    async load(type, project_id) {
      this.loading = true
      const data = await loadWorkflow(type, project_id)
      this.workflows[type] = data.workflow || {}
      this.loading = false
      return this.workflows[type]
    },

    async save(type, project_id, workflow) {
      await saveWorkflow(type, project_id, workflow)
      this.workflows[type] = workflow
    }
  }
})
