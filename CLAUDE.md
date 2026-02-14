# CLAUDE.md - Ecclesia Core Developer Guide

## Visão Geral

Ecclesia Core é um sistema MVP para gerenciamento de dízimo e ofertas de paróquias católicas. O sistema suporta estrutura paroquial (Paróquia → Comunidades) e fluxos principais: cadastro de dizimistas, registro de contribuições, consultas e relatórios.

## Arquitetura

### Stack Tecnológico

**Backend:**
- FastAPI 0.1+ (framework web assíncrono)
- SQLAlchemy 2.x (ORM)
- Alembic (migrations)
- PostgreSQL 15+ (banco de dados)
- JWT (autenticação via python-jose)
- Passlib + bcrypt (hash de senhas)
- Pytest (testes)
- Ruff (linting/formatting)

**Frontend:**
- React 18+
- TypeScript
- Vite (build tool)
- React Router (navegação)
- React Hook Form + Zod (formulários e validação)
- TailwindCSS (estilização)
- TanStack Query (gerenciamento de estado server)

**Infraestrutura:**
- Docker Compose (desenvolvimento local)
- GitHub Actions (CI/CD)
- PostgreSQL em container
- Hot reload para backend e frontend

### Estrutura de Pastas

```
ecclesia-core/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Entry point da aplicação
│   │   ├── config.py       # Configurações (env vars)
│   │   ├── database.py     # Setup SQLAlchemy
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic (validação)
│   │   ├── routers/        # Endpoints REST
│   │   ├── services/       # Lógica de negócio
│   │   └── auth/           # Autenticação JWT
│   ├── alembic/            # Migrations
│   ├── tests/              # Testes pytest
│   └── requirements.txt
├── frontend/               # UI React
│   ├── src/
│   │   ├── components/    # Componentes reutilizáveis
│   │   ├── pages/         # Páginas/rotas
│   │   ├── services/      # Cliente API
│   │   ├── hooks/         # Custom hooks
│   │   └── types/         # TypeScript types
│   └── package.json
├── infra/                 # Guias de deploy
├── .github/workflows/     # CI/CD
├── docker-compose.yml     # Ambiente local
├── Makefile              # Comandos comuns
└── .env.example          # Template de variáveis

```

### Decisões Arquiteturais

**DA-001: FastAPI + React SPA**
- Rationale: Separação clara backend/frontend, deploy independente, API first
- Alternativa considerada: Monolito com templates
- Trade-off: Mais complexidade inicial, maior flexibilidade futura

**DA-002: PostgreSQL**
- Rationale: ACID, relacional, open source, produção-ready
- Alternativa considerada: SQLite (descartado para produção)
- Trade-off: Requer container, mais robusto

**DA-003: JWT para autenticação**
- Rationale: Stateless, escalável, padrão de mercado
- Alternativa considerada: Sessions (descartado por escalabilidade)
- Trade-off: Impossível revogar tokens sem lista negra

**DA-004: Alembic para migrations**
- Rationale: Integração nativa com SQLAlchemy, autogenerate
- Trade-off: Migrações complexas precisam revisão manual

**DA-005: TypeScript no frontend**
- Rationale: Type safety, melhor DX, menos bugs em runtime
- Alternativa considerada: JavaScript puro
- Trade-off: Setup mais complexo, curva de aprendizado

## Comandos Essenciais

### Setup Inicial

```bash
# Copiar template de variáveis de ambiente
cp .env.example .env

# Editar .env com suas configurações (especialmente SECRET_KEY)
# Gerar SECRET_KEY: openssl rand -hex 32

# Inicializar projeto (instala deps, cria .env, sobe containers)
make init
```

### Desenvolvimento Diário

```bash
# Subir todos os serviços (Postgres + Backend + Frontend)
make up

# Ver logs de todos os serviços
make logs

# Ver logs apenas do backend
make logs-backend

# Parar todos os serviços
make down

# Recriar containers (após mudanças no Dockerfile)
make rebuild
```

### Backend

```bash
# Acessar shell do container backend
make backend-shell

# Rodar testes
make backend-test

# Rodar testes com coverage
make backend-test-cov

# Linting (verificar código)
make lint

# Auto-fix linting
make lint-fix

# Criar nova migration
make migrate-create NAME=nome_descritivo

# Aplicar migrations
make migrate

# Reverter última migration
make migrate-downgrade

# Popular banco com dados seed
make seed
```

### Frontend

```bash
# Rodar testes frontend
make frontend-test

# Build de produção
cd frontend && npm run build
```

