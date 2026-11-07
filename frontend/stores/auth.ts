import { defineStore } from 'pinia'

export interface User {
  id: number
  username: string
  phone_number: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  avatar: string | null
  bio: string | null
  is_verified: boolean
  is_staff: boolean
  student_profile?: {
    instrument: string
    instrument_display: string
    skill_level: string
    skill_level_display: string
    learning_goals: string
    attended_sessions_count: number
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    accessToken: null as string | null,
    refreshToken: null as string | null,
    isAuthModalOpen: false,
    authModalMode: 'otp' as 'otp' | 'login' | 'register',
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken && !!state.user,
    isStudent: (state) => !!state.user?.student_profile,
  },

  actions: {
    initAuth() {
      if (process.client) {
        const access = localStorage.getItem('bahavar_access_token')
        const refresh = localStorage.getItem('bahavar_refresh_token')
        const savedUser = localStorage.getItem('bahavar_user')

        if (access) this.accessToken = access
        if (refresh) this.refreshToken = refresh
        if (savedUser) {
          try {
            this.user = JSON.parse(savedUser)
          } catch (e) {
            console.error('Failed to parse user from localStorage', e)
          }
        }
      }
    },

    setAuth(tokens: { access: string; refresh: string }, user: User) {
      this.accessToken = tokens.access
      this.refreshToken = tokens.refresh
      this.user = user

      if (process.client) {
        localStorage.setItem('bahavar_access_token', tokens.access)
        localStorage.setItem('bahavar_refresh_token', tokens.refresh)
        localStorage.setItem('bahavar_user', JSON.stringify(user))
      }
    },

    openAuthModal(mode: 'otp' | 'login' | 'register' = 'otp') {
      this.authModalMode = mode
      this.isAuthModalOpen = true
    },

    closeAuthModal() {
      this.isAuthModalOpen = false
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null

      if (process.client) {
        localStorage.removeItem('bahavar_access_token')
        localStorage.removeItem('bahavar_refresh_token')
        localStorage.removeItem('bahavar_user')
      }
    },
  },
})
