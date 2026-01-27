import { defineStore } from 'pinia'

export const useWorkflowsStore = defineStore('workflows', {
  state: () => ({
    nodes: [],                 // graph nodes
    edges: [],                 // graph edges
    availableNodeTypes: [],    // for the creation menu
    selectedNode: null,        // for inspector
    loading: false,
    clipboard: null,

    // connection rules for validation
    connectionRules: {
      LoadImage: ["Resize", "GaussianBlur", "ColorCorrect", "Composite"],
      Resize: ["GaussianBlur", "ColorCorrect", "Composite"],
      GaussianBlur: ["ColorCorrect", "Composite"],
      ColorCorrect: ["Composite"],
      Composite: ["SaveImage"],
      SaveImage: []
    }
  }),

  actions: {
    // -------------------------------------------------------
    // Load available node types (static for now)
    // -------------------------------------------------------
    async loadNodeTypes() {
      this.availableNodeTypes = [
        "LoadImage",
        "SaveImage",
        "Resize",
        "GaussianBlur",
        "ColorCorrect",
        "Composite",
        "Render",
        "MotionToSprite",
        "SpriteToSheet"
      ]
    },

    // -------------------------------------------------------
    // Load workflow (graph-first)
    // -------------------------------------------------------
    loadWorkflow(data) {
      // data = { nodes: [...], edges: [...] }
      this.nodes = data.nodes
      this.edges = data.edges
    },

    // -------------------------------------------------------
    // Save workflow (graph-first)
    // -------------------------------------------------------
    saveWorkflow() {
      return {
        nodes: this.nodes,
        edges: this.edges
      }
    },

    // -------------------------------------------------------
    // Add a node (with status field)
    // -------------------------------------------------------
    addNode(node) {
      this.nodes.push({
        ...node,
        status: 'idle'   // idle | running | success | error
      })
    },
    // -------------------------------------------------------
    // Copy a node to clipboard
    // -------------------------------------------------------
    copyNode(id) {
      const node = this.nodes.find(n => n.id === id)
      if (node) {
        // Deep clone so edits don’t affect original
        this.clipboard = JSON.parse(JSON.stringify(node))
      }
    },
    // -------------------------------------------------------
    pasteNode(position) {
      if (!this.clipboard) return

      const newId = 'node_' + Date.now()

      const clone = {
        ...this.clipboard,
        id: newId,
        position: {
          x: position.x + 40, // offset so it doesn’t overlap
          y: position.y + 40
        },
        status: 'idle'
      }

      this.nodes.push(clone)
    },
    // -------------------------------------------------------
    // Add an edge
    // -------------------------------------------------------
    addEdge(edge) {
      this.edges.push(edge)
    },

    // -------------------------------------------------------
    // Remove a node + its edges
    // -------------------------------------------------------
    removeNode(id) {
      this.nodes = this.nodes.filter(n => n.id !== id)
      this.edges = this.edges.filter(e => e.source !== id && e.target !== id)
    },

    // -------------------------------------------------------
    // Remove an edge
    // -------------------------------------------------------
    removeEdge(id) {
      this.edges = this.edges.filter(e => e.id !== id)
    },

    // -------------------------------------------------------
    // Select a node for inspector
    // -------------------------------------------------------
    inspectNode(id) {
      this.selectedNode = this.nodes.find(n => n.id === id)
    },

    // -------------------------------------------------------
    // Validate connection (sourceType → targetType)
    // -------------------------------------------------------
    validateConnection(sourceType, targetType) {
      const allowed = this.connectionRules[sourceType] || []
      return allowed.includes(targetType)
    },

    // -------------------------------------------------------
    // Update node execution status
    // -------------------------------------------------------
    setNodeStatus(id, status) {
      const node = this.nodes.find(n => n.id === id)
      if (node) node.status = status
    }
  }
})
