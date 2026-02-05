<template>
    <div class="project-page">

      <!-- HEADER -->
      <div class="header">
        <h2>Projects</h2>
        <button class="create-btn" @click="showCreateModal = true">
          New Project
        </button>
      </div>

      <div class="content">

        <!-- LEFT: PROJECT LIST -->
        <ProjectList
          :projects="projects"
          :activeProjectId="activeProjectId"
          @select="selectProject"
        />

        <!-- RIGHT: PROJECT DETAILS -->
        <div v-if="activeProject" class="details">

          <!-- METADATA EDITOR -->
          <ProjectMetadataEditor
            :project="activeProject"
            @update="updateMetadata"
          />

          <!-- ASSET LIST -->
          <ProjectAssetList
            :projectId="activeProjectId"
          />

        </div>

      </div>

      <!-- CREATE MODAL -->
      <ProjectCreateModal
        v-if="showCreateModal"
        @close="showCreateModal = false"
        @create="createProject"
      />

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import ProjectList from '../components/ProjectList.vue'
import ProjectCreateModal from '../components/ProjectCreateModal.vue'
import ProjectMetadataEditor from '../components/ProjectMetadataEditor.vue'
import ProjectAssetList from '../components/ProjectAssetList.vue'

import { useProjectsStore } from '../stores/projects'
import { useNotifyStore } from '../stores/notify'

/* STORES */
const projectsStore = useProjectsStore()
const notify = useNotifyStore()

/* LOCAL STATE */
const showCreateModal = ref(false)

/* COMPUTED */
const projects = computed(() => projectsStore.projects)
const activeProject = computed(() => projectsStore.activeProject)
const activeProjectId = computed(() => projectsStore.activeProjectId)

/* ACTIONS */
async function selectProject(project_id) {
  await projectsStore.selectProject(project_id)
}

async function createProject(name) {
  const res = await projectsStore.create(name)
  notify.success(`Project created: ${name}`)

  showCreateModal.value = false
  await projectsStore.loadProjects()
}

async function updateMetadata(metadata) {
  await projectsStore.update(metadata)
  notify.success('Project metadata updated')
}

/* INITIAL LOAD */
onMounted(async () => {
  await projectsStore.loadProjects()
})
</script>

<style scoped>
.project-page {
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

.create-btn {
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
}

.content {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 20px;
}

.details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
