import { defineStore } from 'pinia'
import { fetchProjects, loadProject, saveProject } from '../api/projects'
import { useNotifyStore } from './notify'

export const useProjectsStore = defineStore('projects', {
  state: () => ({
    list: [],
    currentId: null,
    metadata: {
      name: '',
      description: ''
    },
    assets: {
      motions: [],
      sprites: [],
      sheets: [],
      workflows: []
    },
    loading: false
  }),

  actions: {
    async loadList() {
      this.list = await fetchProjects()
    },

    async load(id) {
      const notify = useNotifyStore()

      try {
        this.loading = true
        const data = await loadProject(id)
        this.currentId = id
        this.metadata = data.metadata
        this.assets = data.assets
      } catch (err) {
        notify.error("Failed to load project")
      } finally {
        this.loading = false
      }
    },

    async save() {
      const tasks = useTaskStore()
      const notify = useNotifyStore()
      const taskId = tasks.add("Saving project")

      try {
        await saveProject({
          id: this.currentId,
          metadata: this.metadata,
          assets: this.assets
        })

        tasks.complete(taskId)
        notify.success("Project saved")
      } catch (err) {
        tasks.fail(taskId, "Project save failed")
        notify.error("Project save failed")
      }
    },

    createNew(name) {
      this.currentId = `project_${Date.now()}`
      this.metadata = { name, description: '' }
      this.assets = {
        motions: [],
        sprites: [],
        sheets: [],
        workflows: []
      }
    }
  }
})
