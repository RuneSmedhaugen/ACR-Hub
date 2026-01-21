<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-2xl mx-auto">
      <div class="glass-card">
        <h1 class="text-3xl font-semibold text-white mb-6">Create New Race</h1>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label for="name" class="block text-sm font-medium text-neutral-300 mb-2">Race Name *</label>
            <Input
              id="name"
              v-model="form.name"
              placeholder="Enter race name"
              required
              class="w-full"
            />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="track" class="block text-sm font-medium text-neutral-300 mb-2">Track</label>
              <Input
                id="track"
                v-model="form.track"
                placeholder="Track name"
                class="w-full"
              />
            </div>

            <div>
              <label for="surface" class="block text-sm font-medium text-neutral-300 mb-2">Surface</label>
              <Input
                id="surface"
                v-model="form.surface"
                placeholder="e.g., Asphalt, Dirt"
                class="w-full"
              />
            </div>
          </div>

          <div>
            <label for="class" class="block text-sm font-medium text-neutral-300 mb-2">Class</label>
            <Input
              id="class"
              v-model="form.class"
              placeholder="Race class/category"
              class="w-full"
            />
          </div>

          <div>
            <label for="description" class="block text-sm font-medium text-neutral-300 mb-2">Description</label>
            <textarea
              id="description"
              v-model="form.description"
              placeholder="Describe the race (optional)"
              class="w-full px-4 py-3 bg-neutral-800/50 border border-neutral-600 rounded-lg text-white placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              rows="4"
            ></textarea>
          </div>

          <div class="flex gap-4">
            <Button
              type="submit"
              :disabled="loading"
              class="flex-1"
            >
              {{ loading ? 'Creating...' : 'Create Race' }}
            </Button>
            <Button
              type="button"
              variant="secondary"
              @click="goBack"
              class="flex-1"
            >
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import raceService from '@/services/race.service'
import Input from '@/components/ui/Input.vue'
import Button from '@/components/ui/Button.vue'

const router = useRouter()
const loading = ref(false)
const form = ref({
  name: '',
  track: '',
  surface: '',
  class: '',
  description: ''
})

async function handleSubmit() {
  if (!form.value.name.trim()) return

  loading.value = true
  try {
    const race = await raceService.createRace({
      name: form.value.name.trim(),
      track: form.value.track.trim(),
      surface: form.value.surface.trim(),
      class: form.value.class.trim(),
      description: form.value.description.trim()
    })

    // Redirect to the new race detail page (assuming it exists)
    router.push({ name: 'Races' }) // For now, redirect to races list
  } catch (error) {
    console.error('Failed to create race:', error)
    alert('Failed to create race. Please try again.')
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.back()
}
</script>