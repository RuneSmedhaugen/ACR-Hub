import api from './api'

export default {
	listRaces() {
		return api.get('/races/')
			.then(res => res.data)
	},

	getRace(raceId) {
		return api.get(`/races/${raceId}`)
			.then(res => res.data)
	}
}
