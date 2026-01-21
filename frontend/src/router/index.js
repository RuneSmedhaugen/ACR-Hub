import { createRouter, createWebHistory } from "vue-router"
import useAuth from '@/stores/auth'

// Views
import Home from "@/views/Home.vue"
import Login from "@/views/Login.vue"
import Register from "@/views/Register.vue"
import Profile from "@/views/Profile.vue"
import EditProfile from "@/views/EditProfile.vue"
import Teams from "@/views/Teams.vue"
import TeamDetail from "@/views/TeamDetail.vue"
import CreateTeam from "@/views/CreateTeam.vue"
import Races from "@/views/Races.vue"
import CreateRace from "@/views/CreateRace.vue"
import Leaderboard from "@/views/Leaderboard.vue"

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/register",
    name: "Register",
    component: Register
  },
  {
    path: "/leaderboard",
    name: "Leaderboard",
    component: Leaderboard
  },
  {
    path: "/races",
    name: "Races",
    component: Races
  },
  {
    path: "/races/create",
    name: "CreateRace",
    component: CreateRace,
    meta: { requiresAuth: true }
  },
  {
    path: "/teams",
    name: "Teams",
    component: Teams
  },
  {
    path: "/teams/create",
    name: "CreateTeam",
    component: CreateTeam,
    meta: { requiresAuth: true }
  },
  {
    path: "/teams/:id",
    name: "TeamDetail",
    component: TeamDetail,
    props: true
  },
  {
    path: "/profile/:id",
    name: "Profile",
    component: Profile,
    props: true,
    meta: { requiresAuth: true }
  }
  ,
  {
    path: "/profile/edit",
    name: "EditProfile",
    component: EditProfile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard: protect routes that set `meta.requiresAuth`
const auth = useAuth()
router.beforeEach(async (to, from, next) => {
  // redirect logged-in users away from login/register
  if ((to.name === 'Login' || to.name === 'Register') && auth.isLoggedIn()) {
    return next({ name: 'Home' })
  }

  if (to.meta?.requiresAuth) {
    if (!auth.isLoggedIn()) {
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    }

    // ensure user object is loaded
    if (!auth.state.user) {
      try {
        await auth.fetchUser()
      } catch (e) {
        return next({ name: 'Login', query: { redirect: to.fullPath } })
      }
    }
  }

  next()
})

export default router
