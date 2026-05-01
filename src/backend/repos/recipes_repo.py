from database import get_connection
from entities.recipes import DimRecipesEntity

def get_recipes_by_plato(id_plato):
    """ Extraccion del escandallo detallado filtrando por identificador de plato """
    query = """
        SELECT id_recipe, id_plato, ingrediente, cantidad, unidad, coste_unitario_kg
        FROM dim_recipes
        WHERE id_plato = %s
    """

    # Apertura de conexion y ejecucion de consulta parametrizada
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (id_plato,))
    rows = cur.fetchall()
    
    # Cierre de sesion y liberacion de recursos del gestor de base de datos
    conn.close()

    # Mapeo de resultados relacionales hacia entidades de dominio estructuradas
    return [
        DimRecipesEntity(
            id_recipe=row[0],
            id_plato=row[1],
            ingrediente=row[2],
            cantidad=float(row[3]) if row[3] else None,
            unidad=row[4],
            coste_unitario_kg=float(row[5]) if row[5] else None
        )
        for row in rows
    ]