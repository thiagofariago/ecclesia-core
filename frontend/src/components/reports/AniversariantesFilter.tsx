import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { Select } from '../ui/Select'
import { comunidadeService } from '../../services/comunidade.service'

interface AniversariantesFilterProps {
  periodo: 'hoje' | '7dias' | 'mes'
  onPeriodoChange: (value: 'hoje' | '7dias' | 'mes') => void
  comunidadeId: number | undefined
  onComunidadeChange: (value: number | undefined) => void
}

export const AniversariantesFilter: React.FC<AniversariantesFilterProps> = ({
  periodo,
  onPeriodoChange,
  comunidadeId,
  onComunidadeChange,
}) => {
  const { data: comunidades = [] } = useQuery({
    queryKey: ['comunidades'],
    queryFn: () => comunidadeService.list(),
  })

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Select
        label="Período"
        value={periodo}
        onChange={(e) => onPeriodoChange(e.target.value as 'hoje' | '7dias' | 'mes')}
        options={[
          { value: 'hoje', label: 'Hoje' },
          { value: '7dias', label: 'Próximos 7 dias' },
          { value: 'mes', label: 'Mês atual' },
        ]}
      />

      <Select
        label="Comunidade"
        value={comunidadeId || ''}
        onChange={(e) =>
          onComunidadeChange(e.target.value ? Number(e.target.value) : undefined)
        }
        options={comunidades.map((c) => ({ value: c.id, label: c.nome }))}
        placeholder="Todas as comunidades"
      />
    </div>
  )
}
