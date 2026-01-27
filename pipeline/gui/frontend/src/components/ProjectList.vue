<template>
  <div class="panel">
    <h2>Projects</h2>

    <button class="create" @click="$emit('create')">New Project</button>

    <div class="list">
      <div
        v-for="p in list"
        :key="p.id"
        class="item"
        :class="{ active: p.id === selected }"
        @click="$emit('select', p.id)"
      >
        {{ p.name }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['list', 'selected'])
</script>

<style scoped>
.create {
  background: #0e639c;
  padding: 8px 16px;
  border-radius: 4px;
  color: white;
  margin-bottom: 10px;
}
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
