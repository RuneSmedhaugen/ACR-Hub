import api from './api'

export default {
	listTeams() {
		return api.get('/teams/')
			.then(res => res.data)
	},

	getTeam(teamId) {
		return api.get(`/teams/${teamId}`)
			.then(res => res.data)
	}
}
