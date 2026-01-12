<template>
  <div class="min-h-screen bg-zinc-900">
    <Navbar />
    <RouterView />
  </div>
</template>

<script setup>
import Navbar from "./components/layout/Navbar.vue"
</script>