### Banco de Dados

```bash
# Acessar psql
make db-shell

# Dentro do psql:
\dt              # Listar tabelas
\d nome_tabela   # Descrever tabela
SELECT * FROM usuarios;
```

### Limpeza

```bash
# Parar e remover containers
make clean

# Remover tudo (incluindo volumes/dados)
make clean-all
```

## Padrões de Código

### Backend (Python)

**Estilo:**
- Use `ruff` para linting (config em `backend/pyproject.toml`)
- Line length: 100 caracteres
- Imports ordenados (isort integrado no ruff)
- Type hints onde possível
- Docstrings em português para funções públicas

**Estrutura de endpoint:**
```python
# backend/app/routers/exemplo.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.exemplo import ExemploCreate, ExemploResponse
from app.services.exemplo import exemplo_service

router = APIRouter(prefix="/api/exemplos", tags=["exemplos"])

@router.post("/", response_model=ExemploResponse, status_code=201)
async def criar_exemplo(
    data: ExemploCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo exemplo.
    """
    return await exemplo_service.criar(db, data)
```

**Models (SQLAlchemy):**
```python
# backend/app/models/exemplo.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Exemplo(Base):
    __tablename__ = "exemplos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
```

**Schemas (Pydantic):**
```python
# backend/app/schemas/exemplo.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ExemploBase(BaseModel):
    nome: str

class ExemploCreate(ExemploBase):
    pass

class ExemploResponse(ExemploBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ativo: bool
    criado_em: datetime
```

### Frontend (TypeScript/React)

**Estilo:**
- Componentes funcionais com hooks
- Props tipadas com TypeScript
- Naming: PascalCase para componentes, camelCase para funções
- Um componente por arquivo

**Estrutura de componente:**
```typescript
// frontend/src/components/ExemploForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const exemploSchema = z.object({
  nome: z.string().min(3, 'Nome deve ter no mínimo 3 caracteres'),
});

type ExemploFormData = z.infer<typeof exemploSchema>;

interface ExemploFormProps {
  onSubmit: (data: ExemploFormData) => void;
  isLoading?: boolean;
}

export function ExemploForm({ onSubmit, isLoading }: ExemploFormProps) {
  const { register, handleSubmit, formState: { errors } } = useForm<ExemploFormData>({
    resolver: zodResolver(exemploSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('nome')} />
      {errors.nome && <span>{errors.nome.message}</span>}
      <button type="submit" disabled={isLoading}>Salvar</button>
    </form>
  );
}
```

## Como Adicionar uma Feature

### 1. Definir o Domínio (Backend)

**a) Criar o modelo:**
```bash
# Editar backend/app/models/nova_entidade.py
# Importar em backend/app/models/__init__.py
```

**b) Criar os schemas:**
```bash
# Editar backend/app/schemas/nova_entidade.py
```

**c) Criar migration:**
```bash
make migrate-create NAME=add_nova_entidade
make migrate
```

**d) Criar service (lógica de negócio):**
```bash
# Editar backend/app/services/nova_entidade.py
```

**e) Criar router (endpoints):**
```bash
# Editar backend/app/routers/nova_entidade.py
# Registrar em backend/app/main.py
```

**f) Escrever testes:**
```bash
# Editar backend/tests/test_nova_entidade.py
make backend-test
```

### 2. Implementar UI (Frontend)

**a) Definir types:**
```bash
# frontend/src/types/nova-entidade.ts
```

**b) Criar serviço API:**
```bash
# frontend/src/services/nova-entidade.ts
```

**c) Criar componentes:**
```bash
# frontend/src/components/NovaEntidade/
#   - NovaEntidadeForm.tsx
#   - NovaEntidadeList.tsx
#   - NovaEntidadeDetail.tsx
```

**d) Criar páginas/rotas:**
```bash
# frontend/src/pages/NovaEntidade.tsx
# Adicionar rota em frontend/src/App.tsx
```

### 3. Validação End-to-End

```bash
# Backend
make backend-test
make lint

# Frontend
make frontend-test
cd frontend && npm run build

# Manual
make up
# Testar no navegador: http://localhost:5173
```

## Definition of Done (DoD)

Uma feature está PRONTA quando:

### Backend
- [ ] Modelo SQLAlchemy criado e migração aplicada
- [ ] Schemas Pydantic para request/response
- [ ] Endpoints REST implementados (CRUD se aplicável)
- [ ] Validação de entrada (Pydantic + lógica de negócio)
- [ ] Tratamento de erros (HTTPException com status code correto)
- [ ] Testes automatizados (pytest) com >80% coverage
- [ ] Linting passa (make lint)
- [ ] Documentação automática (/docs) atualizada
- [ ] Logs estruturados em operações críticas

