from database import get_connection
from entities.menu import DimMenuEntity

def get_all_menu():
    """ Extraccion del catalogo completo de platos disponibles en el sistema """
    query = """
        SELECT id_plato, nombre_plato, categoria, precio_venta
        FROM dim_menu
    """

    # Apertura de conexion y ejecucion de la consulta de lectura
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)

    # Recuperacion de registros y liberacion del gestor de base de datos
    rows = cur.fetchall()
    conn.close()

    # Mapeo de resultados relacionales a lista de entidades de dominio
    return [
        DimMenuEntity(
            id_plato=row[0],
            nombre_plato=row[1],
            categoria=row[2],
            precio_venta=float(row[3]) if row[3] else None
        )
        for row in rows
    ]