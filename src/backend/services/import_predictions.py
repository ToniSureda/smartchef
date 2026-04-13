
import pandas as pd
import psycopg2
import os
from database import get_connection

## Ruta al CSV

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CSV_PATH = os.path.join(
    BASE_DIR,
    "exports",
    "predictions",
    "fact_predictions_ml.csv"
)

## Leer CSV


df = pd.read_csv(
    CSV_PATH,
    parse_dates=["fecha_prediccion"]
)

print(f"Filas leídas del CSV: {len(df)}")

## Conexion a SQL

conn = get_connection()
cur = conn.cursor()

## Insert SQL

insert_sql = """
INSERT INTO fact_predictions (
    id_prediction,
    fecha_prediccion,
    id_plato,
    cantidad_predicha,
    intervalo_confianza
)
VALUES (%s, %s, %s, %s, %s)
"""

## insercion

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

print("Predicciones insertadas correctamente en fact_predictions")






