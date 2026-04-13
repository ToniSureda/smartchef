import pandas as pd
import holidays
import requests
from datetime import datetime, timedelta
import os
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# CONFIGURACIÓN DE RUTAS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ajustado a la estructura de carpetas estándar
CLEAN_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'clean_data', 'dim_context.csv'))

LAT, LON = 41.3851, 2.1734 # Barcelona

def get_weather_data(start_date, end_date):
    yesterday = (datetime.now() - timedelta(days=1)).date()
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()

    all_data = []

    if start_dt <= yesterday:
        hist_end = min(end_dt, yesterday)
        logger.info(f"Consultando histórico: {start_date} al {hist_end}")
        url_hist = "https://archive-api.open-meteo.com/v1/archive"
        params_hist = {
            "latitude": LAT, "longitude": LON,
            "start_date": start_date, "end_date": hist_end.strftime("%Y-%m-%d"),
            "daily": ["temperature_2m_max", "precipitation_sum"],
            "timezone": "Europe/Madrid"
        }
        res = requests.get(url_hist, params=params_hist).json()
        if "daily" in res:
            all_data.append(pd.DataFrame({
                "date": pd.to_datetime(res["daily"]["time"]),
                "temp_max": res["daily"]["temperature_2m_max"],
                "precipitation": res["daily"]["precipitation_sum"]
            }))

    if end_dt > yesterday:
        fore_start = max(start_dt, yesterday + timedelta(days=1))
        logger.info(f"Consultando predicción: {fore_start} al {end_date}")
        url_fore = "https://api.open-meteo.com/v1/forecast"
        params_fore = {
            "latitude": LAT, "longitude": LON,
            "start_date": fore_start.strftime("%Y-%m-%d"), "end_date": end_date,
            "daily": ["temperature_2m_max", "precipitation_sum"],
            "timezone": "Europe/Madrid"
        }
        res = requests.get(url_fore, params=params_fore).json()
        if "daily" in res:
            all_data.append(pd.DataFrame({
                "date": pd.to_datetime(res["daily"]["time"]),
                "temp_max": res["daily"]["temperature_2m_max"],
                "precipitation": res["daily"]["precipitation_sum"]
            }))

    return pd.concat(all_data).drop_duplicates()

def add_features(df):
    es_holidays = holidays.CountryHoliday('ESP', subdiv='CT')
    df['is_holiday'] = df['date'].apply(lambda x: 1 if x in es_holidays else 0)
    df = df.sort_values('date')
    df['es_vispera'] = df['is_holiday'].shift(-1).fillna(0).astype(int)
    
    # Mantener consistencia con nombres sin acentos para BBDD
    days_map = {0:'Lunes', 1:'Martes', 2:'Miercoles', 3:'Jueves', 4:'Viernes', 5:'Sabado', 6:'Domingo'}
    df['day_of_week'] = df['date'].dt.dayofweek.map(days_map)
    
    df['temp_max'] = df['temp_max'].round(1)
    df['precipitation'] = df['precipitation'].round(2)
    return df

def run_init():
    logger.info("Iniciando generación de dim_context...")
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    
    start = "2024-01-01"
    end = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    try:
        df = get_weather_data(start, end)
        df = add_features(df)
        
        cols = ['date', 'is_holiday', 'es_vispera', 'day_of_week', 'temp_max', 'precipitation']
        
        # Guardado con formato ISO y encoding seguro
        df[cols].to_csv(
            CLEAN_PATH, 
            index=False, 
            date_format='%Y-%m-%d', 
            encoding='utf-8',
            quoting=1,
            lineterminator='\n'
        )
        
        logger.info(f"Dataset guardado exitosamente en: {CLEAN_PATH}")
    except Exception as e:
        logger.error(f"Error en el proceso: {e}")

if __name__ == "__main__":
    run_init()