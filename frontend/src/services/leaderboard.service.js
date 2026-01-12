import api from './api'

export default {
  getRaceLeaderboard(raceId) {
    return api.get(`/leaderboard/races/${raceId}`)
      .then(res => res.data)
  },

  getRaceStages(raceId) {
    return api.get(`/leaderboard/races/${raceId}/stages`)
      .then(res => res.data)
  }
}
