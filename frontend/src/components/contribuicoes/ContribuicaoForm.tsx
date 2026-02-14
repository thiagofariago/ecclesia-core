import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Input } from '../ui/Input'
import { Select } from '../ui/Select'
import { Button } from '../ui/Button'
import { contribuicaoService } from '../../services/contribuicao.service'
import { comunidadeService } from '../../services/comunidade.service'
import { dizimistaService } from '../../services/dizimista.service'
import { ContribuicaoCreate, TipoContribuicao, FormaPagamento } from '../../types'
import { formatDateForInput } from '../../utils/format'

const contribuicaoSchema = z.object({
  dizimista_id: z.number().optional(),
  comunidade_id: z.number({ required_error: 'Comunidade é obrigatória' }),
  tipo: z.nativeEnum(TipoContribuicao, { required_error: 'Tipo é obrigatório' }),
  valor: z.number({ required_error: 'Valor é obrigatório' }).min(0.01, 'Valor deve ser maior que zero'),
  data_contribuicao: z.string().min(1, 'Data é obrigatória'),
  forma_pagamento: z.nativeEnum(FormaPagamento).optional(),
  referencia_mes: z.string().optional().or(z.literal('')),
  observacoes: z.string().optional(),
})

type ContribuicaoFormData = z.infer<typeof contribuicaoSchema>

interface ContribuicaoFormProps {
  onSuccess: () => void
  onCancel: () => void
}

export const ContribuicaoForm: React.FC<ContribuicaoFormProps> = ({ onSuccess, onCancel }) => {
  const queryClient = useQueryClient()
  const [dizimistaSearch, setDizimistaSearch] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<ContribuicaoFormData>({
    resolver: zodResolver(contribuicaoSchema),
    defaultValues: {
      data_contribuicao: formatDateForInput(new Date()),
    },
  })

  const { data: comunidades = [] } = useQuery({
    queryKey: ['comunidades'],
    queryFn: () => comunidadeService.list(),
  })

  const { data: dizimistas = [] } = useQuery({
    queryKey: ['dizimistas-search', dizimistaSearch],
    queryFn: () => dizimistaService.search(dizimistaSearch),
    enabled: dizimistaSearch.length >= 2,
  })

  const createMutation = useMutation({
    mutationFn: (data: ContribuicaoCreate) => contribuicaoService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contribuicoes'] })
      onSuccess()
    },
  })

  const onSubmit = (data: ContribuicaoFormData) => {
    const formattedData: ContribuicaoCreate = {
      ...data,
      dizimista_id: data.dizimista_id || undefined,
      forma_pagamento: data.forma_pagamento || undefined,
      referencia_mes: data.referencia_mes || undefined,
      observacoes: data.observacoes || undefined,
    }

    createMutation.mutate(formattedData)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {createMutation.error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          Erro ao registrar contribuição. Por favor, tente novamente.
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

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Dizimista (opcional)
        </label>
        <Input
          placeholder="Buscar dizimista..."
          value={dizimistaSearch}
          onChange={(e) => setDizimistaSearch(e.target.value)}
          helperText="Digite ao menos 2 caracteres para buscar"
        />
        {dizimistas.length > 0 && (
          <select
            {...register('dizimista_id', { valueAsNumber: true })}
            className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-lg"
          >
            <option value="">Contribuição anônima</option>
            {dizimistas.map((d) => (
              <option key={d.id} value={d.id}>
                {d.nome} - {d.telefone}
              </option>
            ))}
          </select>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label="Tipo"
          required
          {...register('tipo')}
          error={errors.tipo?.message}
          options={[
            { value: TipoContribuicao.DIZIMO, label: 'Dízimo' },
            { value: TipoContribuicao.OFERTA, label: 'Oferta' },
          ]}
          placeholder="Selecione o tipo"
        />

        <Input
          label="Valor"
          type="number"
          step="0.01"
          required
          {...register('valor', { valueAsNumber: true })}
          error={errors.valor?.message}
          placeholder="0.00"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Data da Contribuição"
          type="date"
          required
          {...register('data_contribuicao')}
          error={errors.data_contribuicao?.message}
        />

        <Select
          label="Forma de Pagamento"
          {...register('forma_pagamento')}
          error={errors.forma_pagamento?.message}
          options={[
            { value: FormaPagamento.DINHEIRO, label: 'Dinheiro' },
            { value: FormaPagamento.PIX, label: 'PIX' },
            { value: FormaPagamento.CARTAO, label: 'Cartão' },
            { value: FormaPagamento.TRANSFERENCIA, label: 'Transferência' },
            { value: FormaPagamento.CHEQUE, label: 'Cheque' },
          ]}
          placeholder="Selecione a forma"
        />
      </div>

      <Input
        label="Referência Mês"
        type="month"
        {...register('referencia_mes')}
        error={errors.referencia_mes?.message}
        helperText="Exemplo: 2024-01 para Janeiro/2024"
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
        <Button type="submit" isLoading={createMutation.isPending}>
          Registrar Contribuição
        </Button>
      </div>
    </form>
  )
}
