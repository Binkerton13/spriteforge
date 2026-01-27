<template>
  <div class="panel" v-if="sheetUrl">
    <h2>Sprite Sheet</h2>
    <img :src="sheetUrl" style="max-width:100%;" />
  </div>
</template>

<script setup>
defineProps(['sheetUrl'])
</script>
