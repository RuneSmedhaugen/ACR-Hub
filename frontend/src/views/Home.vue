<template>
  <div class="bg-zinc-950 text-white min-h-screen">

    <!-- Hero -->
    <section class="max-w-7xl mx-auto px-6 py-24 text-center">
      <h1 class="text-5xl font-extrabold mb-6">
        Assetto Corsa Rally Hub
      </h1>
      <p class="text-zinc-400 text-lg max-w-2xl mx-auto mb-10">
        Compete in single-player rally events, climb the leaderboards,
        and represent your team across stages.
      </p>

      <div class="flex justify-center gap-6">
        <RouterLink
          to="/leaderboard"
          class="bg-red-600 hover:bg-red-700 px-8 py-4 rounded-lg font-semibold"
        >
          View Leaderboards
        </RouterLink>

        <RouterLink
          to="/register"
          class="border border-zinc-700 hover:border-white px-8 py-4 rounded-lg font-semibold"
        >
          Join the Hub
        </RouterLink>
      </div>
    </section>

    <!-- Features -->
    <section class="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-10">
      <FeatureCard
        title="Races"
        text="Create and participate in rally events with global rankings."
      />
      <FeatureCard
        title="Teams"
        text="Join or create teams and dominate the leaderboard together."
      />
      <FeatureCard
        title="Leaderboards"
        text="Track the fastest drivers across all stages and seasons."
      />
    </section>

  </div>
</template>

<script setup>
import FeatureCard from "@/components/ui/FeatureCard.vue"
</script>
