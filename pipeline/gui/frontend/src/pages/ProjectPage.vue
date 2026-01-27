<template>
  <div class="page">
    <h1>Projects</h1>

    <div class="grid">
      <div class="left">
        <ProjectList
          :list="store.list"
          :selected="store.currentId"
          @select="store.load"
          @create="showCreate = true"
        />
      </div>

      <div class="right" v-if="store.currentId">
        <ProjectMetadataEditor :model="store" />
        <ProjectAssetList :assets="store.assets" />

        <button class="save" @click="store.save">Save Project</button>
      </div>
    </div>

    <ProjectCreateModal
      :visible="showCreate"
      @cancel="showCreate = false"
      @create="createProject"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProjectsStore } from '../stores/projects'

import ProjectList from '../components/ProjectList.vue'
import ProjectCreateModal from '../components/ProjectCreateModal.vue'
import ProjectMetadataEditor from '../components/ProjectMetadataEditor.vue'
import ProjectAssetList from '../components/ProjectAssetList.vue'

const store = useProjectsStore()
const showCreate = ref(false)

function createProject(name) {
  store.createNew(name)
  showCreate.value = false
}

onMounted(() => {
  store.loadList()
})
</script>

<style scoped>
.page {
  padding: 24px;
  min-height: 100vh;
  background: var(--bg-0);
  color: var(--fg-0);
}

.grid {
  display: flex;
  gap: 20px;
}
.left {
  width: 250px;
}
.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.save {
  background: #0e639c;
  padding: 10px 16px;
  border-radius: 4px;
  color: white;
}
</style>
