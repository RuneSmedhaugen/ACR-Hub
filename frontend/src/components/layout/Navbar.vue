<template>
  <nav class="bg-zinc-900/80 backdrop-blur border-b border-white/5">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

      <RouterLink to="/" class="text-xl font-bold neon-accent">
        🏁 AC Rally Hub
      </RouterLink>

      <div class="flex items-center gap-2">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/leaderboard" class="nav-link">Leaderboards</RouterLink>
        <RouterLink to="/races" class="nav-link">Races</RouterLink>
        <RouterLink to="/teams" class="nav-link">Teams</RouterLink>
      </div>

      <div class="flex items-center gap-3">
        <template v-if="isLoggedIn">
          <RouterLink v-if="userId" :to="{ name: 'Profile', params: { id: userId } }" class="nav-link">Profile</RouterLink>
          <button @click="handleLogout" class="btn-ghost">Logout</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="nav-link">Login</RouterLink>
          <RouterLink to="/register" class="btn-primary">Register</RouterLink>
        </template>
      </div>

    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import useAuth from '@/stores/auth'

const auth = useAuth()
const router = useRouter()

const isLoggedIn = computed(() => auth.isLoggedIn())
const userId = computed(() => auth.state.user?._id)

function handleLogout() {
  auth.logout()
  router.push({ name: 'Home' })
}
</script>
