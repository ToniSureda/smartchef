import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
PATH_MAESTRO = os.path.join(PROJECT_ROOT, 'data', 'clean_data', 'maestro_platos_limpio.csv')
PATH_OUTPUT = os.path.join(PROJECT_ROOT, 'data', 'raw_data', 'ventas_historico_sucio.csv')

def generate_daily_dirty_data():
    # 1. Cargar platos reales
    if not os.path.exists(PATH_MAESTRO):
        print(f"❌ Error: No encuentro {PATH_MAESTRO}. Créalo primero.")
        return
    
    df_maestro = pd.read_csv(PATH_MAESTRO)
    platos_reales = df_maestro['id_plato'].tolist()
    
    # 2. Determinar fecha de inicio
    if os.path.exists(PATH_OUTPUT):
        # Si el archivo existe, leemos la última fecha registrada
        df_old = pd.read_csv(PATH_OUTPUT)
        # Convertimos a datetime (manejando los formatos sucios que genera el propio script)
        df_old['fecha_dt'] = pd.to_datetime(df_old['fecha'], errors='coerce')
        ultima_fecha = df_old['fecha_dt'].max().date()
        fecha_inicio = ultima_fecha + timedelta(days=1)
        print(f"🔄 Continuando desde la última fecha: {ultima_fecha}")
    else:
        # Si no existe, empezamos en 2024
        fecha_inicio = datetime(2024, 1, 1).date()
        print(f"🆕 Creando nuevo archivo RAW desde {fecha_inicio}")

    fecha_hoy = datetime.now().date()
    
    if fecha_inicio > fecha_hoy:
        print("✅ Los datos ya están actualizados hasta hoy.")
        return

    # 3. Generar datos por cada día faltante
    data = []
    current_date = fecha_inicio
    
    while current_date <= fecha_hoy:
        # Generamos entre 20 y 50 líneas de venta por día para que parezca un restaurante real
        ventas_del_dia = random.randint(20, 50)
        
        for _ in range(ventas_del_dia):
            # FECHA (con el toque sucio ocasional)
            fecha_str = current_date.strftime('%Y-%m-%d') if random.random() > 0.05 else current_date.strftime('%d/%m/%Y')
            
            # TICKET (Agrupamos ventas por mesas)
            ticket_id = f"T-{random.randint(20000, 99999)}" 

            # TURNO (Sucio)
            turno_opciones = ["Comida", "Cena", "comida", "CENA", "  Cena  ", "NULL", "N/A"]
            turno = random.choice(turno_opciones) if random.random() > 0.05 else np.nan

            # ID_PLATO
            id_plato = "P-99" if random.random() > 0.98 else random.choice(platos_reales)

            # CANTIDAD
            if random.random() > 0.99:
                cantidad = -1 
            else:
                cantidad = random.randint(1, 4)

            data.append([ticket_id, fecha_str, turno, id_plato, cantidad])
        
        current_date += timedelta(days=1)

    # 4. Guardar resultados
    new_df = pd.DataFrame(data, columns=['id_ticket', 'fecha', 'turno', 'id_plato', 'cantidad'])
    
    if os.path.exists(PATH_OUTPUT):
        # Concatenamos con lo viejo
        df_old = pd.read_csv(PATH_OUTPUT)
        # Quitamos la columna temporal de fecha si se quedó guardada
        if 'fecha_dt' in df_old.columns: df_old = df_old.drop(columns=['fecha_dt'])
        
        df_final = pd.concat([df_old, new_df], ignore_index=True)
        df_final.to_csv(PATH_OUTPUT, index=False)
        print(f"✅ Se han añadido {len(new_df)} nuevas líneas de ventas.")
    else:
        new_df.to_csv(PATH_OUTPUT, index=False)
        print(f"✅ Archivo RAW creado con {len(new_df)} líneas.")

if __name__ == "__main__":
    generate_daily_dirty_data()