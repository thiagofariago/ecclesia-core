// User and Auth Types
export interface User {
  id: number
  nome: string
  email: string
  role: string
  paroquia_id?: number
  comunidade_id?: number
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

// Paroquia Types
export interface Paroquia {
  id: number
  nome: string
  cnpj?: string
  endereco?: string
  telefone?: string
  email?: string
  diocese?: string
  created_at: string
  updated_at: string
}

export interface ParoquiaCreate {
  nome: string
  cnpj?: string
  endereco?: string
  telefone?: string
  email?: string
  diocese?: string
}

// Comunidade Types
export interface Comunidade {
  id: number
  paroquia_id: number
  nome: string
  endereco?: string
  telefone?: string
  responsavel?: string
  created_at: string
  updated_at: string
}

export interface ComunidadeCreate {
  paroquia_id: number
  nome: string
  endereco?: string
  telefone?: string
  responsavel?: string
}

// Dizimista Types
export interface Dizimista {
  id: number
  comunidade_id: number
  nome: string
  cpf?: string
  telefone?: string
  email?: string
  data_nascimento?: string
  endereco?: string
  ativo: boolean
  observacoes?: string
  created_at: string
  updated_at: string
  comunidade?: Comunidade
}

export interface DizimistaCreate {
  comunidade_id: number
  nome: string
  cpf?: string
  telefone?: string
  email?: string
  data_nascimento?: string
  endereco?: string
  observacoes?: string
}

export interface DizimistaUpdate {
  nome?: string
  cpf?: string
  telefone?: string
  email?: string
  data_nascimento?: string
  endereco?: string
  ativo?: boolean
  observacoes?: string
}

// Contribuicao Types
export enum TipoContribuicao {
  DIZIMO = 'DIZIMO',
  OFERTA = 'OFERTA',
}

export enum FormaPagamento {
  DINHEIRO = 'DINHEIRO',
  PIX = 'PIX',
  CARTAO = 'CARTAO',
  TRANSFERENCIA = 'TRANSFERENCIA',
  CHEQUE = 'CHEQUE',
}

export interface Contribuicao {
  id: number
  dizimista_id?: number
  comunidade_id: number
  tipo: TipoContribuicao
  valor: number
  data_contribuicao: string
  forma_pagamento?: FormaPagamento
  referencia_mes?: string
  observacoes?: string
  created_at: string
  updated_at: string
  dizimista?: Dizimista
  comunidade?: Comunidade
}

export interface ContribuicaoCreate {
  dizimista_id?: number
  comunidade_id: number
  tipo: TipoContribuicao
  valor: number
  data_contribuicao: string
  forma_pagamento?: FormaPagamento
  referencia_mes?: string
  observacoes?: string
}

// Report Types
export interface Aniversariante {
  id: number
  nome: string
  data_nascimento: string
  telefone?: string
  email?: string
  comunidade_id: number
  comunidade_nome: string
  dias_ate_aniversario: number
  idade_completa: number
}

export interface TotalPeriodoResponse {
  total: number
  start_date: string
  end_date: string
  comunidade_id?: number
}

export interface TotalTipoResponse {
  dizimo: number
  oferta: number
  total: number
  start_date: string
  end_date: string
  comunidade_id?: number
}

// Pagination Types
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface PaginationParams {
  page?: number
  page_size?: number
}

// Filter Types
export interface DizimistaFilters extends PaginationParams {
  search?: string
  comunidade_id?: number
  ativo?: boolean
}

export interface ContribuicaoFilters extends PaginationParams {
  dizimista_id?: number
  comunidade_id?: number
  tipo?: TipoContribuicao
  start_date?: string
  end_date?: string
}

export interface AniversariantesFilters {
  periodo?: 'hoje' | '7dias' | 'mes'
  comunidade_id?: number
}

export interface ReportFilters {
  start_date: string
  end_date: string
  comunidade_id?: number
}
