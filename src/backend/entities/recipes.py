from dataclasses import dataclass

# Definicion de la entidad de dominio para detallar la composicion de recetas y escandallos
@dataclass
class DimRecipesEntity:
    id_recipe: int
    id_plato: str | None
    ingrediente: str | None
    cantidad: float | None
    unidad: str | None
    coste_unitario_kg: float | None