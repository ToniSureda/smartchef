from database import get_connection
from entities.menu import DimMenuEntity

def get_all_menu():
    query = """
        SELECT id_plato, nombre_plato, categoria, precio_venta
        FROM dim_menu
    """

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)

    rows = cur.fetchall()
    conn.close()

    return [
        DimMenuEntity(
            id_plato=row[0],
            nombre_plato=row[1],
            categoria=row[2],
            precio_venta=float(row[3]) if row[3] else None
        )
        for row in rows
    ]