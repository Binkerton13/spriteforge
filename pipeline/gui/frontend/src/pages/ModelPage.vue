<template>
  <div class="page">
    <h1>Model Manager</h1>

    <ModelUploadButton />

    <ModelTypeTabs
      :types="store.types"
      :activeType="store.activeType"
      @select="t => { store.activeType = t; store.loadModels() }"
    />

    <ModelList
      :models="store.models"
      :activeModel="store.activeModel"
      @select="m => store.setActive(m)"
    />

    <ModelActiveSelector :model="store.activeModel" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useModelsStore } from '../stores/models'

import ModelTypeTabs from '../components/ModelTypeTabs.vue'
import ModelList from '../components/ModelList.vue'
import ModelActiveSelector from '../components/ModelActiveSelector.vue'
import ModelUploadButton from '../components/ModelUploadButton.vue'

const store = useModelsStore()

onMounted(() => {
  store.loadTypes()
})
</script>

<style scoped>
.page {
  padding: 24px;
  min-height: 100vh;
  background: var(--bg-0);
  color: var(--fg-0);
}

</style>
