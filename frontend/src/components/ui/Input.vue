<template>
  <input
    :id="id"
    v-bind="$attrs"
    :value="modelValue"
    @input="onInput"
    :class="['px-4 py-3 bg-neutral-800/50 border border-neutral-600 rounded-lg text-white placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent', $attrs.class]
    "
  />
</template>

<script setup>
import { toRef } from 'vue'
const props = defineProps({
  id: String,
  modelValue: [String, Number, Boolean, Array, Object]
})
const emit = defineEmits(['update:modelValue'])

const model = toRef(props, 'modelValue')

function onInput(e) {
  emit('update:modelValue', e.target.value)
}
</script>
