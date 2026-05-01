import pandas as pd
import os
import sys

# Configuracion de la variable de entorno PATH para permitir la importacion de modulos raiz
ruta_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_padre not in sys.path:
    sys.path.append(ruta_padre)

# Inicializacion del controlador de base de datos
try:
    from database import get_connection
    print("Conexion con el modulo de persistencia establecida exitosamente.")
except ImportError:
    print("Error de importacion: Modulo database no encontrado. Verifique la estructura de directorios del proyecto.")
    sys.exit(1)

# Definicion de la ruta absoluta para la ingesta del modelo de machine learning
CSV_PATH = "/app/backend/exports/predictions/fact_predictions_ml.csv"

if not os.path.exists(CSV_PATH):
    print(f"Error critico: Archivo de predicciones no localizado en la ruta esperada: {CSV_PATH}")
    sys.exit(1)

# Lectura y tipado del dataset de predicciones
df = pd.read_csv(CSV_PATH, parse_dates=["fecha_prediccion"])
print(f"Total de registros cargados en memoria temporal: {len(df)}")

# Apertura de conexion y ejecucion de bloque transaccional
try:
    conn = get_connection()
    cur = conn.cursor()

    # Sentencia DML con instruccion de resolucion de conflictos para garantizar idempotencia
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
    print("Operacion completada. Lote de predicciones persistido correctamente en la base de datos.")

except Exception as e:
    print(f"Fallo durante la transaccion de insercion de datos: {e}")