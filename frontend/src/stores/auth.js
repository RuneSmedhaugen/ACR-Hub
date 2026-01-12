import { reactive } from 'vue'
import authService from '@/services/auth.service'
import userService from '@/services/user.service'

const state = reactive({
  token: localStorage.getItem('access_token') || null,
  user: null,
  loading: false
})

function isLoggedIn() {
  return !!state.token
}

function setToken(token) {
  state.token = token
  if (token) localStorage.setItem('access_token', token)
  else localStorage.removeItem('access_token')
}

async function fetchUser() {
  if (!state.token) return null
  try {
    state.loading = true
    const data = await userService.getMe()
    state.user = data
    return data
  } catch (e) {
    // invalid token — clear
    setToken(null)
    state.user = null
    throw e
  } finally {
    state.loading = false
  }
}

async function login(username, password) {
  const res = await authService.login(username, password)
  const token = res?.access_token
  if (token) {
    setToken(token)
    await fetchUser()
  }
  return res
}

function logout() {
  authService.logout()
  setToken(null)
  state.user = null
}

export default function useAuth() {
  return {
    state,
    isLoggedIn,
    fetchUser,
    setToken,
    login,
    logout
  }
}
