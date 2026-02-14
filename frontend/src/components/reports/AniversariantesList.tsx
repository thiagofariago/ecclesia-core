import React from 'react'
import { Aniversariante } from '../../types'
import { Table } from '../ui/Table'
import { formatDate, formatPhone } from '../../utils/format'

interface AniversariantesListProps {
  aniversariantes: Aniversariante[]
  isLoading: boolean
}

export const AniversariantesList: React.FC<AniversariantesListProps> = ({
  aniversariantes,
  isLoading,
}) => {
  const columns = [
    {
      header: 'Nome',
      accessor: (row: Aniversariante) => row.nome,
    },
    {
      header: 'Data de Nascimento',
      accessor: (row: Aniversariante) => formatDate(row.data_nascimento),
    },
    {
      header: 'Idade',
      accessor: (row: Aniversariante) => `${row.idade_completa} anos`,
    },
    {
      header: 'Dias até Aniversário',
      accessor: (row: Aniversariante) => (
        <span
          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
            row.dias_ate_aniversario === 0
              ? 'bg-green-100 text-green-800'
              : row.dias_ate_aniversario <= 7
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-blue-100 text-blue-800'
          }`}
        >
          {row.dias_ate_aniversario === 0
            ? 'Hoje!'
            : `${row.dias_ate_aniversario} dias`}
        </span>
      ),
    },
    {
      header: 'Telefone',
      accessor: (row: Aniversariante) => (row.telefone ? formatPhone(row.telefone) : '-'),
    },
    {
      header: 'Comunidade',
      accessor: (row: Aniversariante) => row.comunidade_nome,
    },
  ]

  return (
    <Table
      columns={columns}
      data={aniversariantes}
      isLoading={isLoading}
      emptyMessage="Nenhum aniversariante encontrado no período selecionado"
    />
  )
}
