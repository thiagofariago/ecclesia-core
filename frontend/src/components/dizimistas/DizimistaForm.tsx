import React, { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Input } from '../ui/Input'
import { Select } from '../ui/Select'
import { Button } from '../ui/Button'
import { dizimistaService } from '../../services/dizimista.service'
import { comunidadeService } from '../../services/comunidade.service'
import { Dizimista, DizimistaCreate, DizimistaUpdate } from '../../types'
import { unformatCPF, unformatPhone, formatDateForInput } from '../../utils/format'

const dizimistaSchema = z.object({
  comunidade_id: z.number({ required_error: 'Comunidade é obrigatória' }),
  nome: z.string().min(1, 'Nome é obrigatório'),
  cpf: z.string().optional(),
  telefone: z.string().optional(),
  email: z.string().email('Email inválido').optional().or(z.literal('')),
  data_nascimento: z.string().optional().or(z.literal('')),
  endereco: z.string().optional(),
  observacoes: z.string().optional(),
})

type DizimistaFormData = z.infer<typeof dizimistaSchema>

interface DizimistaFormProps {
  dizimista?: Dizimista
  onSuccess: () => void
  onCancel: () => void
}

export const DizimistaForm: React.FC<DizimistaFormProps> = ({
  dizimista,
  onSuccess,
  onCancel,
}) => {
  const queryClient = useQueryClient()

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<DizimistaFormData>({
    resolver: zodResolver(dizimistaSchema),
    defaultValues: dizimista
      ? {
          comunidade_id: dizimista.comunidade_id,
          nome: dizimista.nome,
          cpf: dizimista.cpf || '',
          telefone: dizimista.telefone || '',
          email: dizimista.email || '',
          data_nascimento: dizimista.data_nascimento
            ? formatDateForInput(dizimista.data_nascimento)
            : '',
          endereco: dizimista.endereco || '',
          observacoes: dizimista.observacoes || '',
        }
      : undefined,
  })

  const { data: comunidades = [] } = useQuery({
    queryKey: ['comunidades'],
    queryFn: () => comunidadeService.list(),
  })

  const createMutation = useMutation({
    mutationFn: (data: DizimistaCreate) => dizimistaService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dizimistas'] })
      onSuccess()
    },
  })

  const updateMutation = useMutation({
    mutationFn: (data: DizimistaUpdate) => dizimistaService.update(dizimista!.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dizimistas'] })
      queryClient.invalidateQueries({ queryKey: ['dizimista', dizimista!.id] })
      onSuccess()
    },
  })

  const onSubmit = (data: DizimistaFormData) => {
    const formattedData = {
      ...data,
      cpf: data.cpf ? unformatCPF(data.cpf) : undefined,
      telefone: data.telefone ? unformatPhone(data.telefone) : undefined,
      email: data.email || undefined,
      data_nascimento: data.data_nascimento || undefined,
      endereco: data.endereco || undefined,
      observacoes: data.observacoes || undefined,
    }

    if (dizimista) {
      updateMutation.mutate(formattedData)
    } else {
      createMutation.mutate(formattedData as DizimistaCreate)
    }
  }

  const isLoading = createMutation.isPending || updateMutation.isPending
  const error = createMutation.error || updateMutation.error

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          Erro ao salvar dizimista. Por favor, tente novamente.
        </div>
      )}

      <Select
        label="Comunidade"
        required
        {...register('comunidade_id', { valueAsNumber: true })}
        error={errors.comunidade_id?.message}
        options={comunidades.map((c) => ({ value: c.id, label: c.nome }))}
        placeholder="Selecione uma comunidade"
      />

      <Input
        label="Nome Completo"
        required
        {...register('nome')}
        error={errors.nome?.message}
        placeholder="Digite o nome completo"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="CPF"
          {...register('cpf')}
          error={errors.cpf?.message}
          placeholder="000.000.000-00"
        />

        <Input
          label="Telefone"
          {...register('telefone')}
          error={errors.telefone?.message}
          placeholder="(00) 00000-0000"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Email"
          type="email"
          {...register('email')}
          error={errors.email?.message}
          placeholder="email@exemplo.com"
        />

        <Input
          label="Data de Nascimento"
          type="date"
          {...register('data_nascimento')}
          error={errors.data_nascimento?.message}
        />
      </div>

      <Input
        label="Endereço"
        {...register('endereco')}
        error={errors.endereco?.message}
        placeholder="Rua, número, bairro, cidade - UF"
      />

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
        <textarea
          {...register('observacoes')}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          placeholder="Informações adicionais..."
        />
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancelar
        </Button>
        <Button type="submit" isLoading={isLoading}>
          {dizimista ? 'Atualizar' : 'Cadastrar'}
        </Button>
      </div>
    </form>
  )
}
