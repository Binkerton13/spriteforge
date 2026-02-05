// src/stores/projects.js
import { defineStore } from 'pinia'
import { listProjects, createProject, loadProject, updateProject } from '../api/projects'

export const useProjectsStore = defineStore('projects', {
  state: () => ({
    projects: [],
    activeProject: null,
    activeProjectId: null,
    loading: false,
  }),

  actions: {
    async loadProjects() {
      this.loading = true
      const data = await listProjects()
      this.projects = data.projects || []
      this.loading = false
    },

    async selectProject(project_id) {
      const data = await loadProject(project_id)
      this.activeProject = data.project || null
      this.activeProjectId = project_id
    },

    async create(name) {
      const data = await createProject(name)
      await this.loadProjects()
      return data
    },

    async update(metadata) {
      if (!this.activeProjectId) return
      await updateProject(this.activeProjectId, metadata)
      await this.selectProject(this.activeProjectId)
    },

    ensureLoaded() {
      if (!this.projects.length) this.loadProjects()
    }
  }
})
