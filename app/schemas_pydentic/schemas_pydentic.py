from datetime import date
from pydantic import BaseModel


class ImovelModel(BaseModel):
    name: str
    Tipo: str
    Endereco : str
    Metros2: float
    Comodos: int
    Area_De_lazer: bool | None = None
    Situacao: str
    Disponibilidade_de_reserva: bool| None = None
    Data_Inicial_reserva: date | None = None
    Data_Final_reserva: date | None = None

class ReservaModel(BaseModel):
    Situacao: str
    Data_Inicial_reserva: date | None = None
    Data_Final_reserva: date | None = None
