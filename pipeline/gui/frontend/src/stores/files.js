import { defineStore } from 'pinia'
import { listFiles, uploadFile, deleteFile } from '../api/files'

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
    },

    async upload(file) {
      await uploadFile(this.currentPath, file)
      await this.load(this.currentPath)
    },

    async remove(item) {
      await deleteFile(item.path)
      await this.load(this.currentPath)
    },

    select(item) {
      this.selected = item
      this.previewUrl = item.is_file ? `/api/files/preview?path=${encodeURIComponent(item.path)}` : null
    }
  }
})