### Frontend
- [ ] Types TypeScript definidos
- [ ] Serviço API client criado
- [ ] Componentes implementados e reutilizáveis
- [ ] Formulários com validação (react-hook-form + zod)
- [ ] Feedback visual (loading, success, error states)
- [ ] Responsivo (mobile + desktop)
- [ ] Build sem erros (npm run build)
- [ ] Testes básicos (smoke tests mínimo)

### Geral
- [ ] Integração backend/frontend funciona
- [ ] Dados persistem corretamente no banco
- [ ] Não há secrets hardcoded
- [ ] README/docs atualizados se necessário
- [ ] CI passa (lint + tests)
- [ ] Code review aprovado (se trabalho em time)

## Segurança

### Checklist de Segurança

- [ ] **Autenticação**: Todos os endpoints protegidos exceto login/health
- [ ] **Autorização**: Verificar role do usuário (Admin vs Operador)
- [ ] **Validação**: Server-side validation em todos os inputs
- [ ] **SQL Injection**: Usar ORM (SQLAlchemy), nunca raw SQL com concatenação
- [ ] **XSS**: Sanitização de inputs, React escapa por padrão
- [ ] **CSRF**: Stateless JWT, sem cookies
- [ ] **Senhas**: Nunca logar senhas, sempre hash (bcrypt)
- [ ] **Secrets**: Variáveis de ambiente, nunca commit
- [ ] **HTTPS**: Obrigatório em produção (configurar no reverse proxy)
- [ ] **CORS**: Restrito a domínios conhecidos em produção
- [ ] **Rate Limiting**: Considerar para produção (slowapi)
- [ ] **Audit**: Campos created_by, updated_by, timestamps

### LGPD Considerations

- **Minimização**: Coletar apenas dados necessários
- **Consentimento**: Dizimista aceita cadastro (futuro: checkbox termos)
- **Acesso**: Usuários podem ver seus próprios dados
- **Portabilidade**: Endpoint para export de dados (futuro)
- **Exclusão**: Soft delete (ativo=false) ou hard delete se solicitado
- **Proteção**: Acesso restrito por autenticação, logs de acesso

## Debugging

### Backend

```bash
# Ver logs em tempo real
make logs-backend

# Acessar shell do container
make backend-shell

# Dentro do container, testar imports
python -c "from app.database import Base; print(Base.metadata.tables.keys())"

# Debugger: adicionar no código
import pdb; pdb.set_trace()
```

### Frontend

```bash
# Ver logs
make logs-frontend

# Erros de build
cd frontend && npm run build

# Console do navegador: F12
# React DevTools: extensão do Chrome
```

### Database

```bash
# Verificar tabelas
make db-shell
\dt

# Ver dados
SELECT * FROM usuarios;

# Resetar banco (CUIDADO: perde dados)
make clean-all
make up
make migrate
make seed
```

## Troubleshooting

**Problema: Containers não sobem**
```bash
# Verificar logs
docker-compose logs

# Recriar do zero
make clean-all
make up
```

**Problema: Migration falha**
```bash
# Ver migrations pendentes
cd backend && alembic current
cd backend && alembic history

# Reverter e tentar novamente
make migrate-downgrade
# Corrigir migration
make migrate
```

**Problema: Backend não conecta no banco**
```bash
# Verificar .env
cat .env | grep DATABASE_URL

# Deve ser: postgresql://ecclesia:senha@postgres:5432/ecclesia_db
# (usar 'postgres' como host dentro do Docker)
```

**Problema: Frontend não chama API**
```bash
# Verificar VITE_API_URL em .env
# Deve ser: http://localhost:8000

# Verificar CORS no backend (app/main.py)
```

## Próximos Passos / Backlog

Funcionalidades futuras consideradas:
- [ ] Emissão de recibos (PDF)
- [ ] Gráficos e dashboards avançados
- [ ] Integração com gateways de pagamento
- [ ] Notificações por email/SMS
- [ ] Multi-tenant (várias paróquias em uma instância)
- [ ] App mobile (React Native)
- [ ] Exportação de relatórios (Excel, CSV)
- [ ] Backup automático
- [ ] Audit log completo
- [ ] Permissões granulares

## Referências

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [React Docs](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [TailwindCSS](https://tailwindcss.com/docs)

---

**Última atualização**: Milestone 0 - Bootstrap (2026-02-14)
