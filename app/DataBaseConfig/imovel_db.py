from sqlalchemy import Column, Integer, String, Float, Boolean , Date
from app.DataBaseConfig.database import Base

class ImovelDB(Base):
    __tablename__ = "imoveis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String , index=True)
    Tipo= Column(String)
    Endereco= Column(String) #Ira se tornar um json na proxima atualizacao
    Metros2= Column(Float)
    Comodos= Column(Integer)
    Area_De_lazer=Column (Boolean)
    Situacao=Column(String)
    Disponibilidade_de_reserva=Column(Boolean)
    Data_Inicial_reserva=Column(Date)
    Data_Final_reserva=Column(Date)
