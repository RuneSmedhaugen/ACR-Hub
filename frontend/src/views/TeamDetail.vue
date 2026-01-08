<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-5xl mx-auto">

      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h1 class="text-3xl font-semibold text-white">{{ team.name }}</h1>
          <p class="text-neutral-400 mt-1">{{ team.description }}</p>
        </div>

        <button class="btn-outline">
          Leave Team
        </button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div class="stat-card">
          <p class="label">Members</p>
          <p class="value">{{ team.members.length }}</p>
        </div>
        <div class="stat-card">
          <p class="label">Races Entered</p>
          <p class="value">18</p>
        </div>
        <div class="stat-card">
          <p class="label">Podiums</p>
          <p class="value">5</p>
        </div>
      </div>

      <!-- Members -->
      <div>
        <h2 class="text-xl text-white mb-4">Members</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <div
            v-for="member in team.members"
            :key="member"
            class="glass-card"
          >
            {{ member }}
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
const team = {
  name: "Nordic Rally",
  description: "Cold tires, fast lines, questionable bravery.",
  members: ["Rune", "Axel", "Luna", "Nova"]
}
</script>
