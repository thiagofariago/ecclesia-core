import React from 'react'
import { RelatorioSimples } from '../components/reports/RelatorioSimples'

export const RelatoriosPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Relatórios</h1>
        <p className="text-gray-600 mt-2">Visualize relatórios financeiros e estatísticas</p>
      </div>

      <RelatorioSimples />
    </div>
  )
}
