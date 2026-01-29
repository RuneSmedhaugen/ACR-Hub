<template>
  <footer class="bg-zinc-900/80 backdrop-blur border-t border-white/5 mt-16">
    <div class="max-w-7xl mx-auto px-6 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        <!-- About -->
        <div>
          <h3 class="text-lg font-semibold text-white mb-4">🏁 AC Rally Hub</h3>
          <p class="text-sm text-neutral-400">
            Your ultimate platform for rally racing community, team management, and competitive leaderboards.
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h4 class="text-sm font-semibold text-white mb-4 uppercase tracking-wide">Navigation</h4>
          <ul class="space-y-2">
            <li><RouterLink to="/" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Home</RouterLink></li>
            <li><RouterLink to="/races" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Races</RouterLink></li>
            <li><RouterLink to="/teams" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Teams</RouterLink></li>
            <li><RouterLink to="/leaderboard" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Leaderboard</RouterLink></li>
          </ul>
        </div>

        <!-- Community -->
        <div>
          <h4 class="text-sm font-semibold text-white mb-4 uppercase tracking-wide">Community</h4>
          <ul class="space-y-2">
            <li><a href="#" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Discord</a></li>
            <li><a href="#" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Twitter</a></li>
            <li><a href="#" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Forums</a></li>
            <li><a href="#" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Support</a></li>
          </ul>
        </div>

        <!-- Legal -->
        <div>
          <h4 class="text-sm font-semibold text-white mb-4 uppercase tracking-wide">Legal</h4>
          <ul class="space-y-2">
            <li><a href="#" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Privacy</a></li>
            <li><a href="#" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Terms</a></li>
            <li><a href="#" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Code of Conduct</a></li>
            <li><a href="#" class="text-sm text-neutral-400 hover:text-indigo-400 transition">Contact</a></li>
          </ul>
        </div>
      </div>

      <!-- Divider -->
      <div class="border-t border-white/5 pt-8">
        <div class="flex flex-col md:flex-row items-center justify-between">
          <p class="text-sm text-neutral-500">
            © 2026 AC Rally Hub. All rights reserved. Built with passion by rally enthusiasts.
          </p>
          <div class="flex gap-6 mt-4 md:mt-0">
            <a href="#" class="text-neutral-400 hover:text-indigo-400 transition">
              <span class="text-xl">𝕏</span>
            </a>
            <a href="#" class="text-neutral-400 hover:text-indigo-400 transition">
              <span class="text-xl">💬</span>
            </a>
            <a href="#" class="text-neutral-400 hover:text-indigo-400 transition">
              <span class="text-xl">📧</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
