from dataclasses import dataclass

# Definicion de la entidad de dominio para la representacion del catalogo de productos
@dataclass
class DimMenuEntity:
    id_plato: str
    nombre_plato: str | None
    categoria: str | None
    precio_venta: float | None