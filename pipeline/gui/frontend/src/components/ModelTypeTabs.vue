<template>
  <div class="tabs">
    <div
      v-for="t in types"
      :key="t"
      class="tab"
      :class="{ active: t === activeType }"
      @click="$emit('select', t)"
    >
      {{ t }}
    </div>
  </div>
</template>

<script setup>
defineProps(['types', 'activeType'])
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.tab {
  padding: 8px 16px;
  background: #2d2d30;
  border-radius: 4px;
  cursor: pointer;
}
.tab.active {
  background: #0e639c;
}
</style>
