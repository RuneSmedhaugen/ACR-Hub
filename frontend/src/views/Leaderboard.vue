<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-6xl mx-auto">

      <!-- Race Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-semibold text-white">{{ race.name || 'Leaderboard' }}</h1>
        <p class="text-neutral-400">
          {{ race.track || '—' }} · {{ race.surface || '—' }} · {{ race.class || '—' }}
        </p>
      </div>

      <!-- Podium -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div
          v-for="(entry, index) in podium"
          :key="entry.user?._id || index"
          class="podium-card"
          :class="podiumColors[index]"
        >
          <p class="rank">#{{ index + 1 }}</p>
          <p class="name">{{ entry.user?.name || entry.user?.username || '—' }}</p>
          <p class="time">{{ formatMs(entry.total_time) }}</p>
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
              :key="entry.user?._id || index"
              class="border-t border-white/10 hover:bg-white/5 transition"
            >
              <td class="td">#{{ entry.rank || (index + 1) }}</td>
              <td class="td">{{ entry.user?.name || entry.user?.username || '—' }}</td>
              <td class="td">{{ entry.user?.team || "—" }}</td>
              <td class="td font-mono">{{ formatMs(entry.total_time) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import leaderboardService from '@/services/leaderboard.service'
import raceService from '@/services/race.service'

const route = useRoute()
const race = ref({})
const leaderboard = ref([])
const podium = ref([])
const podiumColors = [
  'border-yellow-500 text-yellow-400',
  'border-neutral-400 text-neutral-300',
  'border-amber-700 text-amber-500'
]

function formatMs(ms) {
  if (ms == null) return '—'
  const total = Math.floor(ms)
  const minutes = Math.floor(total / 60000)
  const seconds = Math.floor((total % 60000) / 1000)
  const millis = total % 1000
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2,'0')}.${String(millis).padStart(3,'0')}`
}

onMounted(async () => {
  try {
    let raceId = route.query.race
    if (!raceId) {
      const races = await raceService.listRaces()
      if (races && races.length) raceId = races[0]._id
      else return
    }

    const data = await leaderboardService.getRaceLeaderboard(raceId)
    if (data?.race) race.value = data.race
    if (data?.leaderboard) {
      leaderboard.value = data.leaderboard
      podium.value = leaderboard.value.slice(0,3)
    }
  } catch (e) {
    console.error('Failed to load leaderboard', e)
  }
})
</script>