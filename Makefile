.PHONY: up down logs backend-shell db-shell backend-test frontend-test migrate seed lint clean help

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Ecclesia Core - Development Commands"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services
	docker-compose up -d
	@echo "Services started. Backend: http://localhost:8000 | Frontend: http://localhost:5173"

down: ## Stop all services
	docker-compose down

logs: ## Follow logs for all services
	docker-compose logs -f

logs-backend: ## Follow logs for backend service
	docker-compose logs -f backend

logs-frontend: ## Follow logs for frontend service
	docker-compose logs -f frontend

logs-postgres: ## Follow logs for postgres service
	docker-compose logs -f postgres

backend-shell: ## Open a shell in the backend container
	docker-compose exec backend /bin/bash

db-shell: ## Open psql shell in the database
	docker-compose exec postgres psql -U ecclesia_user -d ecclesia_db

backend-test: ## Run pytest in backend container
	docker-compose exec backend pytest

backend-test-cov: ## Run pytest with coverage in backend container
	docker-compose exec backend pytest --cov=app --cov-report=html --cov-report=term

frontend-test: ## Run frontend tests
	docker-compose exec frontend npm run test

migrate: ## Run alembic migrations
	docker-compose exec backend alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MSG="your message")
	docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

migrate-downgrade: ## Downgrade migration by one version
	docker-compose exec backend alembic downgrade -1

seed: ## Run seed data script
	docker-compose exec backend python -m app.scripts.seed

lint: ## Run ruff linter on backend
	docker-compose exec backend ruff check .

lint-fix: ## Run ruff linter with auto-fix on backend
	docker-compose exec backend ruff check --fix .

format: ## Format backend code with ruff
	docker-compose exec backend ruff format .

clean: ## Stop and remove all containers, networks, and volumes
	docker-compose down -v
	@echo "Cleaned up containers, networks, and volumes"

clean-all: clean ## Clean everything including images
	docker-compose down -v --rmi all
	@echo "Cleaned up everything including images"

restart: down up ## Restart all services

rebuild: ## Rebuild and restart all services
	docker-compose down
	docker-compose up -d --build

build: ## Build all services without starting
	docker-compose build

ps: ## Show status of all services
	docker-compose ps

init: ## Initialize project (copy .env.example to .env if not exists)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created from .env.example"; \
		echo "Please update .env with your configuration"; \
	else \
		echo ".env file already exists"; \
	fi

setup: init build up migrate ## Complete setup: init, build, start, and migrate
	@echo "Setup complete! Access the application:"
	@echo "  Backend API: http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"
	@echo "  Frontend: http://localhost:5173"
