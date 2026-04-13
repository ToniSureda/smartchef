import pandas as pd
import requests
import os
import logging
from datetime import datetime, timedelta
# Importamos la lógica, pero definimos la ruta aquí de nuevo para seguridad total
from context_init import add_features, LAT, LON, get_weather_data

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURACIÓN DE RUTAS BLINDADA (Misma que en init) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
CLEAN_PATH = os.path.join(PROJECT_ROOT, 'data', 'clean_data', 'dim_context.csv')

def update_incremental():
    if not os.path.exists(CLEAN_PATH):
        logger.error(f"❌ No se encontró el archivo en: {CLEAN_PATH}")
        logger.info("Ejecuta primero context_init.py")
        return

    logger.info("Iniciando actualización diaria...")
    
    # 1. Cargar
    df_old = pd.read_csv(CLEAN_PATH)
    df_old['date'] = pd.to_datetime(df_old['date'])
    
    # 2. Rango actualización
    start_update = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    end_update = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    try:
        # 3. Datos nuevos
        df_new = get_weather_data(start_update, end_update)
        df_new['date'] = pd.to_datetime(df_new['date'])
        
        # 4. Unir y limpiar duplicados (priorizar lo nuevo)
        df_final = pd.concat([df_old, df_new]).drop_duplicates(subset='date', keep='last')
        
        # 5. Features
        df_final = add_features(df_final)
        
        # 6. Guardar
        df_final = df_final.sort_values('date')
        df_final.to_csv(CLEAN_PATH, index=False, date_format='%Y-%m-%d')
        
        logger.info(f"✅ Archivo actualizado con éxito.")
        logger.info(f"📅 Última fecha: {df_final['date'].max().date()}")
        logger.info(f"📍 Ruta: {CLEAN_PATH}")
        
    except Exception as e:
        logger.error(f"Error en el update: {e}")

if __name__ == "__main__":
    update_incremental()