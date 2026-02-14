#!/bin/bash
#
# Ecclesia Core - Database Backup Script
#
# This script creates automated backups of the PostgreSQL database
# and manages backup retention (keeps last 7 days by default)
#
# Usage:
#   ./backup.sh                    # Run backup with default settings
#   ./backup.sh --retention 14     # Keep backups for 14 days
#   ./backup.sh --help             # Show help
#
# Setup for automated backups:
#   1. Make executable: chmod +x backup.sh
#   2. Copy to system bin: sudo cp backup.sh /usr/local/bin/ecclesia-backup
#   3. Add to crontab: crontab -e
#      0 2 * * * /usr/local/bin/ecclesia-backup
#

set -e  # Exit on error

# ==========================================
# Configuration
# ==========================================

# Backup directory
BACKUP_DIR="/var/backups/ecclesia"

# Database configuration (from .env or override here)
DB_CONTAINER="${DB_CONTAINER:-ecclesia-postgres}"
DB_NAME="${POSTGRES_DB:-ecclesia_db}"
DB_USER="${POSTGRES_USER:-ecclesia_user}"

# Retention period (days)
RETENTION_DAYS="${RETENTION_DAYS:-7}"

# Backup filename format
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql.gz"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

# Log file
LOG_FILE="${BACKUP_DIR}/backup.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==========================================
# Functions
# ==========================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

show_help() {
    cat << EOF
Ecclesia Core - Database Backup Script

Usage: $0 [OPTIONS]

Options:
    --retention DAYS    Number of days to keep backups (default: 7)
    --backup-dir PATH   Backup directory (default: /var/backups/ecclesia)
    --container NAME    Database container name (default: ecclesia-postgres)
    --help             Show this help message

Examples:
    $0                          # Run backup with defaults
    $0 --retention 14           # Keep backups for 14 days
    $0 --backup-dir /backups    # Use custom backup directory

Environment Variables:
    DB_CONTAINER        Database container name
    POSTGRES_DB         Database name
    POSTGRES_USER       Database user
    RETENTION_DAYS      Retention period in days

EOF
    exit 0
}

check_requirements() {
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed or not in PATH"
    fi

    # Check if database container is running
    if ! docker ps --format '{{.Names}}' | grep -q "^${DB_CONTAINER}$"; then
        error "Database container '${DB_CONTAINER}' is not running"
    fi

    log "Requirements check passed"
}

create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log "Creating backup directory: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR" || error "Failed to create backup directory"
    fi
}

perform_backup() {
    log "Starting backup of database '${DB_NAME}'..."

    # Create backup using pg_dump
    if docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_PATH"; then
        success "Backup created: $BACKUP_FILE"

        # Get backup size
        BACKUP_SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
        log "Backup size: $BACKUP_SIZE"

        # Verify backup integrity
        if gunzip -t "$BACKUP_PATH" 2>/dev/null; then
            success "Backup integrity verified"
        else
            error "Backup file is corrupted!"
        fi
    else
        error "Failed to create backup"
    fi
}

cleanup_old_backups() {
    log "Cleaning up backups older than $RETENTION_DAYS days..."

    # Count backups before cleanup
    BEFORE_COUNT=$(find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f | wc -l)

    # Remove old backups
    DELETED=$(find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete -print | wc -l)

    if [ "$DELETED" -gt 0 ]; then
        log "Deleted $DELETED old backup(s)"
    else
        log "No old backups to delete"
    fi

    # Count remaining backups
    AFTER_COUNT=$(find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f | wc -l)
    log "Total backups: $AFTER_COUNT"
}

list_backups() {
    log "Available backups:"
    find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -printf "%T+ %s %p\n" | sort -r | while read -r line; do
        TIMESTAMP=$(echo "$line" | awk '{print $1}')
        SIZE=$(echo "$line" | awk '{print $2}')
        FILE=$(echo "$line" | awk '{print $3}')
        FILENAME=$(basename "$FILE")
        SIZE_HUMAN=$(numfmt --to=iec-i --suffix=B "$SIZE" 2>/dev/null || echo "$SIZE bytes")
        echo "  - $FILENAME ($SIZE_HUMAN) - $TIMESTAMP"
    done | tee -a "$LOG_FILE"
}

send_notification() {
    # Optional: Send notification on backup completion
    # Uncomment and configure for email notifications

    # if command -v mail &> /dev/null; then
    #     echo "Backup completed successfully: $BACKUP_FILE" | \
    #         mail -s "Ecclesia Backup Success" admin@your-church.org
    # fi

    # Or use a webhook (e.g., Slack, Discord)
    # curl -X POST -H 'Content-type: application/json' \
    #     --data '{"text":"Ecclesia backup completed"}' \
    #     YOUR_WEBHOOK_URL

    :  # Do nothing by default
}

# ==========================================
# Parse Arguments
# ==========================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --retention)
            RETENTION_DAYS="$2"
            shift 2
            ;;
        --backup-dir)
            BACKUP_DIR="$2"
            shift 2
            ;;
        --container)
            DB_CONTAINER="$2"
            shift 2
            ;;
        --help)
            show_help
            ;;
        *)
            error "Unknown option: $1\nUse --help for usage information"
            ;;
    esac
done

# ==========================================
# Main Execution
# ==========================================

log "==================================================="
log "Ecclesia Core - Database Backup"
log "==================================================="
log "Container: $DB_CONTAINER"
log "Database: $DB_NAME"
log "Backup Directory: $BACKUP_DIR"
log "Retention: $RETENTION_DAYS days"
log "==================================================="

# Run backup process
check_requirements
create_backup_dir
perform_backup
cleanup_old_backups
list_backups
send_notification

log "==================================================="
success "Backup process completed successfully!"
log "==================================================="

exit 0
