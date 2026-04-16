import pandas as pd
import psycopg2
import os
import sys

# 1. PRIMERO preparamos el camino (esto debe ir antes de importar database)
ruta_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_padre not in sys.path:
    sys.path.append(ruta_padre)

# 2. AHORA ya podemos importar database
try:
    from database import get_connection
    print("✅ Conexión con database.py establecida")
except ImportError:
    print("❌ Error: Todavía no encuentro database.py. Revisa la estructura de carpetas.")
    sys.exit(1)

# 3. Ruta absoluta al CSV
CSV_PATH = "/app/backend/exports/predictions/fact_predictions_ml.csv"

if not os.path.exists(CSV_PATH):
    print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
    sys.exit(1)

## Leer CSV
df = pd.read_csv(CSV_PATH, parse_dates=["fecha_prediccion"])
print(f"📊 Filas leídas del CSV: {len(df)}")

## Conexion a SQL e Inserción
try:
    conn = get_connection()
    cur = conn.cursor()

    # Usamos ON CONFLICT para que no te de error si lo lanzas varias veces
    insert_sql = """
    INSERT INTO fact_predictions (
        id_prediction, fecha_prediccion, id_plato, cantidad_predicha, intervalo_confianza
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id_prediction) DO UPDATE SET
        cantidad_predicha = EXCLUDED.cantidad_predicha,
        intervalo_confianza = EXCLUDED.intervalo_confianza;
    """

    for _, row in df.iterrows():
        cur.execute(
            insert_sql,
            (
                int(row["id_prediction"]),
                row["fecha_prediccion"],
                row["id_plato"],
                float(row["cantidad_predicha"]),
                row["intervalo_confianza"]
            )
        )

    conn.commit()
    cur.close()
    conn.close()
    print("🚀 ¡ÉXITO! Predicciones insertadas en la base de datos.")

except Exception as e:
    print(f"❌ Error en la base de datos: {e}")