<template>
  <div class="node" :class="data.status">
    <div class="header">{{ data.type }}</div>

    <div class="body">
      <div
        v-for="(value, key) in data.params"
        :key="key"
        class="param"
      >
        <label>{{ key }}</label>
        <input v-model="data.params[key]" />
      </div>
    </div>

    <div class="ports">
      <div class="inputs">
        <div
          v-for="input in data.inputs"
          :key="input"
          class="port input-port"
        ></div>
      </div>

      <div class="outputs">
        <div
          v-for="output in data.outputs"
          :key="output"
          class="port output-port"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  id: String,
  data: Object
})
</script>

<style scoped>
.node {
  width: 200px;
  background: var(--bg-2);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: 0 2px 6px rgba(0,0,0,0.4);
  overflow: hidden;
  font-size: 13px;
}

.header {
  background: var(--accent);
  color: white;
  padding: 8px;
  font-weight: 600;
  text-align: center;
}

.body {
  padding: 10px;
}

.param {
  margin-bottom: 8px;
}

.param label {
  display: block;
  margin-bottom: 4px;
  color: var(--fg-muted);
}

.param input {
  width: 100%;
  background: var(--bg-1);
  border: 1px solid var(--border);
  color: var(--fg-0);
  padding: 4px;
  border-radius: var(--radius);
}

.ports {
  display: flex;
  justify-content: space-between;
  padding: 6px;
}

.port {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.input-port {
  background: #4fc3f7;
}

.output-port {
  background: #ffb74d;
}
.node.running {
  box-shadow: 0 0 12px #42a5f5;
  border-color: #42a5f5;
}

.node.success {
  border-color: #4caf50;
}

.node.error {
  border-color: #d32f2f;
}

</style>
