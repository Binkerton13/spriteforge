<template>
  <div class="page">
    <h1>Workflow Graph</h1>

    <VueFlow
      v-model:nodes="store.nodes"
      v-model:edges="store.edges"
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
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { VueFlow, Controls, MiniMap } from '@vue-flow/core'
import { useWorkflowsStore } from '../stores/workflows'
import WorkflowNode from '../components/nodes/WorkflowNode.vue'
import NodeCreateMenu from '../components/nodes/NodeCreateMenu.vue'
import { useNotifyStore } from '../stores/notify'

/* -------------------------------------------------------
   STORES + STATE
------------------------------------------------------- */
const store = useWorkflowsStore()
const notify = useNotifyStore()

const showMenu = ref(false)
const menuPos = ref({ x: 0, y: 0 })

// Tracks last clicked node for duplication
let lastClickedNode = null

/* -------------------------------------------------------
   INIT
------------------------------------------------------- */
onMounted(() => {
  store.loadNodeTypes()
  window.addEventListener('keydown', onKeyDown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeyDown)
})

/* -------------------------------------------------------
   CONNECTION VALIDATION
------------------------------------------------------- */
function onConnect(connection) {
  const sourceNode = store.nodes.find(n => n.id === connection.source)
  const targetNode = store.nodes.find(n => n.id === connection.target)

  if (!sourceNode || !targetNode) return

  const sourceType = sourceNode.data.type
  const targetType = targetNode.data.type

  const valid = store.validateConnection(sourceType, targetType)

  if (!valid) {
    notify.error(`Cannot connect ${sourceType} → ${targetType}`)
    return
  }

  store.addEdge({
    id: `${connection.source}-${connection.target}`,
    source: connection.source,
    target: connection.target
  })
}

/* -------------------------------------------------------
   RIGHT CLICK → OPEN NODE CREATION MENU
------------------------------------------------------- */
function onRightClick(event) {
  event.preventDefault()
  const bounds = event.target.getBoundingClientRect()
  menuPos.value = {
    x: event.clientX - bounds.left,
    y: event.clientY - bounds.top
  }
  showMenu.value = true
}

/* -------------------------------------------------------
   CREATE NODE
------------------------------------------------------- */
function createNode(type) {
  const id = 'node_' + Date.now()

  store.addNode({
    id,
    type: 'workflowNode',
    position: { x: menuPos.value.x, y: menuPos.value.y },
    data: {
      type,
      params: {},
      inputs: [],
      outputs: []
    }
  })

  showMenu.value = false
}

/* -------------------------------------------------------
   NODE CLICK → SELECT + EXECUTION PREVIEW
------------------------------------------------------- */
function onNodeClick(evt) {
  const id = evt.node.id
  lastClickedNode = id
  simulateExecution(id)
}

/* -------------------------------------------------------
   EXECUTION PREVIEW (DEMO)
------------------------------------------------------- */
function simulateExecution(nodeId) {
  store.setNodeStatus(nodeId, "running")

  setTimeout(() => {
    const ok = Math.random() > 0.2
    store.setNodeStatus(nodeId, ok ? "success" : "error")
  }, 1500)
}

/* -------------------------------------------------------
   KEYBOARD SHORTCUTS (COPY / PASTE)
------------------------------------------------------- */
function onKeyDown(e) {
  // COPY
  if (e.ctrlKey && e.key === 'c') {
    if (lastClickedNode) {
      store.copyNode(lastClickedNode)
      notify.info("Node copied")
    }
  }

  // PASTE
  if (e.ctrlKey && e.key === 'v') {
    const pos = { x: 300, y: 200 } // default paste location
    store.pasteNode(pos)
    notify.success("Node pasted")
  }
}
</script>

<style scoped>
.graph {
  height: calc(100vh - 80px);
  background: var(--bg-1);
  border-radius: var(--radius);
}
</style>
