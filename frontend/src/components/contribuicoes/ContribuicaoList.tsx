import React from 'react'
import { Contribuicao } from '../../types'
import { Table, Pagination } from '../ui/Table'
import { formatCurrency, formatDate } from '../../utils/format'

interface ContribuicaoListProps {
  contribuicoes: Contribuicao[]
  isLoading: boolean
  currentPage: number
  totalPages: number
  totalItems: number
  itemsPerPage: number
  onPageChange: (page: number) => void
}

export const ContribuicaoList: React.FC<ContribuicaoListProps> = ({
  contribuicoes,
  isLoading,
  currentPage,
  totalPages,
  totalItems,
  itemsPerPage,
  onPageChange,
}) => {
  const columns = [
    {
      header: 'Data',
      accessor: (row: Contribuicao) => formatDate(row.data_contribuicao),
    },
    {
      header: 'Dizimista',
      accessor: (row: Contribuicao) => row.dizimista?.nome || 'Anônimo',
    },
    {
      header: 'Comunidade',
      accessor: (row: Contribuicao) => row.comunidade?.nome || '-',
    },
    {
      header: 'Tipo',
      accessor: (row: Contribuicao) => (
        <span
          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
            row.tipo === 'DIZIMO'
              ? 'bg-blue-100 text-blue-800'
              : 'bg-purple-100 text-purple-800'
          }`}
        >
          {row.tipo === 'DIZIMO' ? 'Dízimo' : 'Oferta'}
        </span>
      ),
    },
    {
      header: 'Valor',
      accessor: (row: Contribuicao) => (
        <span className="font-medium text-gray-900">{formatCurrency(row.valor)}</span>
      ),
    },
    {
      header: 'Forma de Pagamento',
      accessor: (row: Contribuicao) => row.forma_pagamento || '-',
    },
  ]

  return (
    <div className="space-y-4">
      <Table columns={columns} data={contribuicoes} isLoading={isLoading} />

      {!isLoading && contribuicoes.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          totalItems={totalItems}
          itemsPerPage={itemsPerPage}
          onPageChange={onPageChange}
        />
      )}
    </div>
  )
}
