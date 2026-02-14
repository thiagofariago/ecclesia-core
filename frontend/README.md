# Ecclesia - Frontend

Sistema de Gestão de Dízimos - Interface Web

## Tecnologias

- **React 18** - Biblioteca UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool e dev server
- **TailwindCSS** - Framework CSS utilitário
- **React Router** - Roteamento
- **TanStack Query** - Gerenciamento de estado servidor
- **React Hook Form** - Gerenciamento de formulários
- **Zod** - Validação de schemas
- **Axios** - Cliente HTTP

## Estrutura do Projeto

```
src/
├── components/
│   ├── layout/          # Componentes de layout (Header, Sidebar, Layout)
│   ├── ui/              # Componentes UI reutilizáveis (Button, Input, etc.)
│   ├── dizimistas/      # Componentes específicos de Dizimistas
│   ├── contribuicoes/   # Componentes específicos de Contribuições
│   └── reports/         # Componentes de relatórios
├── pages/               # Páginas da aplicação
├── services/            # Serviços de API
├── hooks/               # Custom hooks (useAuth)
├── types/               # TypeScript types e interfaces
├── utils/               # Funções utilitárias (formatação)
├── App.tsx              # Componente raiz com rotas
├── main.tsx             # Entry point
└── index.css            # Estilos globais
```

## Funcionalidades Implementadas

### Autenticação
- Login com email e senha
- Proteção de rotas
- Logout
- Persistência de sessão

### Dizimistas
- Listagem paginada com filtros
- Busca por nome, telefone ou email
- Cadastro de novos dizimistas
- Edição de dados
- Visualização de detalhes
- Histórico de contribuições
- Desativação (soft delete)

### Contribuições
- Registro de contribuições (Dízimo/Oferta)
- Vinculação opcional a dizimista
- Filtros por data, tipo, comunidade
- Listagem paginada
- Múltiplas formas de pagamento

### Aniversariantes
- Listagem de aniversariantes
- Filtros: hoje, próximos 7 dias, mês atual
- Filtro por comunidade
- Exibição de idade e dias até aniversário

### Relatórios
- Total de contribuições por período
- Total por tipo (Dízimo vs Oferta)
- Filtros por data e comunidade

### Dashboard
- Cards com estatísticas gerais
- Total de dizimistas ativos
- Total de contribuições
- Total do mês atual
- Aniversariantes do dia
- Acesso rápido às funcionalidades

## Desenvolvimento

### Pré-requisitos

- Node.js 18+
- npm ou yarn

### Instalação

```bash
cd frontend
npm install
```

### Configuração

Crie o arquivo `.env`:

```env
VITE_API_URL=http://localhost:8000
```

### Executar em Desenvolvimento

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`

### Build para Produção

```bash
npm run build
```

Os arquivos otimizados estarão em `dist/`

### Preview da Build

```bash
npm run preview
```

## Docker

O frontend já está configurado para rodar em container Docker através do docker-compose na raiz do projeto.

```bash
# Da raiz do projeto
docker-compose up frontend
```

## Validações Implementadas

### Dizimistas
- Nome: obrigatório
- Email: formato válido (opcional)
- CPF: formato brasileiro 000.000.000-00 (opcional)
- Telefone: formato brasileiro (00) 00000-0000 (opcional)
- Comunidade: obrigatória

### Contribuições
- Comunidade: obrigatória
- Tipo: obrigatório (DIZIMO ou OFERTA)
- Valor: obrigatório, maior que zero
- Data: obrigatória

## Formatação

Todas as funções de formatação estão em `src/utils/format.ts`:

- `formatCurrency()` - Valores em R$
- `formatDate()` - Datas em pt-BR
- `formatCPF()` - CPF formatado
- `formatPhone()` - Telefone formatado
- `calculateAge()` - Cálculo de idade

## Integração com Backend

O frontend está configurado para consumir a API REST do backend através do Axios. Todas as chamadas são autenticadas com Bearer token.

Endpoints consumidos:
- `/api/auth/*` - Autenticação
- `/api/dizimistas/*` - CRUD de Dizimistas
- `/api/contribuicoes/*` - CRUD de Contribuições
- `/api/reports/*` - Relatórios
- `/api/comunidades/*` - Listagem de comunidades

## Responsividade

- Design mobile-first
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Tabelas com scroll horizontal em telas pequenas
- Menu lateral adaptável

## Acessibilidade

- Labels descritivos em formulários
- Indicadores de campos obrigatórios
- Feedback visual de erros
- Navegação por teclado
- Contraste adequado de cores

## Próximos Passos (TODOs)

Após o backend estar completo:

1. Testar integração completa com API real
2. Adicionar tratamento de erros mais específico
3. Implementar toast notifications para feedback
4. Adicionar mais relatórios (gráficos com Chart.js)
5. Implementar exportação de dados (Excel/PDF)
6. Adicionar testes unitários e E2E
7. Implementar PWA para uso offline
8. Adicionar suporte a múltiplas paróquias
9. Implementar sistema de permissões por role

## Notas de Desenvolvimento

- Todas as strings em português brasileiro
- TypeScript em modo strict
- Componentes funcionais com hooks
- Estado de servidor gerenciado com TanStack Query
- Estado local com useState
- Formulários com react-hook-form + zod
- Estilização com Tailwind classes utilitárias
