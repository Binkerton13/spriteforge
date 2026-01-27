<template>
  <div class="panel">
    <h2>Workflows</h2>

    <div class="list">
      <div
        v-for="w in list"
        :key="w"
        class="item"
        :class="{ active: w === selected }"
        @click="$emit('select', w)"
      >
        {{ w }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['list', 'selected'])
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
