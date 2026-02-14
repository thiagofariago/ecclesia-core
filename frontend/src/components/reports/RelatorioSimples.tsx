import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { Card } from '../ui/Card'
import { Input } from '../ui/Input'
import { Select } from '../ui/Select'
import { Button } from '../ui/Button'
import { LoadingSpinner } from '../ui/LoadingSpinner'
import { reportService } from '../../services/report.service'
import { comunidadeService } from '../../services/comunidade.service'
import { formatCurrency, formatDateForInput } from '../../utils/format'

interface ReportFormData {
  start_date: string
  end_date: string
  comunidade_id: number | ''
}

export const RelatorioSimples: React.FC = () => {
  const { register, watch, handleSubmit } = useForm<ReportFormData>({
    defaultValues: {
      start_date: formatDateForInput(new Date(new Date().getFullYear(), new Date().getMonth(), 1)),
      end_date: formatDateForInput(new Date()),
      comunidade_id: '',
    },
  })

  const formData = watch()
  const [shouldFetch, setShouldFetch] = React.useState(false)

  const { data: comunidades = [] } = useQuery({
    queryKey: ['comunidades'],
    queryFn: () => comunidadeService.list(),
  })

  const { data: totalPeriodo, isLoading: loadingPeriodo } = useQuery({
    queryKey: ['total-periodo', formData],
    queryFn: () =>
      reportService.getTotalPeriodo({
        start_date: formData.start_date,
        end_date: formData.end_date,
        comunidade_id: formData.comunidade_id || undefined,
      }),
    enabled: shouldFetch && !!formData.start_date && !!formData.end_date,
  })

  const { data: totalTipo, isLoading: loadingTipo } = useQuery({
    queryKey: ['total-tipo', formData],
    queryFn: () =>
      reportService.getTotalTipo({
        start_date: formData.start_date,
        end_date: formData.end_date,
        comunidade_id: formData.comunidade_id || undefined,
      }),
    enabled: shouldFetch && !!formData.start_date && !!formData.end_date,
  })

  const onSubmit = () => {
    setShouldFetch(true)
  }

  return (
    <div className="space-y-6">
      <Card title="Filtros do Relatório">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Data Inicial"
              type="date"
              required
              {...register('start_date')}
            />

            <Input
              label="Data Final"
              type="date"
              required
              {...register('end_date')}
            />
          </div>

          <Select
            label="Comunidade"
            {...register('comunidade_id')}
            options={comunidades.map((c) => ({ value: c.id, label: c.nome }))}
            placeholder="Todas as comunidades"
          />

          <Button type="submit" fullWidth>
            Gerar Relatório
          </Button>
        </form>
      </Card>

      {shouldFetch && (
        <>
          {loadingPeriodo || loadingTipo ? (
            <LoadingSpinner text="Gerando relatório..." />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card title="Total do Período">
                <div className="text-center">
                  <p className="text-4xl font-bold text-primary-600">
                    {totalPeriodo ? formatCurrency(totalPeriodo.total) : 'R$ 0,00'}
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    Total de contribuições
                  </p>
                </div>
              </Card>

              <Card title="Total por Tipo">
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">Dízimo:</span>
                    <span className="text-lg font-semibold text-blue-600">
                      {totalTipo ? formatCurrency(totalTipo.dizimo) : 'R$ 0,00'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">Oferta:</span>
                    <span className="text-lg font-semibold text-purple-600">
                      {totalTipo ? formatCurrency(totalTipo.oferta) : 'R$ 0,00'}
                    </span>
                  </div>
                  <div className="border-t pt-4 flex justify-between items-center">
                    <span className="text-gray-900 font-medium">Total:</span>
                    <span className="text-xl font-bold text-primary-600">
                      {totalTipo ? formatCurrency(totalTipo.total) : 'R$ 0,00'}
                    </span>
                  </div>
                </div>
              </Card>
            </div>
          )}
        </>
      )}
    </div>
  )
}
