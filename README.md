# Ecclesia Core

A comprehensive Catholic church tithing and donation management system built with FastAPI, React, and PostgreSQL.

## Overview

Ecclesia Core provides churches with a secure, user-friendly platform to manage member donations, track tithing, generate financial reports, and maintain transparency with parishioners.

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- PostgreSQL 16
- SQLAlchemy ORM
- Alembic for migrations
- JWT authentication

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- React Router
- TanStack Query

### Infrastructure
- Docker & Docker Compose
- GitHub Actions for CI/CD
- Cloud-agnostic deployment approach

## Project Structure

```
ecclesia-core/
├── backend/              # FastAPI backend application
│   ├── app/             # Application code
│   ├── tests/           # Backend tests
│   ├── alembic/         # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/            # React frontend application
│   ├── src/             # Source code
│   ├── public/          # Static assets
│   ├── Dockerfile
│   └── package.json
├── infra/               # Infrastructure documentation
├── .github/
│   └── workflows/       # CI/CD workflows
├── docker-compose.yml   # Development environment
├── Makefile            # Development commands
└── .env.example        # Environment variables template
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Make (optional, but recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ecclesia-core
```

2. Initialize the environment:
```bash
make init
```
This creates a `.env` file from `.env.example`. Update it with your configuration.

3. Build and start all services:
```bash
make setup
```

4. Access the application:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:5173

## Development Commands

The Makefile provides convenient commands for development:

```bash
make up              # Start all services
make down            # Stop all services
make logs            # Follow logs for all services
make backend-shell   # Open shell in backend container
make db-shell        # Open PostgreSQL shell
make backend-test    # Run backend tests
make frontend-test   # Run frontend tests
make migrate         # Run database migrations
make lint            # Run code linter
make clean           # Clean up containers and volumes
make help            # Show all available commands
```

## Development Workflow

### Backend Development
- Hot reload is enabled by default
- Code is mounted as a volume for instant updates
- Access API docs at http://localhost:8000/docs

### Frontend Development
- Vite dev server with hot module replacement
- Code changes reflect immediately
- Access at http://localhost:5173

### Database Migrations
```bash
# Create a new migration
make migrate-create MSG="your migration message"

# Apply migrations
make migrate

# Rollback one migration
make migrate-downgrade
```

## Testing

### Backend Tests
```bash
# Run all tests
make backend-test

# Run with coverage
make backend-test-cov
```

### Frontend Tests
```bash
make frontend-test
```

## Code Quality

### Linting
```bash
# Check for issues
make lint

# Auto-fix issues
make lint-fix

# Format code
make format
```

## CI/CD

GitHub Actions workflow runs on push and pull requests:
- Backend: linting, testing, coverage
- Frontend: linting, testing, build
- Docker: build verification

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `DATABASE_URL`: Full database connection string
- `SECRET_KEY`: JWT signing key (change in production!)
- `ENVIRONMENT`: development/staging/production

## Deployment

Ready to deploy to production? Check out our comprehensive deployment guide:

**[📘 Deployment Guide](infra/DEPLOY.md)**

The guide covers:
- **4 deployment options**: Railway, Render, DigitalOcean, and Self-Hosted VPS
- **Cost estimates**: $5-20/month for small to medium churches
- **Step-by-step instructions** for each platform
- **Security checklist** and best practices
- **Backup strategies** and monitoring setup
- **Troubleshooting** common issues

### Quick Deployment Options

| Platform | Cost | Difficulty | Best For |
|----------|------|------------|----------|
| **[Railway.app](https://railway.app)** | $5-10/mo | Easy | Quick MVP deployment |
| **[Render.com](https://render.com)** | $7-15/mo | Easy | Stable production deployment |
| **[DigitalOcean](https://digitalocean.com)** | $12-20/mo | Medium | Growing churches, scalability |
| **Self-Hosted VPS** | $5-10/mo | Advanced | Full control, lowest cost |

For detailed instructions, see [infra/DEPLOY.md](infra/DEPLOY.md).

## Security Notes

- Change default passwords in `.env` before deployment
- Use strong `SECRET_KEY` in production (generate with `openssl rand -hex 32`)
- Never commit `.env` file to version control
- Review security settings in Milestone 3
- **Before production**: Complete the [Security Checklist](infra/DEPLOY.md#security-checklist)

## Milestones

- **Milestone 0**: Infrastructure setup (CURRENT)
- **Milestone 1**: Backend MVP with authentication and core models
- **Milestone 2**: Frontend MVP with all user flows
- **Milestone 3**: Security hardening and production documentation

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

[To be determined]

## Support

For issues and questions, please use the GitHub issue tracker.
