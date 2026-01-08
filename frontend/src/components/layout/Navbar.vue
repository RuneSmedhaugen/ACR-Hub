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
        <RouterLink to="/login" class="nav-link">Login</RouterLink>
        <RouterLink to="/register" class="btn-primary">Register</RouterLink>
      </div>

    </div>
  </nav>
</template>
