# Getting Started with Ecclesia Core

**Welcome!** This guide will help you get Ecclesia Core up and running on your local machine in just a few minutes.

---

## Prerequisites

Before you begin, make sure you have:
- **Docker** and **Docker Compose** installed ([Install Docker](https://docs.docker.com/get-docker/))
- **Make** (optional but recommended - usually pre-installed on macOS/Linux)
- **Git** (to clone the repository)

---

## Quick Start (5 Minutes)

### 1. Verify Prerequisites

```bash
# Check Docker
docker --version
# Should output: Docker version 20.x or higher

# Check Docker Compose
docker-compose --version
# Should output: docker-compose version 1.29.x or higher

# Check Make (optional)
make --version
```

### 2. Initialize Environment

```bash
# Create environment file from template
make init

# This will:
# - Create .env from .env.example
# - Set up necessary environment variables
```

### 3. Generate SECRET_KEY

**⚠️ CRITICAL STEP - Do not skip!**

```bash
# Generate a strong secret key
openssl rand -hex 32
```

Copy the output and update your `.env` file:

```bash
# Open .env file
nano .env

# Find the SECRET_KEY line and replace with your generated key:
SECRET_KEY=your_generated_key_paste_here

# Save and exit (Ctrl+X, then Y, then Enter)
```

### 4. Start All Services

```bash
# Build and start containers
make up

# This will:
# - Start PostgreSQL database
# - Start FastAPI backend (http://localhost:8000)
# - Start React frontend (http://localhost:5173)
```

**First startup might take 2-3 minutes** while Docker downloads images and builds containers. Watch the logs to track progress.

### 5. Initialize Database

In a new terminal window:

```bash
# Run database migrations
make migrate

# Seed initial data (optional but recommended for testing)
make seed
```

### 6. Access the Application

Open your browser and visit:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc

### 7. Login

Use these test credentials:

**Admin User:**
- Email: `admin@ecclesia.com`
- Password: `Admin123!`

**Operador User:**
- Email: `operador@ecclesia.com`
- Password: `Opera123!`

---

## What You Get

After following the steps above, you'll have:

✅ A complete church tithing management system
✅ Sample parish and communities
✅ 5 sample dizimistas (tithing members)
✅ 10 sample contributions
✅ 2 user accounts (admin and operator)

---

## Common Commands

```bash
# View logs (all services)
make logs

# View only backend logs
make logs-backend

# View only frontend logs
make logs-frontend

# Stop all services
make down

# Restart services
make restart

# Run backend tests
make backend-test

# Access backend shell (for debugging)
make backend-shell

# Access database shell
make db-shell

# See all available commands
make help
```

---

## Project Structure

```
ecclesia-core/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   ├── tests/        # Backend tests
│   └── alembic/      # Database migrations
├── frontend/         # React frontend
│   └── src/          # Source code
├── infra/           # Deployment guides
├── docker-compose.yml
├── Makefile         # Common commands
└── .env             # Your environment variables (YOU CREATED THIS)
```

---

## Next Steps

Now that you have Ecclesia Core running, you can:

### 1. Explore the Application
- Navigate through the different sections
- Create a new dizimista (tithing member)
- Register a contribution
- View birthday reports
- Generate financial reports

### 2. Read the Documentation
- **CLAUDE.md** - Developer guide, architecture, coding standards
- **PROJECT_STATUS.md** - Complete project status and features
- **SECURITY_REVIEW.md** - Security assessment and recommendations
- **BACKLOG.md** - Planned future features
- **infra/DEPLOY.md** - Deployment guide for production

### 3. Customize for Your Church
- Update parish and community names
- Add your church's logo (future feature)
- Configure email settings (future feature)
- Customize receipt templates (future feature)

### 4. Development (If you want to modify code)
- Backend: Edit files in `backend/app/`
- Frontend: Edit files in `frontend/src/`
- Changes reload automatically (hot reload enabled)

### 5. Deploy to Production
When ready to deploy:
1. Read `infra/DEPLOY.md` for deployment options
2. Review `SECURITY_REVIEW.md` for security checklist
3. Choose a hosting platform (Railway, Render, DigitalOcean, or VPS)
4. Follow the step-by-step deployment guide

---

## Troubleshooting

### Issue: Containers won't start

```bash
# Check if ports are already in use
lsof -i :5173  # Frontend port
lsof -i :8000  # Backend port
lsof -i :5432  # Database port

# If ports are in use, stop the conflicting services or change ports in docker-compose.yml
```

### Issue: Database connection error

```bash
# Make sure PostgreSQL container is running
docker-compose ps

# Check database logs
make logs-db

# Restart database
make restart
```

### Issue: SECRET_KEY error on startup

```bash
# Make sure you generated and set a SECRET_KEY in .env
cat .env | grep SECRET_KEY

# If it's still the default value, generate a new one:
openssl rand -hex 32

# Update .env with the generated key
```

### Issue: Frontend can't connect to backend

```bash
# Check if backend is running
curl http://localhost:8000/health

# Should return: {"status":"ok"}

# Check CORS settings in .env
cat .env | grep ALLOWED_ORIGINS

# Should include: http://localhost:5173
```

### Issue: Migrations fail

```bash
# Drop database and start fresh (WARNING: loses all data)
make clean-all
make up
make migrate
make seed
```

---

## Getting Help

If you run into issues:

1. Check the logs: `make logs`
2. Read `CLAUDE.md` for detailed documentation
3. Review `PROJECT_STATUS.md` for system overview
4. Check `SECURITY_REVIEW.md` for security guidelines

For common issues, see the Troubleshooting section in `CLAUDE.md`.

---

## System Requirements

**Minimum:**
- 2 GB RAM
- 10 GB disk space
- Docker 20.10+
- Docker Compose 1.29+

**Recommended:**
- 4 GB RAM
- 20 GB disk space
- Modern browser (Chrome, Firefox, Safari, Edge)

---

## Security Note

**⚠️ For Development Only**

The default configuration is for **local development** only. Before deploying to production:

1. Generate a strong SECRET_KEY (32+ characters)
2. Change all default passwords
3. Configure ALLOWED_ORIGINS to your production domain
4. Enable HTTPS/SSL
5. Review `SECURITY_REVIEW.md` for complete checklist
6. Read `infra/DEPLOY.md` for deployment best practices

---

## What's Included in the MVP

✅ **Authentication** - Secure login with JWT
✅ **User Roles** - Admin and Operador (Operator) roles
✅ **Parish Management** - Manage parishes and communities
✅ **Dizimista CRUD** - Full member management
✅ **Contribution Tracking** - Record dízimo (tithing) and ofertas (offerings)
✅ **Search & Filters** - Find members quickly
✅ **Birthday Reports** - Track member birthdays
✅ **Financial Reports** - View totals by period and type
✅ **Anonymous Contributions** - Support contributions without a registered member
✅ **Responsive UI** - Works on mobile and desktop
✅ **Brazilian Portuguese** - Complete localization

---

## What's Coming Next (See BACKLOG.md)

🔜 PDF receipt generation
🔜 Email notifications
🔜 Excel/CSV export
🔜 Dashboard charts
🔜 LGPD compliance features (consent, data export, deletion)
🔜 Payment gateway integration
🔜 And much more!

---

## Support

This is an open-source MVP project. For questions or contributions, refer to the documentation files in this repository.

---

## License

[To be determined]

---

**🎉 You're all set! Start exploring Ecclesia Core.**

Visit http://localhost:5173 and login with the test credentials to begin.
