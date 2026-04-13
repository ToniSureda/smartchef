import pandas as pd
import os
import logging
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
CLEAN_FOLDER = os.path.join(PROJECT_ROOT, 'data', 'clean_data')

DB_URL = "postgresql://postgres:tu_password@localhost:5432/smartchef_db"
engine = create_engine(DB_URL)

def upsert_context(df):
    """Inserta o actualiza el clima y festivos basándose en la fecha"""
    query = text("""
        INSERT INTO dim_context (date, is_holiday, es_vispera, day_of_week, temp_max, precipitation)
        VALUES (:date, :is_holiday, :es_vispera, :day_of_week, :temp_max, :precipitation)
        ON CONFLICT (date) DO UPDATE SET
            temp_max = EXCLUDED.temp_max,
            precipitation = EXCLUDED.precipitation,
            es_vispera = EXCLUDED.es_vispera,
            is_holiday = EXCLUDED.is_holiday;
    """)
    with engine.connect() as conn:
        for _, row in df.iterrows():
            conn.execute(query, row.to_dict())
        conn.commit()

def insert_only_new_sales(df):
    """Inserta solo los tickets que NO existen en la base de datos"""
    # 1. Traer IDs de tickets que ya están en la BBDD
    with engine.connect() as conn:
        existing_ids = pd.read_sql("SELECT DISTINCT id_ticket FROM fact_sales", conn)['id_ticket'].tolist()
    
    # 2. Filtrar el DataFrame para dejar solo lo nuevo
    df_new = df[~df['id_ticket'].isin(existing_ids)]
    
    if not df_new.empty:
        df_new[['id_ticket', 'fecha', 'turno', 'id_plato', 'cantidad']].to_sql(
            'fact_sales', engine, if_exists='append', index=False
        )
        return len(df_new)
    return 0

def sync_incremental():
    try:
        # --- 1. Sincronizar Contexto (UPSERT) ---
        # El clima cambia (la predicción de ayer hoy es realidad), así que actualizamos.
        df_context = pd.read_csv(os.path.join(CLEAN_FOLDER, 'dim_context.csv'))
        upsert_context(df_context)
        logger.info("✅ dim_context actualizado (Upsert).")

        # --- 2. Sincronizar Ventas (SOLO NUEVAS) ---
        # Las ventas pasadas no cambian, solo añadimos lo que no esté.
        df_sales = pd.read_csv(os.path.join(CLEAN_FOLDER, 'ventas_historico_limpio.csv'))
        nuevos = insert_only_new_sales(df_sales)
        logger.info(f"✅ fact_sales: {nuevos} registros nuevos añadidos.")

        # --- 3. Maestro y Recetas (REPLACE) ---
        # Estas tablas son pequeñas, aquí sí solemos sobreescribir porque si 
        # cambias un precio o un ingrediente, queremos la versión más reciente.
        pd.read_csv(os.path.join(CLEAN_FOLDER, 'maestro_platos_limpio.csv')).to_sql(
            'dim_menu', engine, if_exists='replace', index=False
        )
        pd.read_csv(os.path.join(CLEAN_FOLDER, 'recetas_ingredientes_limpio.csv')).to_sql(
            'dim_recipes', engine, if_exists='replace', index=False
        )
        logger.info("✅ dim_menu y dim_recipes refrescados.")

    except Exception as e:
        logger.error(f"❌ Error en la sincronización: {e}")

if __name__ == "__main__":
    sync_incremental()