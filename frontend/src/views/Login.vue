<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-neutral-900 via-black to-neutral-900">
    <div class="w-full max-w-md bg-black/60 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
      
      <h1 class="text-2xl font-semibold text-white text-center mb-6">
        Welcome Back
      </h1>

      <form @submit.prevent="login" class="space-y-5">
        <div>
          <label class="block text-sm text-neutral-400 mb-1">Username</label>
          <input
            v-model="username"
            type="text"
            class="w-full px-4 py-2 rounded-lg bg-neutral-900 text-white border border-white/10 focus:outline-none focus:border-indigo-500"
            required
          />
        </div>

        <div>
          <label class="block text-sm text-neutral-400 mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            class="w-full px-4 py-2 rounded-lg bg-neutral-900 text-white border border-white/10 focus:outline-none focus:border-indigo-500"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 transition text-white font-medium"
        >
          Login
        </button>
      </form>

      <p class="text-sm text-neutral-400 text-center mt-6">
        Don’t have an account?
        <router-link to="/register" class="text-indigo-400 hover:underline">
          Register
        </router-link>
      </p>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import useAuth from '@/stores/auth'

const router = useRouter()
const auth = useAuth()
const username = ref('')
const password = ref('')
const loading = ref(false)

const login = async () => {
  loading.value = true
  try {
    const res = await auth.login(username.value, password.value)
    if (res?.access_token) {
      router.push({ name: 'Home' })
    }
  } catch (e) {
    console.error('Login failed', e)
    alert(e.response?.data?.msg || 'Login failed')
  } finally {
    loading.value = false
  }
}
</script>

