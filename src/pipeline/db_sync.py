import pandas as pd
import os
import logging
from sqlalchemy import create_engine, text

# Config de logs
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data", "clean_data"))

# Conexion a la base de datos
DB_URL = "postgresql://postgres:1234@localhost:5432/SmartChefBBDD"
engine = create_engine(DB_URL)

def upsert_context(df):
    """ Actualiza si la fecha ya existe o inserta si es nueva """
    query = text("""
        INSERT INTO dim_context (date, is_holiday, es_vispera, day_of_week, temp_max, precipitation)
        VALUES (:date, :is_holiday, :es_vispera, :day_of_week, :temp_max, :precipitation)
        ON CONFLICT (date) DO UPDATE SET
            temp_max = EXCLUDED.temp_max,
            precipitation = EXCLUDED.precipitation,
            es_vispera = EXCLUDED.es_vispera,
            is_holiday = EXCLUDED.is_holiday,
            day_of_week = EXCLUDED.day_of_week;
    """)
    with engine.begin() as conn:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        conn.execute(query, df.to_dict(orient='records'))

def sync_incremental_table(df, table_name, keys):
    """ Filtra registros que ya estan en la BD para no duplicar """
    
    # Quitar duplicados del propio dataframe antes de comparar
    df = df.drop_duplicates(subset=keys)
    
    logger.info(f"Comprobando datos nuevos para {table_name}...")
    try:
        # Sacar claves existentes para comparar
        key_cols = ", ".join(keys)
        query = f"SELECT {key_cols} FROM {table_name}"
        with engine.connect() as conn:
            existing_data = pd.read_sql(query, conn)
        
        # Forzar strings para evitar fallos en el merge
        for key in keys:
            df[key] = df[key].astype(str)
            existing_data[key] = existing_data[key].astype(str)

        # Quedarse solo con lo que no esta en la base de datos
        df_merged = df.merge(existing_data, on=keys, how='left', indicator=True)
        df_new = df_merged[df_merged['_merge'] == 'left_only'].drop(columns=['_merge'])
    except Exception as e:
        logger.warning(f"Fallo al comparar {table_name}, se intenta carga completa: {e}")
        df_new = df

    if not df_new.empty:
        logger.info(f"Insertando {len(df_new)} registros nuevos en {table_name}")
        df_new.to_sql(table_name, engine, if_exists='append', index=False, chunksize=500)
        return len(df_new)
    return 0

def sync_incremental():
    logger.info("Iniciando sincronización incremental...")
    try:
        # 1. Carga de Contexto (Clima/Festivos)
        path_context = os.path.join(CLEAN_FOLDER, 'dim_context.csv')
        if os.path.exists(path_context):
            df = pd.read_csv(path_context, encoding='utf-8')
            upsert_context(df)
            logger.info("Tabla dim_context: OK")

        # 2. Carga de Platos
        path_menu = os.path.join(CLEAN_FOLDER, 'maestro_platos_limpio.csv')
        if os.path.exists(path_menu):
            df = pd.read_csv(path_menu, encoding='utf-8')
            n = sync_incremental_table(df, 'dim_menu', ['id_plato'])
            logger.info(f"Tabla dim_menu: {n} registros añadidos")

        # 3. Carga de Recetas
        path_recipes = os.path.join(CLEAN_FOLDER, 'recetas_ingredientes_limpio.csv')
        if os.path.exists(path_recipes):
            df = pd.read_csv(path_recipes, encoding='utf-8')
            n = sync_incremental_table(df, 'dim_recipes', ['id_plato', 'ingrediente'])
            logger.info(f"Tabla dim_recipes: {n} registros añadidos")

        # 4. Carga de Ventas
        path_sales = os.path.join(CLEAN_FOLDER, 'ventas_historico_limpio.csv')
        if os.path.exists(path_sales):
            df = pd.read_csv(path_sales, encoding='utf-8')
            # Columnas necesarias para la tabla fact_sales
            cols_db = ['id_ticket', 'fecha', 'turno', 'id_plato', 'cantidad']
            n = sync_incremental_table(df[cols_db], 'fact_sales', ['id_ticket', 'id_plato'])
            logger.info(f"Tabla fact_sales: {n} registros añadidos")

        logger.info("Sincronización finalizada correctamente.")

    except Exception as e:
        logger.error(f"Error en el proceso: {e}")

if __name__ == "__main__":
    sync_incremental()