#!/bin/sh

echo "Iniciando ejecución del pipeline de datos..."

# 1. Actualización de datos en crudo
python /app/generate_raw_historic.py
python /app/ingest.py
python /app/context_update.py

# 2. Sincronización de base de datos para garantizar información actualizada al modelo
python /app/db_sync.py

# 3. Entrenamiento con el dataset actualizado y generación de inferencias
echo "Ejecutando entrenamiento del modelo predictivo..."
python /app/backend/services/train_predictions.py

# Inserción de resultados en la tabla fact_predictions para exposición mediante API
echo "Volcando predicciones en la base de datos..."
python /app/backend/services/import_predictions.py

echo "Ejecución finalizada con éxito."