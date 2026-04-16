from dataclasses import dataclass
from datetime import date

# Definicion de la entidad de dominio para estructurar los resultados del modelo predictivo
@dataclass
class FactPredictionsEntity:
    id_prediction: int
    fecha_prediccion: date | None
    id_plato: str | None
    cantidad_predicha: float | None
    intervalo_confianza: str | None