import { defineStore } from 'pinia'
import { pingBackend } from '../api/health'

export const useHealthStore = defineStore('health', {
  state: () => ({
    online: false,
    lastCheck: null
  }),

  actions: {
    async check() {
      this.online = await pingBackend()
      this.lastCheck = Date.now()
    },

    startPolling() {
      this.check()
      setInterval(() => this.check(), 5000)
    }
  }
})
