<template>
    <div class="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 p-8">
        <div class="max-w-3xl mx-auto glass-card">
            <h2 class="text-2xl text-white font-semibold mb-4">Edit Profile</h2>

            <form @submit.prevent="save" class="grid grid-cols-1 gap-4">
                <div>
                    <label class="block text-sm text-neutral-400 mb-1">Username</label>
                    <input v-model="form.username" type="text" class="input" />
                </div>

                <div>
                    <label class="block text-sm text-neutral-400 mb-1">Name</label>
                    <input v-model="form.name" type="text" class="input" />
                </div>

                <div>
                    <label class="block text-sm text-neutral-400 mb-1">Avatar URL</label>
                    <input v-model="form.avatar" type="url" class="input" placeholder="https://..." />
                </div>

                <div>
                    <label class="block text-sm text-neutral-400 mb-1">Bio</label>
                    <textarea v-model="form.bio" class="input h-24 resize-y"></textarea>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm text-neutral-400 mb-1">Age</label>
                        <input v-model.number="form.age" type="number" min="0" class="input" />
                    </div>
                    <div>
                        <label class="block text-sm text-neutral-400 mb-1">Favorite Car</label>
                        <input v-model="form.car" type="text" class="input" />
                    </div>
                </div>

                <div>
                    <label class="block text-sm text-neutral-400 mb-1">Country</label>
                    <select v-model="form.location" class="input">
                        <option value="">Choose country</option>
                        <option v-for="c in countriesList" :key="c.code" :value="c.code">{{ c.name }}</option>
                    </select>
                </div>

                <div class="flex gap-3 mt-4">
                    <button type="submit" class="btn-primary">Save Changes</button>
                    <button type="button" @click="cancel" class="btn-outline">Cancel</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import userService from '@/services/user.service'
import api from '@/services/api'
import useAuth from '@/stores/auth'
import countries from '@/data/countries'

const router = useRouter()
const auth = useAuth()

const form = reactive({
    username: '',
    name: '',
    avatar: '',
    bio: '',
    age: null,
    car: '',
    location: ''
})

const countriesList = countries

onMounted(async () => {
    try {
        const data = await userService.getMe()
        if (data) {
            form.username = data.username || ''
            form.name = data.name || ''
            form.avatar = data.avatar || ''
            form.bio = data.bio || ''
            form.age = data.age || null
            form.car = data.car || ''
            form.location = data.location || ''
        }
    } catch (e) {
        console.error('Failed to load profile for editing', e)
    }
})

async function save () {
        try {
            // client-side quick validation
            if (!form.username || form.username.length < 3) {
                alert('Username must be at least 3 characters')
                return
            }

            const payload = {
                username: form.username,
                name: form.name,
                avatar: form.avatar,
                bio: form.bio,
                age: form.age,
                car: form.car,
                location: form.location
            }

            const res = await api.put('/users/me', payload)
            const data = res.data || {}
            if (data.access_token) {
                // update stored token then refresh user
                auth.setToken(data.access_token)
            }
            try { await auth.fetchUser() } catch (e) {}
            alert('Profile updated')
            router.back()
        } catch (e) {
            console.error('Save failed', e)
            alert(e.response?.data?.msg || 'Failed to save profile')
        }
}

function cancel () {
    router.back()
}
</script>