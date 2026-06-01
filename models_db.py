from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class ImovelDB(Base):
    __tablename__ = "imoveis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String , index=True)
    Tipo= Column(String)
    Metros2= Column(Float)
    Comodos= Column(Integer)
    Area_De_lazer=Column (Boolean)
    Situacao=Column(String)
    Disponibilidade_de_venda=Column(Boolean)