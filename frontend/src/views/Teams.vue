<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-6xl mx-auto">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-semibold text-white">Teams</h1>
        <button class="btn-primary">
          + Create Team
        </button>
      </div>

      <!-- Team List -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="team in teams"
          :key="team.name"
          class="glass-card hover:border-indigo-500 transition"
        >
          <h2 class="text-xl text-white mb-2">{{ team.name }}</h2>
          <p class="text-neutral-400 text-sm mb-4">
            {{ team.members.length }} members
          </p>

          <div class="flex flex-wrap gap-2">
            <span
              v-for="member in team.members"
              :key="member"
              class="px-3 py-1 rounded-full bg-indigo-600/20 text-indigo-400 text-xs"
            >
              {{ member }}
            </span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
const teams = [
  {
    name: "Nordic Rally",
    members: ["Rune", "Axel", "Luna"]
  },
  {
    name: "Midnight Apex",
    members: ["Rune", "Kai"]
  },
  {
    name: "Gravel Kings",
    members: ["Nova", "Echo", "Blaze"]
  }
]
</script>
