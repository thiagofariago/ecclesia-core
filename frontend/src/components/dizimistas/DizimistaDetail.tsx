import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { Dizimista } from '../../types'
import { reportService } from '../../services/report.service'
import { LoadingSpinner } from '../ui/LoadingSpinner'
import { formatCurrency, formatDate, formatPhone, formatCPF, calculateAge } from '../../utils/format'

interface DizimistaDetailProps {
  dizimista: Dizimista
}

export const DizimistaDetail: React.FC<DizimistaDetailProps> = ({ dizimista }) => {
  const { data: historico, isLoading } = useQuery({
    queryKey: ['dizimista-historico', dizimista.id],
    queryFn: () => reportService.getDizimistaHistorico(dizimista.id),
  })

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h3 className="text-sm font-medium text-gray-500">Nome Completo</h3>
          <p className="mt-1 text-base text-gray-900">{dizimista.nome}</p>
        </div>

        <div>
          <h3 className="text-sm font-medium text-gray-500">Comunidade</h3>
          <p className="mt-1 text-base text-gray-900">{dizimista.comunidade?.nome || '-'}</p>
        </div>

        {dizimista.cpf && (
          <div>
            <h3 className="text-sm font-medium text-gray-500">CPF</h3>
            <p className="mt-1 text-base text-gray-900">{formatCPF(dizimista.cpf)}</p>
          </div>
        )}

        {dizimista.telefone && (
          <div>
            <h3 className="text-sm font-medium text-gray-500">Telefone</h3>
            <p className="mt-1 text-base text-gray-900">{formatPhone(dizimista.telefone)}</p>
          </div>
        )}

        {dizimista.email && (
          <div>
            <h3 className="text-sm font-medium text-gray-500">Email</h3>
            <p className="mt-1 text-base text-gray-900">{dizimista.email}</p>
          </div>
        )}

        {dizimista.data_nascimento && (
          <div>
            <h3 className="text-sm font-medium text-gray-500">Data de Nascimento</h3>
            <p className="mt-1 text-base text-gray-900">
              {formatDate(dizimista.data_nascimento)} ({calculateAge(dizimista.data_nascimento)}{' '}
              anos)
            </p>
          </div>
        )}

        {dizimista.endereco && (
          <div className="md:col-span-2">
            <h3 className="text-sm font-medium text-gray-500">Endereço</h3>
            <p className="mt-1 text-base text-gray-900">{dizimista.endereco}</p>
          </div>
        )}

        <div>
          <h3 className="text-sm font-medium text-gray-500">Status</h3>
          <p className="mt-1">
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                dizimista.ativo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}
            >
              {dizimista.ativo ? 'Ativo' : 'Inativo'}
            </span>
          </p>
        </div>

        {dizimista.observacoes && (
          <div className="md:col-span-2">
            <h3 className="text-sm font-medium text-gray-500">Observações</h3>
            <p className="mt-1 text-base text-gray-900">{dizimista.observacoes}</p>
          </div>
        )}
      </div>

      <div className="border-t pt-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Histórico de Contribuições</h3>
        {isLoading ? (
          <LoadingSpinner size="sm" text="Carregando histórico..." />
        ) : historico && historico.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Data
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Tipo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Valor
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Forma de Pagamento
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {historico.map((contrib) => (
                  <tr key={contrib.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(contrib.data_contribuicao)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {contrib.tipo}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {formatCurrency(contrib.valor)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {contrib.forma_pagamento || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500 text-center py-4">Nenhuma contribuição registrada</p>
        )}
      </div>
    </div>
  )
}
