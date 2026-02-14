# Ecclesia Backend - Sistema de Dízimo

Backend API desenvolvido com FastAPI para gerenciamento de dízimo e membros da igreja.

## Requisitos

- Python 3.11+
- PostgreSQL 14+

## Instalação

1. Criar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
cp .env.example .env
# Editar .env com suas configurações
```

4. Executar migrations:
```bash
alembic upgrade head
```

## Execução

### Desenvolvimento
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Produção
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Testes

```bash
pytest
```

## Documentação da API

Após executar a aplicação, acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Segurança

### Rate Limiting

O sistema implementa rate limiting para proteger contra ataques de força bruta e abuso da API:

- **Login**: 5 tentativas por minuto por IP
- **Registro de usuário**: 10 requisições por minuto por IP
- **Listagem de dizimistas**: 100 requisições por minuto por IP
- **Listagem de contribuições**: 100 requisições por minuto por IP

Quando o limite é excedido, a API retorna status HTTP 429 (Too Many Requests).

### CORS

As origens permitidas para CORS são configuradas através da variável de ambiente `ALLOWED_ORIGINS`:

```bash
# Desenvolvimento
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Produção
ALLOWED_ORIGINS=https://seudominio.com,https://www.seudominio.com
```

### SECRET_KEY

A `SECRET_KEY` é usada para assinar tokens JWT e deve ser:
- No mínimo 32 caracteres
- Gerada aleatoriamente
- Nunca compartilhada ou versionada

Para gerar uma chave segura:
```bash
openssl rand -hex 32
```

## Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point da aplicação
│   ├── config.py            # Configurações
│   ├── database.py          # Setup do SQLAlchemy
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Schemas Pydantic
│   ├── routers/             # Endpoints da API
│   ├── services/            # Lógica de negócio
│   └── auth/                # Autenticação JWT
├── alembic/                 # Migrations
├── tests/                   # Testes
├── requirements.txt         # Dependências
└── pyproject.toml          # Configuração do Ruff
```

## Linting

```bash
ruff check .
ruff format .
```
