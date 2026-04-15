#!/bin/sh

echo "⏳ Iniciando Pipeline Integral de SmartChef (3:00 AM)..."

# 1. ACTUALIZACIÓN DE DATOS BRUTOS
python /app/generate_raw_historic.py
python /app/ingest.py
python /app/context_update.py

# 2. SINCRONIZACIÓN BBDD (Para que el ML lea datos frescos)
python /app/db_sync.py

# 3. INTELIGENCIA ARTIFICIAL (NUEVOS PASOS)
echo "🧠 Entrenando modelo y generando predicciones..."
# Entrenamos con los últimos datos y generamos el CSV de predicciones
python /app/backend/services/train_predictions.py
echo "📥 Importando predicciones a PostgreSQL..."
# Metemos ese CSV en la tabla fact_predictions para que la API lo vea
python /app/backend/services/import_predictions.py
echo "✅ Proceso completo. Sistema actualizado y listo para el servicio."