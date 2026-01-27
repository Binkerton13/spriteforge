<template>
  <div class="panel">
    <h2>Assets</h2>

    <div class="section" v-for="(items, key) in assets" :key="key">
      <h3>{{ key }}</h3>
      <ul>
        <li v-for="i in items" :key="i">{{ i }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps(['assets'])
</script>

<style scoped>
.section {
  margin-bottom: 15px;
}
h3 {
  color: #4fc3f7;
}
</style>
