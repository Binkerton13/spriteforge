<template>
  <div class="panel" v-if="url">
    <h3>Preview</h3>
    <img :src="url" style="max-width:100%;" />
  </div>
</template>

<script setup>
defineProps(['url'])
</script>
