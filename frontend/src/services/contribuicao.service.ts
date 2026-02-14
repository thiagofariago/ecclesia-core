import api from './api'
import {
  Contribuicao,
  ContribuicaoCreate,
  ContribuicaoFilters,
  PaginatedResponse,
} from '../types'

export const contribuicaoService = {
  /**
   * Lista contribuições com filtros e paginação
   */
  list: async (filters?: ContribuicaoFilters): Promise<PaginatedResponse<Contribuicao>> => {
    const params: Record<string, any> = {
      page: filters?.page || 1,
      page_size: filters?.page_size || 20,
    }

    if (filters?.dizimista_id) params.dizimista_id = filters.dizimista_id
    if (filters?.comunidade_id) params.comunidade_id = filters.comunidade_id
    if (filters?.tipo) params.tipo = filters.tipo
    if (filters?.start_date) params.start_date = filters.start_date
    if (filters?.end_date) params.end_date = filters.end_date

    const { data } = await api.get<PaginatedResponse<Contribuicao>>('/api/contribuicoes', {
      params,
    })
    return data
  },

  /**
   * Obtém uma contribuição por ID
   */
  get: async (id: number): Promise<Contribuicao> => {
    const { data } = await api.get<Contribuicao>(`/api/contribuicoes/${id}`)
    return data
  },

  /**
   * Cria uma nova contribuição
   */
  create: async (contribuicao: ContribuicaoCreate): Promise<Contribuicao> => {
    const { data } = await api.post<Contribuicao>('/api/contribuicoes', contribuicao)
    return data
  },
}
