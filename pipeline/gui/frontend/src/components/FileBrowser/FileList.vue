<template>
  <div class="panel">
    <h3>Files</h3>

    <div class="list">
      <div
        v-for="item in items"
        :key="item.path || item.name || item"
        class="item"
        :class="{ active: isActive(item) }"
        @click="$emit('select', item)"
        @dblclick="open(item)"
      >
        <span>{{ item.name || item.path || item }}</span>

        <button class="delete" @click.stop="$emit('delete', item)">✕</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['items', 'selected'])
const emit = defineEmits(['select', 'open', 'delete'])

function open(item) {
  if (item.is_dir) emit('open', item.path)
}

function isActive(item) {
  if (item === props.selected) return true

  if (item?.path && props.selected?.path)
    return item.path === props.selected.path

  if (item?.name && props.selected?.name)
    return item.name === props.selected.name

  return false
}
</script>

<style scoped>
.list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.item {
  padding: 8px;
  background: var(--bg-1);
  border-radius: var(--radius);
  display: flex;
  justify-content: space-between;
  cursor: pointer;
}
.item.active {
  background: var(--accent);
}
.delete {
  background: transparent;
  color: var(--fg-muted);
  border: none;
  cursor: pointer;
}
</style>
