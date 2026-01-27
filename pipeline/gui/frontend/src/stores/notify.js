import { defineStore } from 'pinia'

export const useNotifyStore = defineStore('notify', {
  state: () => ({
    toasts: []
  }),

  actions: {
    push(type, message, timeout = 3000) {
      const id = Date.now() + Math.random()
      this.toasts.push({ id, type, message })

      setTimeout(() => {
        this.toasts = this.toasts.filter(t => t.id !== id)
      }, timeout)
    },

    success(msg) { this.push('success', msg) },
    error(msg) { this.push('error', msg, 5000) },
    warn(msg) { this.push('warn', msg, 4000) },
    info(msg) { this.push('info', msg) }
  }
})
