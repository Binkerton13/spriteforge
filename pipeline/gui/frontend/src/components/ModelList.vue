<template>
  <div class="panel">
    <h2>Models</h2>

    <div class="list">
      <div
        v-for="m in models"
        :key="m"
        class="item"
        :class="{ active: m === activeModel }"
        @click="$emit('select', m)"
      >
        {{ m }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['models', 'activeModel'])
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

</style>
