#!/bin/bash
set -e

# Script de inicializacion y poblacion de la base de datos
echo "Inicio del proceso de restauracion del volcado de datos..."
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-privileges /tmp/SmartChefBBDD.sql
echo "Operacion completada. Estructura y datos restaurados exitosamente en el sistema."