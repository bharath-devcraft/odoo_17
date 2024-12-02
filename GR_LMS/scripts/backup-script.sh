#!/bin/bash

# Get the current date in the format dd-mm-yyyy
DATE=$(date +%d-%m-%Y_%H-%M-%S)

# Define the backup filename with dynamic date
BACKUP_FILENAME="odoo-db-backup-${DATE}.sql"

# Execute the pg_dump command to create a backup with dynamic filename
docker exec -t postgres pg_dump -U odoo -d odoo-db > /Odoo/Catalyst/DB_Backups/${BACKUP_FILENAME}

# Optionally, print a message when backup is completed
echo "Backup completed: /db-backup/${BACKUP_FILENAME}"

