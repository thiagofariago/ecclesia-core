# Ecclesia Core - Deployment Guide

Complete guide for deploying Ecclesia Core to production. This guide covers multiple hosting options suitable for churches of all sizes, from small communities to larger parishes.

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Architecture](#architecture)
- [Cost Estimates](#cost-estimates)
- [Deployment Options](#deployment-options)
  - [Option 1: Railway.app (Recommended for MVP)](#option-1-railwayapp-recommended-for-mvp)
  - [Option 2: Render.com](#option-2-rendercom)
  - [Option 3: DigitalOcean App Platform](#option-3-digitalocean-app-platform)
  - [Option 4: Self-Hosted (VPS)](#option-4-self-hosted-vps)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Security Checklist](#security-checklist)
- [Backup Strategy](#backup-strategy)
- [Monitoring & Observability](#monitoring--observability)
- [Cost Optimization](#cost-optimization)
- [Troubleshooting](#troubleshooting)
- [Production Readiness Checklist](#production-readiness-checklist)

---

## Overview

Ecclesia Core is a full-stack application consisting of:
- **Backend**: FastAPI application (Python 3.11+)
- **Frontend**: React application with Vite (Node 20+)
- **Database**: PostgreSQL 16+

This guide provides step-by-step instructions for deploying to various cloud platforms, with focus on low-cost, easy-to-manage options suitable for small to medium churches.

---

## System Requirements

### Minimum Requirements
- **Backend**: 512MB RAM, 1 vCPU
- **Frontend**: Static hosting (CDN)
- **Database**: PostgreSQL 16+, 1GB storage minimum
- **Python**: 3.11 or higher
- **Node.js**: 20 or higher

### Recommended for Production
- **Backend**: 1GB RAM, 1-2 vCPU
- **Database**: 2GB storage, automated backups
- **SSL/TLS**: HTTPS certificate (Let's Encrypt recommended)

### Expected Load (50-200 active users)
- Concurrent users: 10-20
- Requests per minute: 50-100
- Database connections: 10-20
- Storage growth: ~100MB/month

---

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────┐
│    Frontend     │  React + Vite (Static)
│  (Port 5173)    │
└────────┬────────┘
         │ API Calls
         ▼
┌─────────────────┐
│     Backend     │  FastAPI
│  (Port 8000)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │  Database
│  (Port 5432)    │
└─────────────────┘
```

---

## Cost Estimates

### Small Church (50-100 users)
| Platform | Monthly Cost | Notes |
|----------|--------------|-------|
| Railway.app | $5-10 | Best for MVP, includes everything |
| Render.com | $7-15 | Free tier available for testing |
| DigitalOcean | $12-20 | More scalable, better for growth |
| Self-Hosted VPS | $5-10 | Cheapest, requires DevOps knowledge |

### Medium Church (100-200 users)
| Platform | Monthly Cost | Notes |
|----------|--------------|-------|
| Railway.app | $15-25 | May need to upgrade database |
| Render.com | $20-35 | Stable and predictable |
| DigitalOcean | $25-40 | Best for scaling |
| Self-Hosted VPS | $10-20 | Cost-effective with proper setup |

**Additional Costs:**
- Domain name: $10-15/year
- Email service (optional): $0-5/month
- Backup storage (optional): $1-5/month
- Monitoring tools: Free tiers available

---

## Deployment Options

### Option 1: Railway.app (Recommended for MVP)

**Best for**: Quick deployment, minimal DevOps experience required

**Estimated Cost**: $5-10/month for small churches

**Pros:**
- One-click PostgreSQL deployment
- Automatic HTTPS
- GitHub integration
- Simple environment variable management
- Free $5 monthly credit

**Cons:**
- Limited free tier
- Less control over infrastructure
- May need to upgrade as you scale

#### Step-by-Step Guide

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Verify your account

2. **Deploy PostgreSQL**
   ```
   - Click "New Project"
   - Select "Provision PostgreSQL"
   - Wait for deployment to complete
   - Copy the DATABASE_URL from variables tab
   ```

3. **Deploy Backend**
   ```
   - In the same project, click "New Service"
   - Select "GitHub Repo"
   - Choose your ecclesia-core repository
   - Set Root Directory: backend
   - Add environment variables (see Environment Variables section)
   - Railway will auto-detect Dockerfile and deploy
   ```

   **Important Environment Variables for Backend:**
   ```
   DATABASE_URL=${POSTGRESQL.DATABASE_URL}
   SECRET_KEY=<generate-with-openssl-rand-hex-32>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ENVIRONMENT=production
   CORS_ORIGINS=https://your-frontend-url.railway.app
   ```

4. **Run Database Migrations**
   ```
   - Once backend is deployed, go to backend service
   - Click "Settings" → "Deploy Logs"
   - Run a one-time command:
     alembic upgrade head
   - Optional: Seed initial data
     python -m app.seed
   ```

5. **Deploy Frontend**
   ```
   - Click "New Service" → "GitHub Repo"
   - Select ecclesia-core repository
   - Set Root Directory: frontend
   - Add environment variable:
     VITE_API_URL=https://your-backend-url.railway.app
   - Deploy
   ```

6. **Configure Custom Domain (Optional)**
   ```
   - Go to frontend service → "Settings"
   - Click "Generate Domain" or add custom domain
   - Update DNS records as instructed
   - Update CORS_ORIGINS in backend with new domain
   ```

7. **Verify Deployment**
   - Visit frontend URL
   - Check `/health` endpoint on backend
   - Test login functionality
   - Verify database connections

---

### Option 2: Render.com

**Best for**: Stable deployment with good free tier for testing

**Estimated Cost**: $7-15/month

**Pros:**
- Excellent free tier (backend sleeps after 15 min inactivity)
- Easy CI/CD from GitHub
- Automatic HTTPS
- Good documentation
- Infrastructure as Code (render.yaml support)

**Cons:**
- Free tier has spin-up delays
- PostgreSQL requires paid tier ($7/month minimum)
- Limited to certain regions

#### Step-by-Step Guide

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Verify email

2. **Deploy PostgreSQL**
   ```
   - Dashboard → "New" → "PostgreSQL"
   - Name: ecclesia-db
   - Database: ecclesia_db
   - User: ecclesia_user
   - Region: Choose closest to your users
   - Plan: Starter ($7/month) or Free (limited)
   - Click "Create Database"
   - Copy "Internal Database URL" for backend
   ```

3. **Deploy Backend**
   ```
   - Dashboard → "New" → "Web Service"
   - Connect your GitHub repository
   - Name: ecclesia-backend
   - Region: Same as database
   - Branch: main
   - Root Directory: backend
   - Runtime: Docker
   - Plan: Free or Starter ($7/month)
   - Add Environment Variables (see section below)
   - Click "Create Web Service"
   ```

   **Environment Variables:**
   ```
   DATABASE_URL=<paste-internal-database-url>
   SECRET_KEY=<generate-with-openssl-rand-hex-32>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ENVIRONMENT=production
   CORS_ORIGINS=https://your-frontend.onrender.com
   ```

4. **Run Migrations**
   ```
   - After first deployment, go to backend service
   - Shell tab → Run command:
     alembic upgrade head
     python -m app.seed  # Optional
   ```

5. **Deploy Frontend**
   ```
   - Dashboard → "New" → "Static Site"
   - Connect GitHub repository
   - Name: ecclesia-frontend
   - Branch: main
   - Root Directory: frontend
   - Build Command: npm install && npm run build
   - Publish Directory: dist
   - Add Environment Variable:
     VITE_API_URL=https://ecclesia-backend.onrender.com
   - Click "Create Static Site"
   ```

6. **Configure Custom Domain**
   ```
   - Go to frontend service → "Settings"
   - Add custom domain under "Custom Domain"
   - Update DNS CNAME record
   - Update backend CORS_ORIGINS
   ```

7. **Enable Auto-Deploy**
   - By default, Render auto-deploys on push to main
   - Configure in Settings → Build & Deploy

---

### Option 3: DigitalOcean App Platform

**Best for**: Growing churches, better scalability

**Estimated Cost**: $12-20/month

**Pros:**
- Great scalability options
- Managed database with daily backups
- Good performance
- More control than Railway/Render
- Excellent documentation

**Cons:**
- Higher starting cost
- Slightly more complex setup
- Requires credit card even for trial

#### Step-by-Step Guide

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Sign up (get $200 credit for 60 days with promo)
   - Add payment method

2. **Create Managed PostgreSQL Database**
   ```
   - Navigate to "Databases"
   - Click "Create Database Cluster"
   - Choose PostgreSQL 16
   - Plan: Basic ($15/month) or Development ($12/month)
   - Datacenter: Choose closest to users
   - Create Cluster
   - Add database: ecclesia_db
   - Create user: ecclesia_user
   - Copy connection string
   ```

3. **Deploy via App Platform**
   ```
   - Navigate to "Apps"
   - Click "Create App"
   - Choose GitHub as source
   - Select ecclesia-core repository
   - App Platform will detect backend and frontend
   ```

4. **Configure Backend Component**
   ```
   - Component Name: backend
   - Source Directory: /backend
   - Build Command: (auto-detected from Dockerfile)
   - Run Command: uvicorn app.main:app --host 0.0.0.0 --port 8000
   - HTTP Port: 8000
   - Instance Size: Basic ($5/month)
   - Environment Variables:
     DATABASE_URL=<database-connection-string>
     SECRET_KEY=<generate-with-openssl-rand-hex-32>
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ENVIRONMENT=production
     CORS_ORIGINS=${frontend.PUBLIC_URL}
   ```

5. **Configure Frontend Component**
   ```
   - Component Type: Static Site
   - Component Name: frontend
   - Source Directory: /frontend
   - Build Command: npm run build
   - Output Directory: dist
   - Environment Variables:
     VITE_API_URL=${backend.PUBLIC_URL}
   ```

6. **Configure Database Connection**
   ```
   - In backend component settings
   - Click "Add Database"
   - Select your PostgreSQL cluster
   - This adds DATABASE_URL automatically
   ```

7. **Launch App**
   ```
   - Review configuration
   - Click "Create Resources"
   - Wait for deployment (5-10 minutes)
   ```

8. **Run Migrations**
   ```
   - Once deployed, go to backend component
   - Click "Console" tab
   - Run:
     alembic upgrade head
     python -m app.seed  # Optional
   ```

9. **Configure Custom Domain**
   ```
   - Go to Settings → Domains
   - Add your domain
   - Update DNS records as instructed
   - SSL certificate auto-provisioned
   ```

---

### Option 4: Self-Hosted (VPS)

**Best for**: Advanced users, maximum control, lowest cost

**Estimated Cost**: $5-10/month (VPS only)

**Pros:**
- Full control over infrastructure
- Lowest monthly cost
- No vendor lock-in
- Can run other services on same VPS

**Cons:**
- Requires Linux/DevOps knowledge
- Manual security updates
- Need to manage backups yourself
- More time investment

**Recommended VPS Providers:**
- Hetzner: €4.15/month (2GB RAM, 40GB SSD)
- DigitalOcean: $6/month (1GB RAM, 25GB SSD)
- Linode: $5/month (1GB RAM, 25GB SSD)
- Vultr: $5/month (1GB RAM, 25GB SSD)

#### Step-by-Step Guide

1. **Provision VPS**
   ```
   - Choose a VPS provider
   - Create Ubuntu 22.04 LTS instance
   - Minimum: 1GB RAM, 1 vCPU, 25GB SSD
   - Select datacenter close to your users
   - Add SSH key for secure access
   ```

2. **Initial Server Setup**
   ```bash
   # SSH into your server
   ssh root@your-server-ip

   # Update system
   apt update && apt upgrade -y

   # Create a non-root user
   adduser ecclesia
   usermod -aG sudo ecclesia

   # Set up firewall
   ufw allow OpenSSH
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable

   # Switch to new user
   su - ecclesia
   ```

3. **Install Docker & Docker Compose**
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER

   # Install Docker Compose
   sudo apt install docker-compose -y

   # Verify installation
   docker --version
   docker-compose --version
   ```

4. **Clone Repository**
   ```bash
   # Install Git
   sudo apt install git -y

   # Clone your repository
   cd /home/ecclesia
   git clone https://github.com/your-username/ecclesia-core.git
   cd ecclesia-core
   ```

5. **Configure Environment**
   ```bash
   # Copy environment template
   cp .env.example .env

   # Generate secure SECRET_KEY
   openssl rand -hex 32

   # Edit .env file
   nano .env
   ```

   **Important .env settings:**
   ```env
   POSTGRES_USER=ecclesia_user
   POSTGRES_PASSWORD=<strong-password-here>
   POSTGRES_DB=ecclesia_db
   DATABASE_URL=postgresql://ecclesia_user:<password>@postgres:5432/ecclesia_db
   SECRET_KEY=<generated-key-from-openssl>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ENVIRONMENT=production
   CORS_ORIGINS=https://your-domain.com
   ```

6. **Create Production Docker Compose**
   ```bash
   # Create docker-compose.prod.yml
   nano docker-compose.prod.yml
   ```

   Paste the following:
   ```yaml
   version: '3.8'

   services:
     postgres:
       image: postgres:16-alpine
       container_name: ecclesia-postgres
       restart: always
       environment:
         POSTGRES_USER: ${POSTGRES_USER}
         POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
         POSTGRES_DB: ${POSTGRES_DB}
       volumes:
         - postgres-data:/var/lib/postgresql/data
         - ./backups:/backups
       networks:
         - ecclesia-network

     backend:
       build: ./backend
       container_name: ecclesia-backend
       restart: always
       environment:
         DATABASE_URL: ${DATABASE_URL}
         SECRET_KEY: ${SECRET_KEY}
         ALGORITHM: ${ALGORITHM}
         ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}
         ENVIRONMENT: ${ENVIRONMENT}
         CORS_ORIGINS: ${CORS_ORIGINS}
       depends_on:
         - postgres
       networks:
         - ecclesia-network

     frontend:
       build:
         context: ./frontend
         args:
           VITE_API_URL: ${VITE_API_URL}
       container_name: ecclesia-frontend
       restart: always
       networks:
         - ecclesia-network

     nginx:
       image: nginx:alpine
       container_name: ecclesia-nginx
       restart: always
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./infra/nginx.conf:/etc/nginx/conf.d/default.conf
         - ./certbot/conf:/etc/letsencrypt
         - ./certbot/www:/var/www/certbot
       depends_on:
         - backend
         - frontend
       networks:
         - ecclesia-network

   volumes:
     postgres-data:

   networks:
     ecclesia-network:
       driver: bridge
   ```

7. **Set Up Nginx (see nginx.conf.example)**
   ```bash
   # Copy example config
   cp infra/nginx.conf.example infra/nginx.conf

   # Edit with your domain
   nano infra/nginx.conf
   # Replace ecclesia.example.com with your actual domain
   ```

8. **Install SSL Certificate (Let's Encrypt)**
   ```bash
   # Install Certbot
   sudo apt install certbot python3-certbot-nginx -y

   # Get certificate (replace with your domain and email)
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com \
     --non-interactive --agree-tos -m your-email@example.com

   # Test auto-renewal
   sudo certbot renew --dry-run
   ```

9. **Build and Start Services**
   ```bash
   # Build and start all containers
   docker-compose -f docker-compose.prod.yml up -d --build

   # Check logs
   docker-compose -f docker-compose.prod.yml logs -f

   # Verify all containers are running
   docker ps
   ```

10. **Run Database Migrations**
    ```bash
    # Run migrations
    docker exec ecclesia-backend alembic upgrade head

    # Optional: Seed initial data
    docker exec ecclesia-backend python -m app.seed
    ```

11. **Set Up Automated Backups**
    ```bash
    # Copy backup script
    sudo cp infra/backup.sh /usr/local/bin/ecclesia-backup
    sudo chmod +x /usr/local/bin/ecclesia-backup

    # Create cron job for daily backups at 2 AM
    crontab -e
    # Add this line:
    0 2 * * * /usr/local/bin/ecclesia-backup
    ```

12. **Configure Auto-Updates (Optional)**
    ```bash
    # Install unattended-upgrades
    sudo apt install unattended-upgrades -y
    sudo dpkg-reconfigure -plow unattended-upgrades
    ```

13. **Set Up Monitoring**
    ```bash
    # Install monitoring tools
    sudo apt install htop nethogs -y

    # Optional: Set up uptime monitoring (see Monitoring section)
    ```

---

## Environment Variables

Complete list of required environment variables for production deployment.

### Backend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ Yes | - | PostgreSQL connection string |
| `SECRET_KEY` | ✅ Yes | - | JWT signing key (use `openssl rand -hex 32`) |
| `ALGORITHM` | No | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | 30 | Token expiration time |
| `ENVIRONMENT` | No | development | Set to `production` |
| `CORS_ORIGINS` | ✅ Yes | * | Comma-separated allowed origins |
| `APP_NAME` | No | Ecclesia Core | Application name |
| `APP_VERSION` | No | 0.1.0 | Application version |

### Frontend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | ✅ Yes | - | Backend API URL |

### Database Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `POSTGRES_USER` | ✅ Yes | - | Database username |
| `POSTGRES_PASSWORD` | ✅ Yes | - | Database password |
| `POSTGRES_DB` | ✅ Yes | - | Database name |

### How to Generate SECRET_KEY

```bash
# Generate a secure 32-byte random string
openssl rand -hex 32
```

### Example Production .env

```env
# Database
POSTGRES_USER=ecclesia_user
POSTGRES_PASSWORD=VerySecurePassword123!@#
POSTGRES_DB=ecclesia_db
DATABASE_URL=postgresql://ecclesia_user:VerySecurePassword123!@#@postgres:5432/ecclesia_db

# Backend
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
CORS_ORIGINS=https://ecclesia.example.com,https://www.ecclesia.example.com

# App
APP_NAME=Ecclesia Core
APP_VERSION=1.0.0

# Frontend
VITE_API_URL=https://api.ecclesia.example.com
```

---

## Database Migrations

### First Deployment

Run migrations after deploying the backend for the first time:

```bash
# Railway/Render/DigitalOcean App Platform
# Use the platform's console/shell feature

# Run migrations
alembic upgrade head

# Seed initial data (creates default admin user)
python -m app.seed
```

### Self-Hosted (Docker)

```bash
# Run migrations
docker exec ecclesia-backend alembic upgrade head

# Seed data
docker exec ecclesia-backend python -m app.seed
```

### Creating New Migrations (Development)

When you make schema changes:

```bash
# Create migration
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file
# Edit if necessary

# Apply migration
alembic upgrade head

# Commit migration files to git
git add backend/alembic/versions/*
git commit -m "Add migration: Description"
```

### Rolling Back Migrations

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

---

## Security Checklist

Complete this checklist before going to production:

### Critical Security Issues (Must Fix)

- [ ] **Change SECRET_KEY**: Generate new key with `openssl rand -hex 32`
- [ ] **Configure CORS properly**: Set `CORS_ORIGINS` to specific domains (remove `*`)
- [ ] **Change default database password**: Use strong password (20+ characters)
- [ ] **Enable HTTPS**: Configure SSL/TLS certificate
- [ ] **Review authentication settings**: Verify JWT expiration times
- [ ] **Disable DEBUG mode**: Set `ENVIRONMENT=production`

### High Priority

- [ ] **Set up rate limiting**: Protect against brute force attacks
- [ ] **Configure security headers**: HSTS, X-Frame-Options, etc.
- [ ] **Enable database connection pooling**: Optimize performance
- [ ] **Set up firewall rules**: Only allow necessary ports
- [ ] **Regular security updates**: Enable automatic updates
- [ ] **Backup verification**: Test restore procedure

### Medium Priority

- [ ] **Set up monitoring**: Configure uptime monitoring
- [ ] **Error tracking**: Integrate Sentry or similar
- [ ] **Log management**: Set up centralized logging
- [ ] **API documentation security**: Restrict /docs endpoint in production
- [ ] **Input validation**: Review all endpoints
- [ ] **SQL injection protection**: Verify ORM usage

### Recommended

- [ ] **Two-factor authentication**: For admin users
- [ ] **Audit logging**: Track sensitive operations
- [ ] **Intrusion detection**: Configure fail2ban
- [ ] **Regular penetration testing**: Quarterly security audits
- [ ] **Dependency scanning**: Monitor for vulnerabilities
- [ ] **GDPR compliance**: If applicable to your region

### Quick Security Fixes

**1. Generate Secure SECRET_KEY**
```bash
openssl rand -hex 32
```

**2. Fix CORS Configuration**

Edit `/home/th_faria/ecclesia-core/backend/app/main.py`:
```python
# Replace
allow_origins=["*"]

# With
allow_origins=settings.CORS_ORIGINS.split(",")
```

**3. Configure Environment Variables**
```env
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
SECRET_KEY=<generated-key>
ENVIRONMENT=production
```

---

## Backup Strategy

### Automated Database Backups

Most managed platforms (Railway, Render, DigitalOcean) provide automated backups:

**Railway:**
- Automatic daily backups (retained for 7 days)
- Manual backups via CLI

**Render:**
- Daily backups on paid plans
- 7-day retention

**DigitalOcean:**
- Daily backups included
- Point-in-time recovery available

### Self-Hosted Backup Script

Use the provided backup script (see `infra/backup.sh`):

```bash
# Make script executable
chmod +x /usr/local/bin/ecclesia-backup

# Run manual backup
/usr/local/bin/ecclesia-backup

# Set up cron job for daily backups at 2 AM
crontab -e
# Add:
0 2 * * * /usr/local/bin/ecclesia-backup
```

### Backup Retention Policy

**Recommended retention:**
- Daily backups: 7 days
- Weekly backups: 4 weeks
- Monthly backups: 12 months (for compliance)

### Testing Backups

**Test restore procedure quarterly:**

```bash
# List available backups
ls -lh /var/backups/ecclesia/

# Restore from backup
gunzip < backup_20260214_020000.sql.gz | \
  docker exec -i ecclesia-postgres psql -U ecclesia_user ecclesia_db

# Verify data integrity
docker exec ecclesia-postgres psql -U ecclesia_user ecclesia_db -c "SELECT COUNT(*) FROM users;"
```

### Off-Site Backups (Recommended)

For critical data, store backups off-site:

**Option 1: Cloud Storage**
```bash
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Configure (Google Drive, Dropbox, etc.)
rclone config

# Sync backups
rclone sync /var/backups/ecclesia remote:ecclesia-backups
```

**Option 2: AWS S3**
```bash
# Install AWS CLI
sudo apt install awscli -y

# Configure
aws configure

# Upload backup
aws s3 cp backup.sql.gz s3://your-bucket/backups/
```

---

## Monitoring & Observability

### Health Check Endpoint

Ecclesia Core includes a built-in health check endpoint:

```
GET /health
```

Response:
```json
{
  "status": "ok",
  "app": "Ecclesia Core",
  "version": "1.0.0"
}
```

### Recommended Monitoring Tools (Free Tiers)

#### 1. UptimeRobot (Uptime Monitoring)
- **Cost**: Free for up to 50 monitors
- **Features**: 5-minute checks, email alerts
- **Setup**:
  1. Sign up at [uptimerobot.com](https://uptimerobot.com)
  2. Add monitor for your `/health` endpoint
  3. Configure alert contacts

#### 2. Sentry (Error Tracking)
- **Cost**: Free for 5,000 errors/month
- **Features**: Real-time error tracking, stack traces
- **Setup**:
  ```bash
  # Install Sentry SDK
  pip install sentry-sdk[fastapi]
  ```

  Add to `backend/app/main.py`:
  ```python
  import sentry_sdk

  sentry_sdk.init(
      dsn="your-sentry-dsn",
      environment=settings.ENVIRONMENT,
  )
  ```

#### 3. Better Stack (formerly Logtail)
- **Cost**: Free for 1GB/month
- **Features**: Log aggregation, search, alerts
- **Setup**: Follow provider documentation

#### 4. Grafana Cloud (Metrics & Dashboards)
- **Cost**: Free tier available
- **Features**: Metrics, logs, traces
- **Advanced**: For larger deployments

### What to Monitor

**Critical Alerts:**
- API downtime (health check fails)
- Database connection errors
- High error rate (>5% of requests)
- Disk space >80%
- Memory usage >90%

**Warning Alerts:**
- Response time >2 seconds
- Database connection pool exhaustion
- SSL certificate expiring <30 days
- Backup failures

### Simple Monitoring Script (Self-Hosted)

Create `/usr/local/bin/ecclesia-monitor`:

```bash
#!/bin/bash
# Simple monitoring script

HEALTH_URL="https://your-domain.com/health"
ALERT_EMAIL="admin@your-church.org"

# Check health endpoint
if ! curl -sf "$HEALTH_URL" > /dev/null; then
    echo "Ecclesia Core is DOWN!" | mail -s "ALERT: Ecclesia Down" "$ALERT_EMAIL"
fi

# Check disk space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "Disk usage is ${DISK_USAGE}%" | mail -s "WARNING: High Disk Usage" "$ALERT_EMAIL"
fi
```

Run every 5 minutes:
```bash
crontab -e
# Add:
*/5 * * * * /usr/local/bin/ecclesia-monitor
```

### Logging Best Practices

**Production logging configuration:**

```python
# backend/app/config.py
import logging

if settings.ENVIRONMENT == "production":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(level=logging.DEBUG)
```

**Log important events:**
- User authentication (success/failure)
- Data modifications
- API errors
- Performance issues

---

## Cost Optimization

### Tips to Reduce Costs

1. **Start Small, Scale Up**
   - Begin with smallest tier
   - Monitor usage
   - Upgrade only when needed

2. **Use Managed Databases**
   - Saves DevOps time
   - Automatic backups included
   - Better than DIY for small teams

3. **Leverage Free Tiers**
   - Monitoring: UptimeRobot, Sentry free tiers
   - SSL: Let's Encrypt (free)
   - CDN: Cloudflare free tier

4. **Optimize Database Queries**
   - Add indexes for frequent queries
   - Use connection pooling
   - Regular VACUUM on PostgreSQL

5. **Image Optimization**
   - Use Alpine-based Docker images
   - Multi-stage builds
   - Remove unnecessary dependencies

6. **Caching**
   - Enable browser caching
   - Consider Redis for session storage (if needed)
   - Cache API responses where appropriate

7. **Regular Maintenance**
   - Clean old logs
   - Archive historical data
   - Remove unused resources

### Cost Comparison Table

| Service | Small Church | Medium Church | Large Church |
|---------|--------------|---------------|--------------|
| **Railway** | $5-10/mo | $15-25/mo | $30-50/mo |
| **Render** | $7-15/mo | $20-35/mo | $40-70/mo |
| **DigitalOcean** | $12-20/mo | $25-40/mo | $60-100/mo |
| **Self-Hosted** | $5-10/mo | $10-20/mo | $20-40/mo |

*Estimates include all infrastructure (database, hosting, backups)*

---

## Troubleshooting

### Common Issues and Solutions

#### 1. CORS Errors

**Symptom**: Frontend can't connect to API, browser console shows CORS errors

**Solution**:
```env
# Backend .env
CORS_ORIGINS=https://your-frontend-domain.com

# Or for multiple domains
CORS_ORIGINS=https://ecclesia.com,https://www.ecclesia.com
```

Restart backend after changing environment variables.

#### 2. Database Connection Failed

**Symptom**: Backend logs show "connection refused" or "authentication failed"

**Solutions**:
- Verify `DATABASE_URL` format:
  ```
  postgresql://username:password@host:port/database
  ```
- Check database is running: `docker ps` or platform dashboard
- Verify credentials match database configuration
- Check firewall rules (self-hosted)
- Ensure database accepts connections from backend IP

#### 3. Frontend Can't Reach API

**Symptom**: API calls timeout or return 404

**Solutions**:
- Verify `VITE_API_URL` is correct
- Check backend is running and healthy: `/health`
- Verify CORS is configured properly
- Check network connectivity between services
- Inspect browser console for errors

#### 4. JWT Token Errors

**Symptom**: "Invalid token" or "Token expired" errors

**Solutions**:
- Ensure `SECRET_KEY` is set and consistent
- Verify `ALGORITHM` matches (default: HS256)
- Check token expiration time is reasonable
- Clear browser cookies/localStorage
- Verify system time is synchronized (NTP)

#### 5. Migration Failures

**Symptom**: "Table already exists" or migration errors

**Solutions**:
```bash
# Check current migration version
alembic current

# Stamp database to current version (if tables exist)
alembic stamp head

# Or start fresh (DANGER: loses data)
alembic downgrade base
alembic upgrade head
```

#### 6. 502 Bad Gateway (Nginx)

**Symptom**: Nginx returns 502 error

**Solutions**:
- Check backend is running: `docker ps`
- Verify proxy_pass URL in nginx.conf
- Check backend logs: `docker logs ecclesia-backend`
- Verify network configuration
- Check file permissions

#### 7. High Memory Usage

**Symptom**: Container or server runs out of memory

**Solutions**:
- Reduce database connection pool size
- Add swap space (self-hosted)
- Upgrade to larger instance
- Check for memory leaks in logs
- Optimize queries

#### 8. Slow Performance

**Symptom**: Slow page loads, API timeouts

**Solutions**:
- Check database query performance
- Add indexes to frequently queried columns
- Enable connection pooling
- Optimize frontend bundle size
- Use CDN for static assets
- Check database VACUUM status

### Debug Mode (Development Only)

**Enable detailed error messages:**

```env
ENVIRONMENT=development
DEBUG=true
```

⚠️ **Never use DEBUG=true in production** - exposes sensitive information

### Getting Help

1. **Check logs first**:
   ```bash
   # Platform-specific
   # Railway: Dashboard → Deployments → Logs
   # Render: Dashboard → Logs
   # DigitalOcean: App → Logs

   # Self-hosted
   docker-compose logs -f
   docker logs ecclesia-backend
   docker logs ecclesia-postgres
   ```

2. **GitHub Issues**: Report bugs at repository issues page

3. **Community Support**: Check discussions or forums

4. **Professional Support**: Consider hiring DevOps consultant for complex issues

---

## Production Readiness Checklist

Use this checklist before launching to production:

### Security ✅

- [ ] `SECRET_KEY` generated with `openssl rand -hex 32`
- [ ] `CORS_ORIGINS` set to specific domains (no `*`)
- [ ] Strong database password (20+ characters)
- [ ] HTTPS/SSL certificate configured
- [ ] `ENVIRONMENT=production` set
- [ ] `DEBUG=false` (or removed)
- [ ] All default passwords changed
- [ ] Security headers configured
- [ ] API documentation restricted (optional)
- [ ] Rate limiting configured

### Infrastructure ✅

- [ ] Domain name registered and configured
- [ ] DNS records properly set
- [ ] SSL certificate auto-renewal tested
- [ ] Firewall rules configured (if applicable)
- [ ] Email service configured (if needed)
- [ ] CDN configured (optional)

### Database ✅

- [ ] Migrations run successfully
- [ ] Seed data created (admin user)
- [ ] Backups configured and tested
- [ ] Connection pooling enabled
- [ ] Indexes created for frequent queries
- [ ] Backup restoration tested

### Application ✅

- [ ] All environment variables set
- [ ] Frontend connects to backend successfully
- [ ] Authentication flow tested
- [ ] All critical features working
- [ ] Error handling tested
- [ ] Performance testing completed
- [ ] Load testing performed (optional)

### Monitoring ✅

- [ ] Uptime monitoring configured
- [ ] Error tracking integrated
- [ ] Log aggregation set up (optional)
- [ ] Alert notifications configured
- [ ] Health check endpoint verified
- [ ] Dashboard created (optional)

### Documentation ✅

- [ ] Admin credentials documented (securely)
- [ ] Deployment process documented
- [ ] Backup/restore procedure documented
- [ ] Troubleshooting guide created
- [ ] User documentation prepared
- [ ] Contact information updated

### Testing ✅

- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] End-to-end testing completed
- [ ] User acceptance testing passed
- [ ] Cross-browser testing done
- [ ] Mobile responsiveness verified

### Compliance & Legal ✅

- [ ] Privacy policy created
- [ ] Terms of service created
- [ ] GDPR compliance verified (if applicable)
- [ ] Data retention policy defined
- [ ] User consent mechanisms in place

### Launch Preparation ✅

- [ ] Maintenance window scheduled
- [ ] Communication plan ready
- [ ] Rollback plan documented
- [ ] Support team trained
- [ ] Incident response plan created
- [ ] Success metrics defined

---

## Next Steps After Deployment

1. **Monitor for 48 hours**: Watch logs and metrics closely
2. **Test all features**: Verify everything works in production
3. **Create admin user**: Set up initial users
4. **Configure notifications**: Set up email alerts
5. **Document processes**: Record any custom configurations
6. **Plan for growth**: Monitor usage and plan scaling
7. **Regular maintenance**: Schedule weekly health checks

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Let's Encrypt](https://letsencrypt.org/)
- [OWASP Security Best Practices](https://owasp.org/)

---

## Support

For deployment assistance:
- GitHub Issues: [ecclesia-core/issues](https://github.com/your-repo/ecclesia-core/issues)
- Email: support@your-church.org
- Documentation: [Full documentation](../README.md)

---

*Last updated: February 2026*
