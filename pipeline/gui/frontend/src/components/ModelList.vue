<template>
  <div class="panel">
    <h2>Models</h2>

    <div class="list">
      <div
        v-for="m in models"
        :key="m"
        class="item"
        :class="{ active: m === active }"
        @click="$emit('select', m)"
      >
        {{ m }}
      </div>

      <div v-if="models.length === 0" class="empty">
        No models found for this type.
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  models: { type: Array, required: true },
  active: { type: String, required: false }
})
</script>

<style scoped>
.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item {
  padding: 10px;
  background: #252526;
  border-radius: 4px;
  cursor: pointer;
}

.item.active {
  background: #0e639c;
}

.item:hover {
  background: var(--bg-3);
}

.empty {
  opacity: 0.6;
  font-style: italic;
  padding: 10px;
}
</style>
