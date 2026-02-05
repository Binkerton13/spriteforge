<template>
    <div class="model-page">

      <div class="header">
        <h2>Model Manager</h2>

        <ModelUploadButton @uploaded="reloadModels" />
      </div>

      <ModelTypeTabs
        :types="modelTypes"
        :activeType="activeType"
        @select="setActiveType"
      />

      <div class="content">

        <!-- LEFT: Model List -->
        <ModelList
          :models="filteredModels"
          :activeModel="activeModel"
          @select="setActiveModel"
          @delete="deleteModel"
        />

        <!-- RIGHT: Active Model Selector -->
        <ModelActiveSelector
          :activeModel="activeModel"
          :models="filteredModels"
          @set-active="setActiveModel"
        />

      </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import ModelList from '../components/ModelList.vue'
import ModelActiveSelector from '../components/ModelActiveSelector.vue'
import ModelUploadButton from '../components/ModelUploadButton.vue'
import ModelTypeTabs from '../components/ModelTypeTabs.vue'

import { useModelsStore } from '../stores/models'
import { useProjectsStore } from '../stores/projects'
import { useNotifyStore } from '../stores/notify'

/* STORES */
const modelsStore = useModelsStore()
const projects = useProjectsStore()
const notify = useNotifyStore()

/* LOCAL STATE */
const activeType = ref('render')  // default category

/* MODEL TYPES */
const modelTypes = [
  { id: 'render', label: 'Render Models' },
  { id: 'motion', label: 'Motion Models' },
  { id: 'style', label: 'Style Models' },
  { id: 'ipadapter', label: 'IP Adapters' },
  { id: 'lora', label: 'LoRA Models' },
]

/* COMPUTED */
const filteredModels = computed(() => {
  return modelsStore.models.filter(m => m.type === activeType.value)
})

const activeModel = computed(() => modelsStore.activeModel)

/* ACTIONS */
function setActiveType(type) {
  activeType.value = type
}

async function reloadModels() {
  await modelsStore.loadModels()
}

async function setActiveModel(model) {
  await modelsStore.setActive(model)
  notify.success(`Active model set to ${model}`)
}

async function deleteModel(name) {
  await modelsStore.remove(name)
  notify.success(`Deleted model: ${name}`)
}

/* INITIAL LOAD */
onMounted(async () => {
  projects.ensureLoaded()
  await modelsStore.loadModels()
})
</script>

<style scoped>
.model-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.content {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 20px;
}
</style>
