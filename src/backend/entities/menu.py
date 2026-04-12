from dataclasses import dataclass

@dataclass
class DimMenuEntity:
    id_plato: str
    nombre_plato: str | None
    categoria: str | None
    precio_venta: float | None