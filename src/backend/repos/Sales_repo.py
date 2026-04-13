from database import get_connection
from entities.sales import FactSalesEntity

def get_sales_by_date(fecha):
    query = """
        SELECT id_ticket, fecha, turno, id_plato, cantidad
        FROM fact_sales
        WHERE fecha = %s
    """

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (fecha,))
    rows = cur.fetchall()
    conn.close()

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