<template>
  <div class="overlay" v-if="visible">
    <div class="modal">
      <h2>Create Project</h2>

      <input v-model="name" placeholder="Project name" />

      <div class="actions">
        <button @click="$emit('cancel')">Cancel</button>
        <button @click="create">Create</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps(['visible'])
const emit = defineEmits(['create', 'cancel'])

const name = ref('')

function create() {
  emit('create', name.value)
  name.value = ''
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: #2d2d30;
  padding: 20px;
  border-radius: 6px;
  width: 300px;
}
.actions {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
}
button {
  background: #0e639c;
  padding: 8px 16px;
  border-radius: 4px;
  color: white;
}
</style>
