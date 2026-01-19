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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import teamService from '@/services/team.service'

const route = useRoute()
const team = ref({ name: '', description: '', members: [] })
const loading = ref(false)

onMounted(async () => {
  const id = route.params.id
  if (!id) return
  loading.value = true
  try {
    const data = await teamService.getTeam(id)
    // team returned has members as array of user objects
    team.value = data
  } catch (e) {
    console.error('Failed to load team', e)
  } finally {
    loading.value = false
  }
})
</script>
