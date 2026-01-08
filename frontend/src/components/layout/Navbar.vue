<template>
  <nav class="glass-card fixed w-full z-50 shadow-lg">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

      <!-- Logo -->
      <RouterLink to="/" class="text-xl font-bold tracking-wide neon-accent">
        🏁 AC Rally Hub
      </RouterLink>

      <!-- Links -->
      <div class="flex items-center gap-6">
        <RouterLink
          to="/"
          class="text-zinc-200 hover:text-red-400 transition-colors font-semibold px-3 py-2 rounded-md"
        >
          Home
        </RouterLink>
        <RouterLink
          to="/leaderboard"
          class="text-zinc-200 hover:text-red-400 transition-colors font-semibold px-3 py-2 rounded-md"
        >
          Leaderboards
        </RouterLink>
        <RouterLink
          to="/races"
          class="text-zinc-200 hover:text-red-400 transition-colors font-semibold px-3 py-2 rounded-md"
        >
          Races
        </RouterLink>
        <RouterLink
          to="/teams"
          class="text-zinc-200 hover:text-red-400 transition-colors font-semibold px-3 py-2 rounded-md"
        >
          Teams
        </RouterLink>
      </div>

      <!-- Auth -->
      <div class="flex items-center gap-4">
        <RouterLink
          to="/login"
          class="text-zinc-200 hover:text-red-400 transition-colors font-semibold px-3 py-2 rounded-md"
        >
          Login
        </RouterLink>
        <RouterLink to="/register" class="btn-primary">
          Register
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<style src="../assets/futuristic.css"></style>
