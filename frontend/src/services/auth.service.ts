import api from './api'
import { LoginRequest, LoginResponse, User } from '../types'

export const authService = {
  /**
   * Login do usuário
   */
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const { data } = await api.post<LoginResponse>('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return data
  },

  /**
   * Obtém dados do usuário autenticado
   */
  getMe: async (): Promise<User> => {
    const { data } = await api.get<User>('/api/auth/me')
    return data
  },

  /**
   * Logout do usuário
   */
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
}
