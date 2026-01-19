<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-neutral-900 via-black to-neutral-900">
    <div class="w-full max-w-lg bg-black/60 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
      
      <h1 class="text-2xl font-semibold text-white text-center mb-6">
        Create Account
      </h1>

      <form @submit.prevent="register" class="grid grid-cols-1 md:grid-cols-2 gap-4">

        <div class="md:col-span-2">
          <label class="block text-sm text-neutral-400 mb-1">Username</label>
          <input v-model="form.username" type="text" class="input" required />
        </div>

        <div>
          <label class="block text-sm text-neutral-400 mb-1">Name</label>
          <input v-model="form.name" type="text" class="input" />
        </div>

        <div>
          <label class="block text-sm text-neutral-400 mb-1">Country</label>
          <select v-model="form.location" class="input">
            <option value="">Choose country</option>
            <option v-for="c in countriesList" :key="c.code" :value="c.code">{{ c.name }}</option>
          </select>
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm text-neutral-400 mb-1">Avatar URL</label>
          <input v-model="form.avatar" type="url" class="input" placeholder="https://..." />
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm text-neutral-400 mb-1">Bio</label>
          <textarea v-model="form.bio" class="input h-24 resize-y" placeholder="Short bio or tagline"></textarea>
        </div>

        <div>
          <label class="block text-sm text-neutral-400 mb-1">Age</label>
          <input v-model.number="form.age" type="number" min="0" class="input" />
        </div>

        <div>
          <label class="block text-sm text-neutral-400 mb-1">Favorite Car</label>
          <input v-model="form.car" type="text" class="input" placeholder="e.g. Subaru Impreza" />
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm text-neutral-400 mb-1">Password</label>
          <input v-model="form.password" type="password" class="input" required />
        </div>

        <div class="md:col-span-2">
          <button
            type="submit"
            class="w-full py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 transition text-white font-medium"
          >
            Register
          </button>
        </div>

      </form>

      <p class="text-sm text-neutral-400 text-center mt-6">
        Already registered?
        <router-link to="/login" class="text-indigo-400 hover:underline">
          Login
        </router-link>
      </p>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/auth.service'
import countries from '@/data/countries'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  name: '',
  avatar: '',
  bio: '',
  age: null,
  car: '',
  location: ''
})

const countriesList = ref([])

onMounted(() => {
  countriesList.value = countries
})

const register = async () => {
  loading.value = true
  try {
    await authService.register({
      username: form.username,
      password: form.password,
      name: form.name || form.username,
      avatar: form.avatar || '',
      bio: form.bio || '',
      age: form.age || 0,
      car: form.car || '',
      location: form.location || ''
    })
    alert('Registration successful — please login')
    router.push({ name: 'Login' })
  } catch (e) {
    console.error('Register failed', e)
    alert(e.response?.data?.msg || 'Registration failed')
  } finally {
    loading.value = false
  }
}
</script>

