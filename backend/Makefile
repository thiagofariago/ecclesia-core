.PHONY: help install dev test lint format clean migration upgrade downgrade

help:
	@echo "Comandos disponíveis:"
	@echo "  make install    - Instalar dependências"
	@echo "  make dev        - Executar servidor de desenvolvimento"
	@echo "  make test       - Executar testes"
	@echo "  make lint       - Verificar código com ruff"
	@echo "  make format     - Formatar código com ruff"
	@echo "  make migration  - Criar nova migration"
	@echo "  make upgrade    - Aplicar migrations"
	@echo "  make downgrade  - Reverter última migration"
	@echo "  make clean      - Limpar arquivos temporários"

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .

migration:
	@read -p "Nome da migration: " name; \
	alembic revision --autogenerate -m "$$name"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
