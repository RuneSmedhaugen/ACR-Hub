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
          <label class="block text-sm text-neutral-400 mb-1">In-game Name</label>
          <input v-model="form.ign" type="text" class="input" />
        </div>

        <div>
          <label class="block text-sm text-neutral-400 mb-1">Location</label>
          <input v-model="form.location" type="text" class="input" />
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
import { reactive } from "vue"

const form = reactive({
  username: "",
  ign: "",
  location: "",
  password: ""
})

const register = () => {
  console.log("Register:", form)
}
</script>

