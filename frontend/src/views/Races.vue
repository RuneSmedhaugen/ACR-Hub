<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-6xl mx-auto">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-semibold text-white">Races</h1>
        <button class="btn-primary">
          + Create Race
        </button>
      </div>

      <!-- Race List -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="race in races"
          :key="race.id"
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
            <button class="text-indigo-400 hover:underline">
              Leaderboard →
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
const races = [
  {
    id: 1,
    name: "Midnight Gravel Run",
    track: "Finland SS3",
    surface: "Gravel",
    class: "Group A"
  },
  {
    id: 2,
    name: "Alpine Descent",
    track: "Monte Carlo SS1",
    surface: "Tarmac",
    class: "R5"
  },
  {
    id: 3,
    name: "Snowblind Sprint",
    track: "Sweden SS5",
    surface: "Snow",
    class: "WRC"
  }
]
</script>

