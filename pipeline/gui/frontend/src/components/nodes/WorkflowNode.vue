<template>
  <div class="workflow-node">

    <!-- NODE HEADER -->
    <div class="header">
      <strong>{{ data.type }}</strong>
    </div>

    <!-- PARAMETER EDITOR -->
    <div class="params">
      <div
        v-for="(value, key) in data.params"
        :key="key"
        class="param-row"
      >
        <label>{{ key }}</label>
        <input
          type="text"
          v-model="localParams[key]"
          @input="emitParams"
        />
      </div>

      <!-- Add new param -->
      <div class="add-param">
        <input
          v-model="newParamKey"
          placeholder="param name"
        />
        <input
          v-model="newParamValue"
          placeholder="value"
        />
        <button @click="addParam">+</button>
      </div>
    </div>

    <!-- INPUT PORTS -->
    <div class="ports inputs">
      <div
        v-for="(input, index) in data.inputs"
        :key="'in-' + index"
        class="port input-port"
        :data-handle-id="'in-' + index"
        data-handle-type="target"
      >
        ● {{ input }}
      </div>
    </div>

    <!-- OUTPUT PORTS -->
    <div class="ports outputs">
      <div
        v-for="(output, index) in data.outputs"
        :key="'out-' + index"
        class="port output-port"
        :data-handle-id="'out-' + index"
        data-handle-type="source"
      >
        ● {{ output }}
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

/* PROPS */
const props = defineProps({
  id: String,
  data: Object,
})

/* EMITS */
const emit = defineEmits([
  'update:params',
  'update:inputs',
  'update:outputs',
])

/* LOCAL STATE */
const localParams = ref({ ...props.data.params })
const newParamKey = ref("")
const newParamValue = ref("")

/* SYNC WHEN PARENT UPDATES */
watch(
  () => props.data.params,
  v => localParams.value = { ...v }
)

/* EMITTERS */
function emitParams() {
  emit('update:params', { ...localParams.value })
}

function addParam() {
  if (!newParamKey.value.trim()) return

  localParams.value[newParamKey.value] = newParamValue.value
  emitParams()

  newParamKey.value = ""
  newParamValue.value = ""
}
</script>

<style scoped>
.workflow-node {
  background: #1e1e1e;
  border-radius: 8px;
  padding: 10px;
  width: 180px;
  color: #eee;
  border: 1px solid #333;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.header {
  font-size: 14px;
  text-align: center;
  padding-bottom: 6px;
  border-bottom: 1px solid #333;
}

.params {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.param-row {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.param-row input {
  background: #2a2a2a;
  border: 1px solid #444;
  padding: 4px;
  border-radius: 4px;
  color: #eee;
}

.add-param {
  display: flex;
  gap: 4px;
}

.add-param input {
  flex: 1;
  background: #2a2a2a;
  border: 1px solid #444;
  padding: 4px;
  border-radius: 4px;
  color: #eee;
}

.add-param button {
  width: 28px;
  background: #444;
  border: none;
  color: #eee;
  border-radius: 4px;
  cursor: pointer;
}

.ports {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.port {
  font-size: 12px;
  padding: 2px 4px;
  border-radius: 4px;
  background: #2a2a2a;
  border: 1px solid #444;
}

.inputs .port {
  align-self: flex-start;
}

.outputs .port {
  align-self: flex-end;
}
</style>
