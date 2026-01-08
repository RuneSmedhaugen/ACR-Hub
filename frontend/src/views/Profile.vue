<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-5xl mx-auto">

      <!-- Header -->
      <div class="flex items-center gap-6 mb-8">
        <div class="w-24 h-24 rounded-full bg-indigo-600/20 border border-indigo-500 flex items-center justify-center text-3xl font-bold text-indigo-400">
          {{ initials }}
        </div>

        <div>
          <h1 class="text-3xl font-semibold text-white">{{ user.ign }}</h1>
          <p class="text-neutral-400">@{{ user.username }} · {{ user.location }}</p>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div class="stat-card">
          <p class="label">Total Races</p>
          <p class="value">12</p>
        </div>
        <div class="stat-card">
          <p class="label">Best Time</p>
          <p class="value">03:42.118</p>
        </div>
        <div class="stat-card">
          <p class="label">Teams</p>
          <p class="value">{{ user.teams.length }}</p>
        </div>
      </div>

      <!-- Teams -->
      <div>
        <h2 class="text-xl text-white mb-4">Teams</h2>
        <div v-if="user.teams.length" class="grid gap-4">
          <div
            v-for="team in user.teams"
            :key="team"
            class="glass-card hover:border-indigo-500 transition"
          >
            {{ team }}
          </div>
        </div>
        <p v-else class="text-neutral-500">No teams joined yet.</p>
      </div>

    </div>
  </div>
</template>

<script setup>
const user = {
  username: "rune",
  ign: "FlatOutRune",
  location: "Norway",
  teams: ["Nordic Rally", "Midnight Apex"]
}

const initials = user.ign
  .split(" ")
  .map(w => w[0])
  .join("")
</script>

