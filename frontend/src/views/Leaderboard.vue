<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-6xl mx-auto">

      <!-- Race Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-semibold text-white">{{ race.name }}</h1>
        <p class="text-neutral-400">
          {{ race.track }} · {{ race.surface }} · {{ race.class }}
        </p>
      </div>

      <!-- Podium -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div
          v-for="(entry, index) in podium"
          :key="entry.user"
          class="podium-card"
          :class="podiumColors[index]"
        >
          <p class="rank">#{{ index + 1 }}</p>
          <p class="name">{{ entry.user }}</p>
          <p class="time">{{ entry.time }}</p>
        </div>
      </div>

      <!-- Full Leaderboard -->
      <div class="glass-card overflow-hidden">
        <table class="w-full text-left">
          <thead class="bg-white/5">
            <tr>
              <th class="th">Rank</th>
              <th class="th">Driver</th>
              <th class="th">Team</th>
              <th class="th">Time</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(entry, index) in leaderboard"
              :key="entry.user"
              class="border-t border-white/10 hover:bg-white/5 transition"
            >
              <td class="td">#{{ index + 1 }}</td>
              <td class="td">{{ entry.user }}</td>
              <td class="td">{{ entry.team || "—" }}</td>
              <td class="td font-mono">{{ entry.time }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
const race = {
  name: "Midnight Gravel Run",
  track: "Finland SS3",
  surface: "Gravel",
  class: "Group A"
}

const leaderboard = [
  { user: "Rune", team: "Nordic Rally", time: "03:42.118" },
  { user: "Axel", team: "Nordic Rally", time: "03:45.902" },
  { user: "Luna", team: "Midnight Apex", time: "03:47.331" },
  { user: "Nova", team: null, time: "03:49.018" },
  { user: "Echo", team: "Gravel Kings", time: "03:52.441" }
]

const podium = leaderboard.slice(0, 3)

const podiumColors = [
  "border-yellow-500 text-yellow-400",
  "border-neutral-400 text-neutral-300",
  "border-amber-700 text-amber-500"
]
</script>