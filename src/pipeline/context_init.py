import pandas as pd
import holidays
import requests
from datetime import datetime, timedelta
import os

# --- CONFIGURACIÓN DE RUTAS BLINDADA ---
# Detecta la ubicación real del script y construye la ruta hacia data/clean
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
CLEAN_PATH = os.path.join(PROJECT_ROOT, 'data', 'clean_data', 'dim_context.csv')

LAT, LON = 41.3851, 2.1734 # Barcelona

def get_weather_data(start_date, end_date):
    yesterday = (datetime.now() - timedelta(days=1)).date()
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()

    all_data = []

    # 1. PARTE HISTÓRICA (Archive)
    if start_dt <= yesterday:
        hist_end = min(end_dt, yesterday)
        print(f"📡 Consultando histórico: {start_date} al {hist_end}")
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

    # 2. PARTE FUTURA (Forecast)
    if end_dt > yesterday:
        fore_start = max(start_dt, yesterday + timedelta(days=1))
        print(f"📡 Consultando predicción: {fore_start} al {end_date}")
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
    days_map = {0:'Lunes', 1:'Martes', 2:'Miércoles', 3:'Jueves', 4:'Viernes', 5:'Sábado', 6:'Domingo'}
    df['day_of_week'] = df['date'].dt.dayofweek.map(days_map)
    return df

def run_init():
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    start = "2024-01-01"
    end = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    df = get_weather_data(start, end)
    df = add_features(df)
    
    cols = ['date', 'is_holiday', 'es_vispera', 'day_of_week', 'temp_max', 'precipitation']
    df[cols].to_csv(CLEAN_PATH, index=False)
    print(f"✅ CSV Creado en: {CLEAN_PATH}")
    print(f"📊 Registros: {len(df)}")

if __name__ == "__main__":
    run_init()