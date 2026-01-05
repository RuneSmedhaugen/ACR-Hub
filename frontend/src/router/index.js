import { createRouter, createWebHistory } from "vue-router"

// Views
import Home from "@/views/Home.vue"
import Login from "@/views/Login.vue"
import Register from "@/views/Register.vue"
import Profile from "@/views/Profile.vue"
import Teams from "@/views/Teams.vue"
import TeamDetail from "@/views/TeamDetail.vue"
import Races from "@/views/Races.vue"
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
    path: "/teams",
    name: "Teams",
    component: Teams
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
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
