<template>
  <div class="bg-zinc-900 border border-zinc-800 p-8 rounded-2xl text-center">
    <h3 class="text-2xl font-bold mb-4">{{ title }}</h3>
    <p class="text-zinc-400">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  text: String
})
</script>
