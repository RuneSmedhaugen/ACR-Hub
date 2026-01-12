import api from './api'

export default {
  login(username, password) {
    return api.post('/users/login', { username, password })
      .then(res => {
        const token = res.data?.access_token
        if (token) localStorage.setItem('access_token', token)
        return res.data
      })
  },

  register(payload) {
    // payload: { username, password, name, location, ... }
    return api.post('/users/register', payload).then(res => res.data)
  },

  logout() {
    localStorage.removeItem('access_token')
  }
}
