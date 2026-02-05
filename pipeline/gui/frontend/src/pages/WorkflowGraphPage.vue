<template>
    <div class="workflow-page">

      <div class="header">
        <h2>Workflow Graph</h2>

        <select v-model="selectedType" @change="loadWorkflow">
          <option value="sprite">Sprite Workflow</option>
          <option value="motion">Motion Workflow</option>
        </select>

        <button class="save-btn" @click="saveCurrentWorkflow">
          Save Workflow
        </button>
      </div>

      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        class="graph"
        :node-types="{ workflowNode: WorkflowNode }"
        :fit-view="true"
        @node-click="onNodeClick"
        @contextmenu="onRightClick"
        @connect="onConnect"
      >
        <Controls />
        <MiniMap />
      </VueFlow>

      <NodeCreateMenu
        :visible="showMenu"
        :position="menuPos"
        @close="showMenu = false"
        @create="createNode"
      />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'

import WorkflowNode from '../components/nodes/WorkflowNode.vue'
import NodeCreateMenu from '../components/nodes/NodeCreateMenu.vue'

import { useProjectsStore } from '../stores/projects'
import { useWorkflowStore } from '../stores/workflow'
import { useNotifyStore } from '../stores/notify'

/* STORES */
const projects = useProjectsStore()
const workflowStore = useWorkflowStore()
const notify = useNotifyStore()

/* LOCAL STATE */
const selectedType = ref('sprite')

const nodes = ref([])
const edges = ref([])

const showMenu = ref(false)
const menuPos = ref({ x: 0, y: 0 })

/* LOAD WORKFLOW */
async function loadWorkflow() {
  const project_id = projects.activeProjectId
  if (!project_id) return

  const wf = await workflowStore.load(selectedType.value, project_id)

  nodes.value = wf.nodes || []
  edges.value = wf.edges || []
}

/* SAVE WORKFLOW */
async function saveCurrentWorkflow() {
  const project_id = projects.activeProjectId
  if (!project_id) return

  const workflow = {
    nodes: nodes.value,
    edges: edges.value,
  }

  await workflowStore.save(selectedType.value, project_id, workflow)
  notify.success('Workflow saved')
}

/* NODE CREATION */
function onRightClick(event) {
  event.preventDefault()
  const bounds = event.target.getBoundingClientRect()

  menuPos.value = {
    x: event.clientX - bounds.left,
    y: event.clientY - bounds.top,
  }

  showMenu.value = true
}

function createNode(type) {
  const id = 'node_' + Date.now()

  nodes.value.push({
    id,
    type: 'workflowNode',
    position: { x: menuPos.value.x, y: menuPos.value.y },
    data: {
      type,
      params: {},
      inputs: [],
      outputs: [],
    },
  })

  showMenu.value = false
}

/* NODE CLICK */
function onNodeClick(evt) {
  notify.info(`Selected node: ${evt.node.id}`)
}

/* CONNECTION VALIDATION */
function onConnect(connection) {
  const sourceNode = nodes.value.find(n => n.id === connection.source)
  const targetNode = nodes.value.find(n => n.id === connection.target)

  if (!sourceNode || !targetNode) return

  const sourceType = sourceNode.data.type
  const targetType = targetNode.data.type

  // Basic validation — can be expanded later
  if (sourceType === targetType) {
    notify.error(`Cannot connect ${sourceType} → ${targetType}`)
    return
  }

  edges.value.push({
    id: `${connection.source}-${connection.target}`,
    source: connection.source,
    target: connection.target,
  })
}

/* INITIAL LOAD */
onMounted(async () => {
  projects.ensureLoaded()
  await loadWorkflow()
})
</script>

<style scoped>
.workflow-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px;
  gap: 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.graph {
  flex: 1;
  background: var(--bg-1);
  border-radius: var(--radius);
}
</style>
