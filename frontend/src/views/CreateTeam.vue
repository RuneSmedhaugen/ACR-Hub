<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-2xl mx-auto">
      <div class="glass-card">
        <h1 class="text-3xl font-semibold text-white mb-6">Create New Team</h1>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label for="name" class="block text-sm font-medium text-neutral-300 mb-2">Team Name *</label>
            <Input
              id="name"
              v-model="form.name"
              placeholder="Enter team name"
              required
              class="w-full"
            />
          </div>

          <div>
            <label for="description" class="block text-sm font-medium text-neutral-300 mb-2">Description</label>
            <textarea
              id="description"
              v-model="form.description"
              placeholder="Describe your team (optional)"
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
              {{ loading ? 'Creating...' : 'Create Team' }}
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
import teamService from '@/services/team.service'
import Input from '@/components/ui/Input.vue'
import Button from '@/components/ui/Button.vue'

const router = useRouter()
const loading = ref(false)
const form = ref({
  name: '',
  description: ''
})

async function handleSubmit() {
  if (!form.value.name.trim()) return

  loading.value = true
  try {
    const team = await teamService.createTeam({
      name: form.value.name.trim(),
      description: form.value.description.trim()
    })

    // Redirect to the new team detail page
    router.push({ name: 'TeamDetail', params: { id: team._id } })
  } catch (error) {
    console.error('Failed to create team:', error)
    alert('Failed to create team. Please try again.')
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.back()
}
</script>