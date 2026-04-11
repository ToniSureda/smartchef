import pandas as pd
import numpy as np
import os
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configuración de rutas relativas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(BASE_DIR, '../../data/raw_data/ventas_historico_sucio.csv')
MASTER_PATH = os.path.join(BASE_DIR, '../../data/clean_data/maestro_platos_limpio.csv')
CLEAN_PATH = os.path.join(BASE_DIR, '../../data/clean_data/ventas_historico_limpio.csv')

def filter_anomalies(df):
    """Elimina registros con cantidades ilógicas u outliers."""
    # Filtramos cantidades negativas o superiores a 20 (umbral de error humano)
    return df[(df['cantidad'] > 0) & (df['cantidad'] <= 20)]

def run_ingest():
    logger.info("Iniciando proceso de ingesta y limpieza...")

    if not os.path.exists(RAW_PATH) or not os.path.exists(MASTER_PATH):
        logger.error("Error: Faltan archivos de entrada en data/")
        return

    # 1. Carga de datos
    df = pd.read_csv(RAW_PATH)
    master_df = pd.read_csv(MASTER_PATH)
    initial_rows = len(df)

    # 2. Limpieza inicial: Duplicados exactos y nulos en IDs
    df = df.drop_duplicates()
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df.dropna(subset=['fecha', 'id_ticket', 'id_plato'])

    # 3. Normalización e Imputación de turnos por ticket
    # Limpiamos strings y rellenamos turnos faltantes usando el contexto del mismo ticket
    df['turno'] = df['turno'].astype(str).str.strip().str.capitalize()
    df['turno'] = df.groupby('id_ticket')['turno'].transform(
        lambda x: x.replace(['Nan', 'None', 'Null', ''], np.nan).ffill().bfill()
    )
    df = df[df['turno'].isin(['Comida', 'Cena'])]

    # 4. Validación de tipos y anomalías
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df = filter_anomalies(df)
    df['cantidad'] = df['cantidad'].astype(int)

    # 5. Integridad referencial con maestro de platos
    # Solo mantenemos ventas de platos que existen en nuestro catálogo limpio
    valid_menu_ids = master_df['id_plato'].unique()
    df = df[df['id_plato'].isin(valid_menu_ids)]

    # 6. Enriquecimiento (Merge)
    # Añadimos info del maestro para facilitar el análisis posterior
    final_df = df.merge(
        master_df[['id_plato', 'nombre_plato', 'categoria']], 
        on='id_plato', 
        how='left'
    )

    # 7. Exportación a carpeta clean
    final_df.to_csv(CLEAN_PATH, index=False)
    
    health_score = (len(final_df) / initial_rows) * 100
    logger.info(f"Proceso finalizado. Health Score: {health_score:.2f}%")
    logger.info(f"Dataset guardado en: {CLEAN_PATH}")

if __name__ == "__main__":
    run_ingest()