import { useAuthStore } from '~/stores/auth'

export const useApi = () => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const apiFetch = async <T = any>(endpoint: string, options: any = {}): Promise<T> => {
    const baseURL = config.public.apiBase || 'http://localhost:8000/api'
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
    const url = `${baseURL}${cleanEndpoint}`

    const headers: Record<string, string> = {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    }

    if (authStore.accessToken) {
      headers['Authorization'] = `Bearer ${authStore.accessToken}`
    }

    try {
      return await $fetch<T>(url, {
        ...options,
        headers,
      })
    } catch (err: any) {
      // Auto handle 401 token expiry if needed
      if (err?.response?.status === 401 && authStore.isAuthenticated) {
        authStore.logout()
      }
      throw err
    }
  }

  return {
    apiFetch,
  }
}
