import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import api from '../services/api'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Modal } from '../components/ui/Modal'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'

interface Paroquia {
  id: number
  nome: string
  criado_em: string
  atualizado_em: string
}

const paroquiaSchema = z.object({
  nome: z.string().min(3, 'Nome deve ter no mínimo 3 caracteres'),
})

type ParoquiaFormData = z.infer<typeof paroquiaSchema>

export const ParoquiasPage: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingParoquia, setEditingParoquia] = useState<Paroquia | null>(null)
  const queryClient = useQueryClient()

  const { data: paroquias, isLoading } = useQuery<Paroquia[]>({
    queryKey: ['paroquias'],
    queryFn: async () => {
      const { data } = await api.get('/api/paroquias')
      return data
    },
  })

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ParoquiaFormData>({
    resolver: zodResolver(paroquiaSchema),
  })

  const createMutation = useMutation({
    mutationFn: async (data: ParoquiaFormData) => {
      return api.post('/api/paroquias', data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['paroquias'] })
      setIsModalOpen(false)
      reset()
    },
  })

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: ParoquiaFormData }) => {
      return api.patch(`/api/paroquias/${id}`, data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['paroquias'] })
      setIsModalOpen(false)
      setEditingParoquia(null)
      reset()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      return api.delete(`/api/paroquias/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['paroquias'] })
    },
  })

  const onSubmit = (data: ParoquiaFormData) => {
    if (editingParoquia) {
      updateMutation.mutate({ id: editingParoquia.id, data })
    } else {
      createMutation.mutate(data)
    }
  }

  const handleEdit = (paroquia: Paroquia) => {
    setEditingParoquia(paroquia)
    reset({ nome: paroquia.nome })
    setIsModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir esta paróquia? Todas as comunidades vinculadas serão afetadas.')) {
      deleteMutation.mutate(id)
    }
  }

  const handleNew = () => {
    setEditingParoquia(null)
    reset({ nome: '' })
    setIsModalOpen(true)
  }

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
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Paróquias</h1>
          <p className="text-gray-600 mt-1">Gerencie as paróquias do sistema</p>
        </div>
        <Button onClick={handleNew}>+ Nova Paróquia</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {paroquias?.map((paroquia) => (
          <Card key={paroquia.id}>
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {paroquia.nome}
              </h3>
              <div className="text-sm text-gray-600 mb-4">
                <p>Criada em: {new Date(paroquia.criado_em).toLocaleDateString('pt-BR')}</p>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  onClick={() => handleEdit(paroquia)}
                  className="flex-1"
                >
                  Editar
                </Button>
                <Button
                  variant="danger"
                  onClick={() => handleDelete(paroquia.id)}
                  className="flex-1"
                >
                  Excluir
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {paroquias?.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg">Nenhuma paróquia cadastrada.</p>
          <Button onClick={handleNew} className="mt-4">
            Criar primeira paróquia
          </Button>
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false)
          setEditingParoquia(null)
          reset()
        }}
        title={editingParoquia ? 'Editar Paróquia' : 'Nova Paróquia'}
      >
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <Input
            label="Nome da Paróquia"
            {...register('nome')}
            error={errors.nome?.message}
            placeholder="Ex: Paróquia Sagrada Família"
          />

          <div className="flex gap-2 justify-end mt-6">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsModalOpen(false)
                setEditingParoquia(null)
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
                : editingParoquia
                ? 'Atualizar'
                : 'Criar'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
