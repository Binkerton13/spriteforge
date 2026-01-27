import { defineStore } from 'pinia'

export const useTaskStore = defineStore('tasks', {
  state: () => ({
    tasks: []  // { id, label, status, progress, started, finished, error }
  }),

  actions: {
    add(label) {
      const id = Date.now() + Math.random()
      this.tasks.push({
        id,
        label,
        status: 'running',
        progress: 0,
        started: Date.now(),
        finished: null,
        error: null
      })
      return id
    },

    update(id, data) {
      const task = this.tasks.find(t => t.id === id)
      if (task) Object.assign(task, data)
    },

    complete(id) {
      this.update(id, {
        status: 'done',
        progress: 100,
        finished: Date.now()
      })
    },

    fail(id, error) {
      this.update(id, {
        status: 'error',
        error,
        finished: Date.now()
      })
    }
  }
})
