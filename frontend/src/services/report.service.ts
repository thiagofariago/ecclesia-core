import api from './api'
import {
  Aniversariante,
  AniversariantesFilters,
  TotalPeriodoResponse,
  TotalTipoResponse,
  ReportFilters,
  Contribuicao,
} from '../types'

export const reportService = {
  /**
   * Lista aniversariantes
   */
  getAniversariantes: async (filters?: AniversariantesFilters): Promise<Aniversariante[]> => {
    const params: Record<string, any> = {
      periodo: filters?.periodo || 'mes',
    }

    if (filters?.comunidade_id) params.comunidade_id = filters.comunidade_id

    const { data } = await api.get<Aniversariante[]>('/api/reports/aniversariantes', {
      params,
    })
    return data
  },

  /**
   * Obtém total de contribuições por período
   */
  getTotalPeriodo: async (filters: ReportFilters): Promise<TotalPeriodoResponse> => {
    const params: Record<string, any> = {
      start_date: filters.start_date,
      end_date: filters.end_date,
    }

    if (filters.comunidade_id) params.comunidade_id = filters.comunidade_id

    const { data } = await api.get<TotalPeriodoResponse>('/api/reports/total-periodo', {
      params,
    })
    return data
  },

  /**
   * Obtém total de contribuições por tipo
   */
  getTotalTipo: async (filters: ReportFilters): Promise<TotalTipoResponse> => {
    const params: Record<string, any> = {
      start_date: filters.start_date,
      end_date: filters.end_date,
    }

    if (filters.comunidade_id) params.comunidade_id = filters.comunidade_id

    const { data } = await api.get<TotalTipoResponse>('/api/reports/total-tipo', {
      params,
    })
    return data
  },

  /**
   * Obtém histórico de contribuições de um dizimista
   */
  getDizimistaHistorico: async (dizimistaId: number): Promise<Contribuicao[]> => {
    const { data } = await api.get<Contribuicao[]>(
      `/api/reports/dizimista/${dizimistaId}/historico`
    )
    return data
  },
}
