#!/bin/bash
set -e
echo "⏳ Iniciando la restauración de tu archivo custom (pg_restore)..."
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-privileges /tmp/SmartChefBBDD.sql
echo "✅ Base de datos restaurada con éxito."