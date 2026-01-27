<template>
  <div class="layout">
    <Sidebar />

    <div class="main">
      <TopBar />
      <div class="content">
        <router-view />
      </div>
    </div>
    <div class="content">
      <router-view />
      <TaskQueue />
    </div>
  </div>
</template>

<script setup>
import Sidebar from './Sidebar.vue'
import TopBar from './TopBar.vue'
import TaskQueue from '../components/TaskQueue.vue'
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  background: #1e1e1e;
  color: #ddd;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>
