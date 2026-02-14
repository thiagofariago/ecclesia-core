# Ecclesia API - Quick Reference Guide

## Base URL
```
http://localhost:8000
```

## Authentication

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@ecclesia.com",
  "senha": "Admin123!"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Use Token
```http
GET /api/auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Paróquias (Parishes)

### List All
```http
GET /api/paroquias
Authorization: Bearer {token}
```

### Create
```http
POST /api/paroquias
Authorization: Bearer {token}
Content-Type: application/json

{
  "nome": "Paróquia São João"
}
```

### Get by ID
```http
GET /api/paroquias/{id}
Authorization: Bearer {token}
```

### Update
```http
PATCH /api/paroquias/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "nome": "Novo Nome"
}
```

### Delete
```http
DELETE /api/paroquias/{id}
Authorization: Bearer {token}
```

## Comunidades (Communities)

### List All (with optional filter)
```http
GET /api/comunidades?paroquia_id=1
Authorization: Bearer {token}
```

### Create
```http
POST /api/comunidades
Authorization: Bearer {token}
Content-Type: application/json

{
  "nome": "Comunidade São Pedro",
  "paroquia_id": 1
}
```

### Get by ID
```http
GET /api/comunidades/{id}
Authorization: Bearer {token}
```

### Update
```http
PATCH /api/comunidades/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "nome": "Novo Nome"
}
```

### Delete
```http
DELETE /api/comunidades/{id}
Authorization: Bearer {token}
```

## Dizimistas (Tithing Members)

### List with Pagination and Filters
```http
GET /api/dizimistas?page=1&page_size=20&search=João&comunidade_id=1&ativo=true
Authorization: Bearer {token}

Response:
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

### Create
```http
POST /api/dizimistas
Authorization: Bearer {token}
Content-Type: application/json

{
  "nome": "João da Silva",
  "comunidade_id": 1,
  "cpf": "123.456.789-01",
  "telefone": "(11) 98765-4321",
  "email": "joao@example.com",
  "data_nascimento": "1975-05-10",
  "endereco": "Rua das Flores, 123",
  "ativo": true,
  "observacoes": "Observações aqui"
}
```

### Get by ID
```http
GET /api/dizimistas/{id}
Authorization: Bearer {token}
```

### Update
```http
PATCH /api/dizimistas/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "telefone": "(11) 99999-9999",
  "ativo": false
}
```

### Soft Delete
```http
DELETE /api/dizimistas/{id}
Authorization: Bearer {token}
```

## Contribuições (Contributions)

### List with Pagination and Filters
```http
GET /api/contribuicoes?page=1&page_size=20&dizimista_id=1&comunidade_id=1&tipo=DIZIMO&data_inicio=2026-01-01&data_fim=2026-01-31
Authorization: Bearer {token}
```

### Create
```http
POST /api/contribuicoes
Authorization: Bearer {token}
Content-Type: application/json

{
  "dizimista_id": 1,
  "comunidade_id": 1,
  "tipo": "DIZIMO",
  "valor": "150.00",
  "data_contribuicao": "2026-02-14",
  "forma_pagamento": "PIX",
  "referencia_mes": "2026-02",
  "observacoes": "Dízimo de fevereiro"
}
```

### Create Anonymous Contribution
```http
POST /api/contribuicoes
Authorization: Bearer {token}
Content-Type: application/json

{
  "dizimista_id": null,
  "comunidade_id": 1,
  "tipo": "OFERTA",
  "valor": "50.00",
  "data_contribuicao": "2026-02-14"
}
```

### Get by ID
```http
GET /api/contribuicoes/{id}
Authorization: Bearer {token}
```

### Update
```http
PATCH /api/contribuicoes/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "valor": "200.00",
  "observacoes": "Valor atualizado"
}
```

### Delete
```http
DELETE /api/contribuicoes/{id}
Authorization: Bearer {token}
```

## Reports

### Aniversariantes (Birthdays)
```http
GET /api/reports/aniversariantes?periodo=hoje&comunidade_id=1
Authorization: Bearer {token}

periodo: "hoje" | "7dias" | "mes"

Response:
[
  {
    "id": 1,
    "nome": "João da Silva",
    "data_nascimento": "1975-02-14",
    "telefone": "(11) 98765-4321",
    "email": "joao@example.com",
    "comunidade_id": 1,
    "comunidade_nome": "Comunidade São Pedro"
  }
]
```

### Total by Period
```http
GET /api/reports/total-periodo?start_date=2026-01-01&end_date=2026-01-31&comunidade_id=1
Authorization: Bearer {token}

Response:
{
  "total": "1500.00",
  "quantidade": 10,
  "data_inicio": "2026-01-01",
  "data_fim": "2026-01-31",
  "comunidade_id": 1
}
```

### Total by Type
```http
GET /api/reports/total-tipo?start_date=2026-01-01&end_date=2026-01-31&comunidade_id=1
Authorization: Bearer {token}

Response:
{
  "data_inicio": "2026-01-01",
  "data_fim": "2026-01-31",
  "comunidade_id": 1,
  "totais": [
    {
      "tipo": "DIZIMO",
      "total": "1200.00",
      "quantidade": 8
    },
    {
      "tipo": "OFERTA",
      "total": "300.00",
      "quantidade": 2
    }
  ]
}
```

### Dizimista History
```http
GET /api/reports/dizimista/{id}/historico
Authorization: Bearer {token}

Response:
{
  "dizimista_id": 1,
  "dizimista_nome": "João da Silva",
  "total_geral": "600.00",
  "quantidade_total": 4,
  "contribuicoes": [...]
}
```

## Enums

### RoleEnum (User Roles)
- `ADMIN` - Full access
- `OPERADOR` - Limited access

### TipoContribuicaoEnum (Contribution Types)
- `DIZIMO` - Tithe
- `OFERTA` - Offering

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email já cadastrado no sistema"
}
```

### 401 Unauthorized
```json
{
  "detail": "Email ou senha incorretos"
}
```

### 403 Forbidden
```json
{
  "detail": "Permissões insuficientes para esta operação"
}
```

### 404 Not Found
```json
{
  "detail": "Dizimista não encontrado"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "valor"],
      "msg": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]
}
```

## Testing with curl

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@ecclesia.com", "senha": "Admin123!"}'
```

### List Dizimistas
```bash
TOKEN="your-jwt-token-here"
curl -X GET "http://localhost:8000/api/dizimistas?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Create Contribution
```bash
TOKEN="your-jwt-token-here"
curl -X POST http://localhost:8000/api/contribuicoes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "dizimista_id": 1,
    "comunidade_id": 1,
    "tipo": "DIZIMO",
    "valor": "150.00",
    "data_contribuicao": "2026-02-14"
  }'
```

## Interactive Documentation

Visit these URLs for interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Health Check

```http
GET /health

Response:
{
  "status": "ok",
  "app": "Ecclesia - Sistema de Dízimo",
  "version": "0.1.0"
}
```
