#!/bin/bash
# Odoo Daily Backup Script — runs on Cloud VM
BACKUP_DIR="/opt/odoo_backups"
DATE=$(date +%Y-%m-%d)
mkdir -p "$BACKUP_DIR"
docker exec odoo-db pg_dump -U odoo odoo > "$BACKUP_DIR/odoo_$DATE.sql"
# Keep last 7 days only
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
echo "Backup complete: odoo_$DATE.sql"
