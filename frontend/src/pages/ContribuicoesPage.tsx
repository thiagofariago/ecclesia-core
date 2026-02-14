import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Modal } from '../components/ui/Modal'
import { Input } from '../components/ui/Input'
import { Select } from '../components/ui/Select'
import { ContribuicaoForm } from '../components/contribuicoes/ContribuicaoForm'
import { ContribuicaoList } from '../components/contribuicoes/ContribuicaoList'
import { contribuicaoService } from '../services/contribuicao.service'
import { comunidadeService } from '../services/comunidade.service'
import { TipoContribuicao } from '../types'
import { formatDateForInput } from '../utils/format'

export const ContribuicoesPage: React.FC = () => {
  const [page, setPage] = useState(1)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [comunidadeId, setComunidadeId] = useState<number | undefined>()
  const [tipo, setTipo] = useState<TipoContribuicao | undefined>()
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const { data, isLoading } = useQuery({
    queryKey: ['contribuicoes', { page, comunidadeId, tipo, startDate, endDate }],
    queryFn: () =>
      contribuicaoService.list({
        page,
        page_size: 20,
        comunidade_id: comunidadeId,
        tipo,
        start_date: startDate || undefined,
        end_date: endDate || undefined,
      }),
  })

  const { data: comunidades = [] } = useQuery({
    queryKey: ['comunidades'],
    queryFn: () => comunidadeService.list(),
  })

  const handleCreateSuccess = () => {
    setShowCreateModal(false)
    setPage(1)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Contribuições</h1>
          <p className="text-gray-600 mt-2">Registre e gerencie contribuições</p>
        </div>
        <Button onClick={() => setShowCreateModal(true)}>
          Registrar Contribuição
        </Button>
      </div>

      <Card title="Filtros">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Select
            label="Comunidade"
            value={comunidadeId || ''}
            onChange={(e) =>
              setComunidadeId(e.target.value ? Number(e.target.value) : undefined)
            }
            options={comunidades.map((c) => ({ value: c.id, label: c.nome }))}
            placeholder="Todas"
          />

          <Select
            label="Tipo"
            value={tipo || ''}
            onChange={(e) =>
              setTipo(e.target.value ? (e.target.value as TipoContribuicao) : undefined)
            }
            options={[
              { value: TipoContribuicao.DIZIMO, label: 'Dízimo' },
              { value: TipoContribuicao.OFERTA, label: 'Oferta' },
            ]}
            placeholder="Todos"
          />

          <Input
            label="Data Inicial"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />

          <Input
            label="Data Final"
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
      </Card>

      <Card>
        <ContribuicaoList
          contribuicoes={data?.items || []}
          isLoading={isLoading}
          currentPage={page}
          totalPages={data?.pages || 1}
          totalItems={data?.total || 0}
          itemsPerPage={data?.page_size || 20}
          onPageChange={setPage}
        />
      </Card>

      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Registrar Contribuição"
        size="lg"
      >
        <ContribuicaoForm
          onSuccess={handleCreateSuccess}
          onCancel={() => setShowCreateModal(false)}
        />
      </Modal>
    </div>
  )
}
