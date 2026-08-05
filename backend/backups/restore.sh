#!/bin/bash
set -e

until pg_isready -h localhost -U $POSTGRES_USER; do
  echo "Waiting for PostgreSQL to start..."
  sleep 1
done

if [ -f /backups/qitc_db_backup_20250321_013820.dump ]; then
  echo "Restoring database from backup..."

  psql -U $POSTGRES_USER -d postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB;"
  psql -U $POSTGRES_USER -d postgres -c "CREATE DATABASE $POSTGRES_DB;"

  pg_restore -U $POSTGRES_USER -d $POSTGRES_DB --clean --if-exists /backups/qitc_db_backup_20250321_013820.dump
  echo "Database restored successfully!"
else
  echo "No backup file found. Skipping restoration."
fi