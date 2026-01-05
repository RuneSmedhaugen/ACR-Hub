<template>
  <nav class="bg-zinc-900 text-white shadow-md">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
      
      <!-- Logo -->
      <RouterLink to="/" class="text-xl font-bold tracking-wide">
        🏁 AC Rally Hub
      </RouterLink>

      <!-- Links -->
      <div class="flex items-center gap-6">
        <RouterLink class="nav-link" to="/">Home</RouterLink>
        <RouterLink class="nav-link" to="/leaderboard">Leaderboards</RouterLink>
        <RouterLink class="nav-link" to="/races">Races</RouterLink>
        <RouterLink class="nav-link" to="/teams">Teams</RouterLink>
      </div>

      <!-- Auth -->
      <div class="flex items-center gap-4">
        <RouterLink class="nav-link" to="/login">Login</RouterLink>
        <RouterLink
          to="/register"
          class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg font-semibold"
        >
          Register
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.nav-link {
  @apply text-zinc-300 hover:text-white transition;
}
</style>
