from dataclasses import dataclass

@dataclass
class DimRecipesEntity:
    id_recipe: int
    id_plato: str | None
    ingrediente: str | None
    cantidad: float | None
    unidad: str | None
    coste_unitario_kg: float | None