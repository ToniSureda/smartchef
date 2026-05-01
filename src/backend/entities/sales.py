from dataclasses import dataclass
from datetime import date

# Definicion de la entidad de dominio para estructurar los registros transaccionales de ventas
@dataclass
class FactSalesEntity:
    id_ticket: str
    fecha: date | None
    turno: str | None
    id_plato: str
    cantidad: int | None