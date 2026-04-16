from database import get_connection
from entities.predictions import FactPredictionsEntity

def get_predictions_by_date(fecha):
    """ Extraccion de inferencias predictivas filtradas por horizonte temporal """
    query = """
        SELECT id_prediction, fecha_prediccion, id_plato, cantidad_predicha, intervalo_confianza
        FROM fact_predictions
        WHERE fecha_prediccion = %s
    """

    # Apertura de conexion y ejecucion de consulta parametrizada
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (fecha,))
    rows = cur.fetchall()
    
    # Cierre de sesion y liberacion de recursos del gestor de base de datos
    conn.close()

    # Mapeo de resultados relacionales hacia entidades de dominio estructuradas
    return [
        FactPredictionsEntity(
            id_prediction=row[0],
            fecha_prediccion=row[1],
            id_plato=row[2],
            cantidad_predicha=float(row[3]) if row[3] else None,
            intervalo_confianza=row[4]
        )
        for row in rows
    ]