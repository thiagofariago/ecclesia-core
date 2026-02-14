import api from './api'
import { Comunidade } from '../types'

export const comunidadeService = {
  /**
   * Lista comunidades
   */
  list: async (paroquiaId?: number): Promise<Comunidade[]> => {
    const params: Record<string, any> = {}
    if (paroquiaId) params.paroquia_id = paroquiaId

    const { data } = await api.get<Comunidade[]>('/api/comunidades', { params })
    return data
  },

  /**
   * Obtém uma comunidade por ID
   */
  get: async (id: number): Promise<Comunidade> => {
    const { data } = await api.get<Comunidade>(`/api/comunidades/${id}`)
    return data
  },
}
