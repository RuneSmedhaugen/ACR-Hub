<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
    <div class="max-w-5xl mx-auto">

          <!-- Header -->
          <div class="flex items-start gap-6 mb-8">
            <div class="flex-shrink-0">
              <div v-if="user.avatar" class="rounded-full overflow-hidden border border-indigo-500" :style="avatarContainerStyle">
                <img :src="user.avatar" alt="avatar" :style="avatarStyle" />
              </div>
              <div v-else class="rounded-full bg-indigo-600/20 border border-indigo-500 flex items-center justify-center text-sm font-bold text-indigo-400" :style="avatarContainerStyle">
                {{ initials }}
              </div>
            </div>

            <div class="flex-1">
              <div class="flex items-start justify-between">
                <div>
                  <div class="flex items-center gap-3">
                    <h1 class="text-3xl font-semibold text-white">{{ user.name || user.username }}</h1>
                    <img v-if="flagUrl" :src="flagUrl" :alt="user.location" :style="flagStyle" @error="flagError = true" v-show="!flagError" />
                  </div>
                  <p class="text-sm text-neutral-400 mt-2">{{ user.bio }}</p>
                </div>

                <div class="flex items-center gap-2">
                  <button @click="goEdit" class="px-4 py-2 rounded-lg border border-white/10 bg-indigo-600 text-white hover:bg-indigo-500">Edit Profile</button>
                  <button @click="goCreateTeam" class="px-3 py-2 rounded-lg border border-white/10 text-white/80">Create team</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Details -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="glass-card">
              <p class="label">Age</p>
              <p class="value">{{ user.age ?? '—' }}</p>
            </div>
            <div class="glass-card">
              <p class="label">Car</p>
              <p class="value">{{ user.car || '—' }}</p>
            </div>
            <div class="glass-card">
              <p class="label">Team</p>
              <p class="value">{{ user.team || '—' }}</p>
            </div>
          </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import userService from '@/services/user.service'

const flagError = ref(false)

const router = useRouter()
const user = ref({ username: '', name: '', location: '', team: '', avatar: '', bio: '', age: null, car: '' })
const loading = ref(false)

const initials = computed(() => {
  const name = user.value.name || user.value.username || ''
  return name
    .split(' ')
    .map(w => w[0] || '')
    .join('')
})

const flagUrl = computed(() => {
  const loc = (user.value.location || '').toLowerCase()
  if (!loc) return ''
  return `https://flagcdn.com/w20/${loc}.png`
})

const flagStyle = {
  width: '20px',
  height: '14px',
  objectFit: 'cover',
  display: 'inline-block'
}

const avatarContainerStyle = {
  width: '96px',
  height: '96px'
}

const avatarStyle = {
  width: '96px',
  height: '96px',
  objectFit: 'cover',
  display: 'block'
}

function goEdit() {
  // placeholder route for future edit profile page
  router.push({ path: '/profile/edit' })
}

function goCreateTeam() {
  router.push({ name: 'CreateTeam' })
}

onMounted(async () => {
  loading.value = true
  try {
    const data = await userService.getMe()
    if (data) user.value = data
  } catch (e) {
    console.error('Failed to load profile', e)
  } finally {
    loading.value = false
  }
})
</script>

