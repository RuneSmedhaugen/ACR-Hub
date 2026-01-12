import api from './api'

export default {
  getMe() {
    return api.get('/users/me').then(res => res.data)
  }
}
