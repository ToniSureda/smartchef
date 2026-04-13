from dataclasses import dataclass
from datetime import date

@dataclass
class FactSalesEntity:
    id_ticket: str
    fecha: date | None
    turno: str | None
    id_plato: str
    cantidad: int | None