import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import api from '../services/api'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Select } from '../components/ui/Select'
import { Modal } from '../components/ui/Modal'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'

interface Paroquia {
  id: number
  nome: string
}

interface Comunidade {
  id: number
  nome: string
  paroquia_id: number
  criado_em: string
  atualizado_em: string
  paroquia?: Paroquia
}

const comunidadeSchema = z.object({
  nome: z.string().min(3, 'Nome deve ter no mínimo 3 caracteres'),
  paroquia_id: z.coerce.number().min(1, 'Selecione uma paróquia'),
})

type ComunidadeFormData = z.infer<typeof comunidadeSchema>

export const ComunidadesPage: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingComunidade, setEditingComunidade] = useState<Comunidade | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const queryClient = useQueryClient()

  const { data: paroquias } = useQuery<Paroquia[]>({
    queryKey: ['paroquias'],
    queryFn: async () => {
      const { data } = await api.get('/api/paroquias')
      return data
    },
  })

  const { data: comunidades, isLoading } = useQuery<Comunidade[]>({
    queryKey: ['comunidades'],
    queryFn: async () => {
      const { data } = await api.get('/api/comunidades')
      return data
    },
  })

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ComunidadeFormData>({
    resolver: zodResolver(comunidadeSchema),
  })

  const createMutation = useMutation({
    mutationFn: async (data: ComunidadeFormData) => {
      return api.post('/api/comunidades', data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comunidades'] })
      setIsModalOpen(false)
      reset()
    },
  })

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: ComunidadeFormData }) => {
      return api.patch(`/api/comunidades/${id}`, data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comunidades'] })
      setIsModalOpen(false)
      setEditingComunidade(null)
      reset()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      return api.delete(`/api/comunidades/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comunidades'] })
    },
  })

  const onSubmit = (data: ComunidadeFormData) => {
    if (editingComunidade) {
      updateMutation.mutate({ id: editingComunidade.id, data })
    } else {
      createMutation.mutate(data)
    }
  }

  const handleEdit = (comunidade: Comunidade) => {
    setEditingComunidade(comunidade)
    reset({
      nome: comunidade.nome,
      paroquia_id: comunidade.paroquia_id,
    })
    setIsModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir esta comunidade?')) {
      deleteMutation.mutate(id)
    }
  }

  const handleNew = () => {
    setEditingComunidade(null)
    reset({
      nome: '',
      paroquia_id: paroquias?.[0]?.id || 1
    })
    setIsModalOpen(true)
  }

  const getParoquiaNome = (paroquiaId: number) => {
    return paroquias?.find(p => p.id === paroquiaId)?.nome || 'N/A'
  }

  const filteredComunidades = comunidades?.filter((c) =>
    c.nome.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Comunidades</h1>
        <Button onClick={handleNew}>+ Nova Comunidade</Button>
      </div>

      <Card>
        <div className="p-4">
          <Input
            placeholder="Buscar comunidade..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredComunidades?.map((comunidade) => (
          <Card key={comunidade.id}>
            <div className="p-6">
              <div className="mb-2">
                <span className="text-xs font-medium text-primary-600 bg-primary-50 px-2 py-1 rounded">
                  {getParoquiaNome(comunidade.paroquia_id)}
                </span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {comunidade.nome}
              </h3>
              <div className="text-sm text-gray-600 mb-4">
                <p>Criada em: {new Date(comunidade.criado_em).toLocaleDateString('pt-BR')}</p>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  onClick={() => handleEdit(comunidade)}
                  className="flex-1"
                >
                  Editar
                </Button>
                <Button
                  variant="danger"
                  onClick={() => handleDelete(comunidade.id)}
                  className="flex-1"
                >
                  Excluir
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {filteredComunidades?.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg">Nenhuma comunidade encontrada.</p>
          <Button onClick={handleNew} className="mt-4">
            Criar primeira comunidade
          </Button>
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false)
          setEditingComunidade(null)
          reset()
        }}
        title={editingComunidade ? 'Editar Comunidade' : 'Nova Comunidade'}
      >
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <Select
            label="Paróquia"
            {...register('paroquia_id')}
            error={errors.paroquia_id?.message}
          >
            <option value="">Selecione a paróquia...</option>
            {paroquias?.map((paroquia) => (
              <option key={paroquia.id} value={paroquia.id}>
                {paroquia.nome}
              </option>
            ))}
          </Select>

          <Input
            label="Nome da Comunidade"
            {...register('nome')}
            error={errors.nome?.message}
            placeholder="Ex: Comunidade Nossa Senhora de Guadalupe"
          />

          <div className="flex gap-2 justify-end mt-6">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsModalOpen(false)
                setEditingComunidade(null)
                reset()
              }}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              disabled={createMutation.isPending || updateMutation.isPending}
            >
              {createMutation.isPending || updateMutation.isPending
                ? 'Salvando...'
                : editingComunidade
                ? 'Atualizar'
                : 'Criar'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
