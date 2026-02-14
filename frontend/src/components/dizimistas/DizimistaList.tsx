import React from 'react'
import { Dizimista } from '../../types'
import { Table, Pagination } from '../ui/Table'
import { Button } from '../ui/Button'
import { formatPhone, formatCPF } from '../../utils/format'

interface DizimistaListProps {
  dizimistas: Dizimista[]
  isLoading: boolean
  currentPage: number
  totalPages: number
  totalItems: number
  itemsPerPage: number
  onPageChange: (page: number) => void
  onView: (dizimista: Dizimista) => void
  onEdit: (dizimista: Dizimista) => void
  onDeactivate: (dizimista: Dizimista) => void
}

export const DizimistaList: React.FC<DizimistaListProps> = ({
  dizimistas,
  isLoading,
  currentPage,
  totalPages,
  totalItems,
  itemsPerPage,
  onPageChange,
  onView,
  onEdit,
  onDeactivate,
}) => {
  const columns = [
    {
      header: 'Nome',
      accessor: (row: Dizimista) => (
        <div>
          <div className="font-medium text-gray-900">{row.nome}</div>
          {row.cpf && <div className="text-sm text-gray-500">{formatCPF(row.cpf)}</div>}
        </div>
      ),
    },
    {
      header: 'Telefone',
      accessor: (row: Dizimista) => (row.telefone ? formatPhone(row.telefone) : '-'),
    },
    {
      header: 'Email',
      accessor: (row: Dizimista) => row.email || '-',
    },
    {
      header: 'Comunidade',
      accessor: (row: Dizimista) => row.comunidade?.nome || '-',
    },
    {
      header: 'Status',
      accessor: (row: Dizimista) => (
        <span
          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
            row.ativo
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          }`}
        >
          {row.ativo ? 'Ativo' : 'Inativo'}
        </span>
      ),
    },
    {
      header: 'Ações',
      accessor: (row: Dizimista) => (
        <div className="flex space-x-2">
          <Button size="sm" variant="ghost" onClick={() => onView(row)}>
            Ver
          </Button>
          <Button size="sm" variant="ghost" onClick={() => onEdit(row)}>
            Editar
          </Button>
          {row.ativo && (
            <Button size="sm" variant="ghost" onClick={() => onDeactivate(row)}>
              Desativar
            </Button>
          )}
        </div>
      ),
    },
  ]

  return (
    <div className="space-y-4">
      <Table columns={columns} data={dizimistas} isLoading={isLoading} />

      {!isLoading && dizimistas.length > 0 && (
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
