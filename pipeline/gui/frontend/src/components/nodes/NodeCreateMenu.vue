<template>
  <div class="overlay" v-if="visible" @click.self="$emit('close')">
    <div class="menu">
      <input
        v-model="search"
        placeholder="Search nodes..."
        class="search"
      />

      <div class="list">
        <div
          v-for="n in filtered"
          :key="n"
          class="item"
          @click="choose(n)"
        >
          {{ n }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useWorkflowsStore } from '../../stores/workflows'

const props = defineProps({
  visible: Boolean,
  position: Object
})

const emit = defineEmits(['close', 'create'])

const search = ref('')
const store = useWorkflowsStore()

const filtered = computed(() =>
  store.availableNodeTypes.filter(n =>
    n.toLowerCase().includes(search.value.toLowerCase())
  )
)

function choose(type) {
  emit('create', type)
  search.value = ''
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.menu {
  margin-top: 80px;
  background: var(--bg-2);
  padding: 16px;
  border-radius: var(--radius);
  width: 300px;
  border: 1px solid var(--border);
}

.search {
  width: 100%;
  padding: 8px;
  margin-bottom: 12px;
  background: var(--bg-1);
  border: 1px solid var(--border);
  color: var(--fg-0);
  border-radius: var(--radius);
}

.list {
  max-height: 300px;
  overflow-y: auto;
}

.item {
  padding: 8px;
  border-radius: var(--radius);
  cursor: pointer;
}

.item:hover {
  background: var(--bg-3);
}
</style>
