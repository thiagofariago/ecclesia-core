import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { Input } from '../ui/Input'
import { Select } from '../ui/Select'
import { comunidadeService } from '../../services/comunidade.service'

interface DizimistaSearchProps {
  search: string
  onSearchChange: (value: string) => void
  comunidadeId: number | undefined
  onComunidadeChange: (value: number | undefined) => void
  ativo: boolean | undefined
  onAtivoChange: (value: boolean | undefined) => void
}

export const DizimistaSearch: React.FC<DizimistaSearchProps> = ({
  search,
  onSearchChange,
  comunidadeId,
  onComunidadeChange,
  ativo,
  onAtivoChange,
}) => {
  const { data: comunidades = [] } = useQuery({
    queryKey: ['comunidades'],
    queryFn: () => comunidadeService.list(),
  })

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Input
        label="Buscar"
        placeholder="Nome, telefone ou email..."
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
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

      <Select
        label="Status"
        value={ativo === undefined ? '' : ativo ? 'true' : 'false'}
        onChange={(e) => {
          const value = e.target.value
          onAtivoChange(value === '' ? undefined : value === 'true')
        }}
        options={[
          { value: 'true', label: 'Ativos' },
          { value: 'false', label: 'Inativos' },
        ]}
        placeholder="Todos"
      />
    </div>
  )
}
