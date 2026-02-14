# Ecclesia Core - Infrastructure

Infrastructure documentation and deployment configurations for Ecclesia Core.

## Available Documentation

### 📘 [DEPLOY.md](DEPLOY.md) - Complete Deployment Guide
Comprehensive guide covering all deployment options, from cloud platforms to self-hosted VPS.

**Includes:**
- Railway.app (recommended for MVP)
- Render.com
- DigitalOcean App Platform
- Self-Hosted VPS deployment
- Security checklist
- Backup strategies
- Monitoring setup
- Troubleshooting guide

### 📄 [nginx.conf.example](nginx.conf.example) - Nginx Configuration
Example Nginx reverse proxy configuration for self-hosted deployments.

**Features:**
- HTTP to HTTPS redirect
- SSL/TLS configuration
- Security headers
- Backend API proxy
- Frontend serving
- Health check endpoint

### 🔧 [backup.sh](backup.sh) - Database Backup Script
Automated PostgreSQL backup script with retention management.

**Features:**
- Automated backups with compression
- Configurable retention period (default: 7 days)
- Backup verification
- Logging
- Easy cron integration

## Quick Reference

### Deployment Options Comparison

| Platform | Monthly Cost | Setup Time | Difficulty | Best For |
|----------|--------------|------------|------------|----------|
| Railway.app | $5-10 | 15 min | Easy | Quick MVP, beginners |
| Render.com | $7-15 | 20 min | Easy | Stable production |
| DigitalOcean | $12-20 | 30 min | Medium | Scaling, growth |
| Self-Hosted VPS | $5-10 | 1-2 hours | Advanced | Full control, cost-effective |

### Essential Files

```
infra/
├── DEPLOY.md              # Complete deployment guide
├── nginx.conf.example     # Nginx reverse proxy config
├── backup.sh             # Database backup script
└── README.md             # This file
```

### Quick Start

1. **Choose a deployment option** from [DEPLOY.md](DEPLOY.md)
2. **Follow the step-by-step guide** for your chosen platform
3. **Complete the security checklist** before going live
4. **Set up automated backups** using backup.sh (for self-hosted)
5. **Configure monitoring** for production readiness

### Getting Help

- For deployment issues, see [Troubleshooting](DEPLOY.md#troubleshooting)
- For security concerns, check [Security Checklist](DEPLOY.md#security-checklist)
- For general questions, open a GitHub issue

## Cloud-Agnostic Approach

This project is designed to be deployable on any cloud provider or on-premises infrastructure. The documentation focuses on low-cost, easy-to-manage options suitable for small to medium churches.

## Future Enhancements

Potential additions for advanced deployments:
- Docker Swarm orchestration
- Kubernetes manifests
- Infrastructure as Code (Terraform)
- Advanced monitoring with Prometheus/Grafana
- Multi-region deployment
- High availability configuration
