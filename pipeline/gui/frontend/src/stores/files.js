import { defineStore } from 'pinia'
import { listFiles, uploadFile} from '../api/files'

export const useFilesStore = defineStore('files', {
  state: () => ({
    currentPath: '',
    items: [],
    selected: null,
    previewUrl: null,
    loading: false
  }),

  actions: {
    async load(path = '') {
      this.loading = true
      this.currentPath = path
      const data = await listFiles(path)
      this.items = data.items
      this.loading = false

      // Re-select item if possible (after reload)
      if (this.selected) {
        const match = this.items.find(i =>
          (i.path && this.selected.path && i.path === this.selected.path) ||
          (i.name && this.selected.name && i.name === this.selected.name)
        )
        if (match) this.selected = match
      }
    },

    async upload(file) {
      // Upload file to backend
      await uploadFile(this.currentPath, file)

      // Reload directory
      await this.load(this.currentPath)

      // After reload, select the uploaded file by name
      const match = this.items.find(i => i.name === file.name)
      if (match) this.select(match)
    },

    async remove(item) {
      await deleteFile(item.path)
      await this.load(this.currentPath)
    },

    select(item) {
      this.selected = item

      // Only generate preview for real files on disk
      if (item.is_file && item.path) {
        this.previewUrl = `/api/files/preview?path=${encodeURIComponent(item.path)}`
      } else {
        this.previewUrl = null
      }
    }
  }
})
