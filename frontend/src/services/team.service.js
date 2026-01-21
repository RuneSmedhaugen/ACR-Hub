import api from './api'

export default {
	listTeams() {
		return api.get('/teams/')
			.then(res => res.data)
	},

	getTeam(teamId) {
		return api.get(`/teams/${teamId}`)
			.then(res => res.data)
	},

	createTeam(teamData) {
		return api.post('/teams/', teamData)
			.then(res => res.data)
	}
}
