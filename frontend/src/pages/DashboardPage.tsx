import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { dizimistaService } from '../services/dizimista.service'
import { contribuicaoService } from '../services/contribuicao.service'
import { reportService } from '../services/report.service'
import { formatCurrency, formatDateForInput } from '../utils/format'

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate()

  // Get current month start and end
  const now = new Date()
  const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
  const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0)

  const { data: dizimistasData, isLoading: loadingDizimistas } = useQuery({
    queryKey: ['dizimistas', { ativo: true }],
    queryFn: () => dizimistaService.list({ ativo: true, page: 1, page_size: 1 }),
  })

  const { data: contribuicoesData, isLoading: loadingContribuicoes } = useQuery({
    queryKey: ['contribuicoes-count'],
    queryFn: () => contribuicaoService.list({ page: 1, page_size: 1 }),
  })

  const { data: totalMes, isLoading: loadingTotal } = useQuery({
    queryKey: ['total-mes'],
    queryFn: () =>
      reportService.getTotalPeriodo({
        start_date: formatDateForInput(startOfMonth),
        end_date: formatDateForInput(endOfMonth),
      }),
  })

  const { data: aniversariantes, isLoading: loadingAniversariantes } = useQuery({
    queryKey: ['aniversariantes-hoje'],
    queryFn: () => reportService.getAniversariantes({ periodo: 'hoje' }),
  })

  if (loadingDizimistas || loadingContribuicoes || loadingTotal || loadingAniversariantes) {
    return <LoadingSpinner text="Carregando dashboard..." />
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Visão geral do sistema</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Dizimistas Ativos</p>
              <p className="text-3xl font-bold text-primary-600 mt-2">
                {dizimistasData?.total || 0}
              </p>
            </div>
            <div className="bg-primary-100 rounded-full p-3">
              <svg
                className="h-8 w-8 text-primary-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Contribuições</p>
              <p className="text-3xl font-bold text-primary-600 mt-2">
                {contribuicoesData?.total || 0}
              </p>
            </div>
            <div className="bg-green-100 rounded-full p-3">
              <svg
                className="h-8 w-8 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total do Mês</p>
              <p className="text-2xl font-bold text-primary-600 mt-2">
                {totalMes ? formatCurrency(totalMes.total) : 'R$ 0,00'}
              </p>
            </div>
            <div className="bg-blue-100 rounded-full p-3">
              <svg
                className="h-8 w-8 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                />
              </svg>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Aniversariantes Hoje</p>
              <p className="text-3xl font-bold text-primary-600 mt-2">
                {aniversariantes?.length || 0}
              </p>
            </div>
            <div className="bg-purple-100 rounded-full p-3">
              <svg
                className="h-8 w-8 text-purple-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zm-3-9v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2h12z"
                />
              </svg>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card title="Acesso Rápido">
          <div className="space-y-3">
            <Button fullWidth onClick={() => navigate('/dizimistas')}>
              Gerenciar Dizimistas
            </Button>
            <Button fullWidth variant="secondary" onClick={() => navigate('/contribuicoes')}>
              Registrar Contribuição
            </Button>
            <Button fullWidth variant="secondary" onClick={() => navigate('/aniversariantes')}>
              Ver Aniversariantes
            </Button>
          </div>
        </Card>

        <Card title="Aniversariantes de Hoje" className="md:col-span-2">
          {aniversariantes && aniversariantes.length > 0 ? (
            <div className="space-y-2">
              {aniversariantes.slice(0, 5).map((aniv) => (
                <div
                  key={aniv.id}
                  className="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
                >
                  <div>
                    <p className="font-medium text-gray-900">{aniv.nome}</p>
                    <p className="text-sm text-gray-500">{aniv.comunidade_nome}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-primary-600">{aniv.idade_completa}</p>
                    <p className="text-xs text-gray-500">anos</p>
                  </div>
                </div>
              ))}
              {aniversariantes.length > 5 && (
                <Button fullWidth variant="ghost" onClick={() => navigate('/aniversariantes')}>
                  Ver todos ({aniversariantes.length})
                </Button>
              )}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">
              Nenhum aniversariante hoje
            </p>
          )}
        </Card>
      </div>
    </div>
  )
}
