from database import get_connection
from entities.sales import FactSalesEntity

def get_sales_by_date(fecha):
    """ Extraccion de registros de ventas filtrados por fecha especifica """
    query = """
        SELECT id_ticket, fecha, turno, id_plato, cantidad
        FROM fact_sales
        WHERE fecha = %s
    """

    # Apertura de conexion y ejecucion de consulta parametrizada
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (fecha,))
    rows = cur.fetchall()
    
    # Liberacion de recursos tras la obtencion del conjunto de resultados
    conn.close()

    # Transformacion de registros crudos a objetos de dominio estructurados
    return [
        FactSalesEntity(
            id_ticket=row[0],
            fecha=row[1],
            turno=row[2],
            id_plato=row[3],
            cantidad=row[4]
        )
        for row in rows
    ]