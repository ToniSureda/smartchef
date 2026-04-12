from dataclasses import dataclass
from datetime import date

@dataclass
class DimContextEntity:
    date: date
    is_holiday: int          
    es_vispera: int          
    day_of_week: str
    temp_max: float | None
    precipitation: float | None