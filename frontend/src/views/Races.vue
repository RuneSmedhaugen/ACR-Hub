<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-6xl mx-auto">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-semibold text-white">Races</h1>
      </div>

      <!-- Race List -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="race in races"
          :key="race._id"
          class="glass-card hover:border-indigo-500 transition"
        >
          <h2 class="text-xl text-white mb-1">{{ race.name }}</h2>
          <p class="text-neutral-400 text-sm mb-3">
            {{ race.track }} · {{ race.surface }}
          </p>

          <div class="flex justify-between items-center text-sm">
            <span class="text-neutral-500">
              Class: {{ race.class }}
            </span>
            <router-link :to="{ name: 'Leaderboard', query: { race: race._id } }" class="text-indigo-400 hover:underline">
              Leaderboard →
            </router-link>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import raceService from '@/services/race.service'

const races = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    races.value = await raceService.listRaces()
  } catch (e) {
    console.error('Failed to load races', e)
  } finally {
    loading.value = false
  }
})
</script>

