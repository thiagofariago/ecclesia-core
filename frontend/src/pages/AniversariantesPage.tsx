import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card } from '../components/ui/Card'
import { AniversariantesFilter } from '../components/reports/AniversariantesFilter'
import { AniversariantesList } from '../components/reports/AniversariantesList'
import { reportService } from '../services/report.service'

export const AniversariantesPage: React.FC = () => {
  const [periodo, setPeriodo] = useState<'hoje' | '7dias' | 'mes'>('mes')
  const [comunidadeId, setComunidadeId] = useState<number | undefined>()

  const { data: aniversariantes = [], isLoading } = useQuery({
    queryKey: ['aniversariantes', { periodo, comunidadeId }],
    queryFn: () => reportService.getAniversariantes({ periodo, comunidade_id: comunidadeId }),
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Aniversariantes</h1>
        <p className="text-gray-600 mt-2">Veja os aniversariantes do período selecionado</p>
      </div>

      <Card>
        <AniversariantesFilter
          periodo={periodo}
          onPeriodoChange={setPeriodo}
          comunidadeId={comunidadeId}
          onComunidadeChange={setComunidadeId}
        />
      </Card>

      <Card>
        <AniversariantesList aniversariantes={aniversariantes} isLoading={isLoading} />
      </Card>
    </div>
  )
}
