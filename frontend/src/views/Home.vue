<template>
  <div class="bg-[#070912] text-white min-h-screen">

    <!-- Hero -->
    <section class="max-w-7xl mx-auto px-6 py-32 text-center">
      <h1 class="text-5xl md:text-6xl font-extrabold mb-6 text-red-500 neon-accent">
        Assetto Corsa Rally Hub
      </h1>
      <p class="text-zinc-300 text-lg md:text-xl max-w-3xl mx-auto mb-12 leading-relaxed">
        Compete in single-player rally events, climb the leaderboards,
        and represent your team across stages.
      </p>
    </section>

    <!-- Features -->
    <section class="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-10">
      <FeatureCard
        title="Races"
        text="Create and participate in rally events with global rankings."
        class="glass-card"
      />
      <FeatureCard
        title="Teams"
        text="Join or create teams and dominate the leaderboard together."
        class="glass-card"
      />
      <FeatureCard
        title="Leaderboards"
        text="Track the fastest drivers across all stages and seasons."
        class="glass-card"
      />
    </section>

  </div>
</template>

<script setup>
import FeatureCard from "@/components/ui/FeatureCard.vue";
</script>

