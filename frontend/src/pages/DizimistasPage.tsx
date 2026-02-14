import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Modal } from '../components/ui/Modal'
import { DizimistaList } from '../components/dizimistas/DizimistaList'
import { DizimistaForm } from '../components/dizimistas/DizimistaForm'
import { DizimistaSearch } from '../components/dizimistas/DizimistaSearch'
import { DizimistaDetail } from '../components/dizimistas/DizimistaDetail'
import { dizimistaService } from '../services/dizimista.service'
import { Dizimista } from '../types'

export const DizimistasPage: React.FC = () => {
  const queryClient = useQueryClient()
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [comunidadeId, setComunidadeId] = useState<number | undefined>()
  const [ativo, setAtivo] = useState<boolean | undefined>(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [selectedDizimista, setSelectedDizimista] = useState<Dizimista | null>(null)

  const { data, isLoading } = useQuery({
    queryKey: ['dizimistas', { page, search, comunidadeId, ativo }],
    queryFn: () =>
      dizimistaService.list({
        page,
        page_size: 20,
        search: search || undefined,
        comunidade_id: comunidadeId,
        ativo,
      }),
  })

  const deactivateMutation = useMutation({
    mutationFn: (id: number) => dizimistaService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dizimistas'] })
    },
  })

  const handleView = (dizimista: Dizimista) => {
    setSelectedDizimista(dizimista)
    setShowDetailModal(true)
  }

  const handleEdit = (dizimista: Dizimista) => {
    setSelectedDizimista(dizimista)
    setShowEditModal(true)
  }

  const handleDeactivate = (dizimista: Dizimista) => {
    if (window.confirm(`Deseja realmente desativar ${dizimista.nome}?`)) {
      deactivateMutation.mutate(dizimista.id)
    }
  }

  const handleCreateSuccess = () => {
    setShowCreateModal(false)
    setPage(1)
  }

  const handleEditSuccess = () => {
    setShowEditModal(false)
    setSelectedDizimista(null)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dizimistas</h1>
          <p className="text-gray-600 mt-2">Gerencie os dizimistas da paróquia</p>
        </div>
        <Button onClick={() => setShowCreateModal(true)}>
          Novo Dizimista
        </Button>
      </div>

      <Card>
        <DizimistaSearch
          search={search}
          onSearchChange={setSearch}
          comunidadeId={comunidadeId}
          onComunidadeChange={setComunidadeId}
          ativo={ativo}
          onAtivoChange={setAtivo}
        />
      </Card>

      <Card>
        <DizimistaList
          dizimistas={data?.items || []}
          isLoading={isLoading}
          currentPage={page}
          totalPages={data?.pages || 1}
          totalItems={data?.total || 0}
          itemsPerPage={data?.page_size || 20}
          onPageChange={setPage}
          onView={handleView}
          onEdit={handleEdit}
          onDeactivate={handleDeactivate}
        />
      </Card>

      {/* Create Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Novo Dizimista"
        size="lg"
      >
        <DizimistaForm
          onSuccess={handleCreateSuccess}
          onCancel={() => setShowCreateModal(false)}
        />
      </Modal>

      {/* Edit Modal */}
      <Modal
        isOpen={showEditModal}
        onClose={() => {
          setShowEditModal(false)
          setSelectedDizimista(null)
        }}
        title="Editar Dizimista"
        size="lg"
      >
        {selectedDizimista && (
          <DizimistaForm
            dizimista={selectedDizimista}
            onSuccess={handleEditSuccess}
            onCancel={() => {
              setShowEditModal(false)
              setSelectedDizimista(null)
            }}
          />
        )}
      </Modal>

      {/* Detail Modal */}
      <Modal
        isOpen={showDetailModal}
        onClose={() => {
          setShowDetailModal(false)
          setSelectedDizimista(null)
        }}
        title="Detalhes do Dizimista"
        size="lg"
      >
        {selectedDizimista && <DizimistaDetail dizimista={selectedDizimista} />}
      </Modal>
    </div>
  )
}
