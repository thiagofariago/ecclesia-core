import api from './api'
import {
  Dizimista,
  DizimistaCreate,
  DizimistaUpdate,
  DizimistaFilters,
  PaginatedResponse,
} from '../types'

export const dizimistaService = {
  /**
   * Lista dizimistas com filtros e paginação
   */
  list: async (filters?: DizimistaFilters): Promise<PaginatedResponse<Dizimista>> => {
    const params: Record<string, any> = {
      page: filters?.page || 1,
      page_size: filters?.page_size || 20,
    }

    if (filters?.search) params.search = filters.search
    if (filters?.comunidade_id) params.comunidade_id = filters.comunidade_id
    if (filters?.ativo !== undefined) params.ativo = filters.ativo

    const { data } = await api.get<PaginatedResponse<Dizimista>>('/api/dizimistas', {
      params,
    })
    return data
  },

  /**
   * Obtém um dizimista por ID
   */
  get: async (id: number): Promise<Dizimista> => {
    const { data } = await api.get<Dizimista>(`/api/dizimistas/${id}`)
    return data
  },

  /**
   * Cria um novo dizimista
   */
  create: async (dizimista: DizimistaCreate): Promise<Dizimista> => {
    const { data } = await api.post<Dizimista>('/api/dizimistas', dizimista)
    return data
  },

  /**
   * Atualiza um dizimista
   */
  update: async (id: number, dizimista: DizimistaUpdate): Promise<Dizimista> => {
    const { data } = await api.patch<Dizimista>(`/api/dizimistas/${id}`, dizimista)
    return data
  },

  /**
   * Desativa um dizimista (soft delete)
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/dizimistas/${id}`)
  },

  /**
   * Busca dizimistas para autocomplete
   */
  search: async (query: string): Promise<Dizimista[]> => {
    const { data } = await api.get<PaginatedResponse<Dizimista>>('/api/dizimistas', {
      params: {
        search: query,
        page_size: 10,
        ativo: true,
      },
    })
    return data.items
  },
}
