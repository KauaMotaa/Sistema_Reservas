from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from sqlalchemy import func , select
from pydantic import BaseModel
from models_db import Base , ImovelDB
from database import engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI()




class ImovelModel(BaseModel):
    name: str
    Tipo: str
    Metros2: float
    Comodos: int
    Area_De_lazer: bool | None = None
    Situacao: str
    Disponibilidade_de_venda: bool| None = None

class StatusImovelModel(BaseModel):
    Situacao: str
    Disponibilidade_de_venda: bool


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    size = db.scalar(select(func.count()).select_from(ImovelDB))
    
    return {"O valor de itens cadastrados e" : size}


@app.get("/imoveis/{imovel_id}")
def read_item(imovel_id: int, db: Session = Depends(get_db)):
    imovel = db.query(ImovelDB).get(imovel_id)
    if not imovel:
        return {"Erro" : "ID de imovel inexistente"}
    return imovel


@app.put("/imoveis/{imovel_id}")
def updat_item(imovel_id: int , imovel_dados:ImovelModel , db: Session = Depends(get_db)):
    
    imovel = db.get(ImovelDB, imovel_id)
    if not imovel: 
        return {"Erro": "Id Invalido"}
    
    imovel.name = imovel_dados.name
    imovel.Tipo = imovel_dados.Tipo
    imovel.Metros2 = imovel_dados.Metros2
    imovel.Comodos = imovel_dados.Comodos
    imovel.Area_De_lazer = imovel_dados.Area_De_lazer
    imovel.Situacao = imovel_dados.Situacao
    imovel.Disponibilidade_de_venda = imovel_dados.Disponibilidade_de_venda
    
    db.commit()
    db.refresh(imovel)
    return {"o Item": imovel_id , 
            "foi Atualizado para": imovel_dados}

@app.put("/imoveis/{imovel_id}/status")
def alter_status(imovel_id: int , imovel_dados:StatusImovelModel , db: Session = Depends(get_db)):
    imovel = db.get(ImovelDB, imovel_id)
    if not imovel: 
        return {"Erro": "Id Invalido"}
    
    imovel.Situacao = imovel_dados.Situacao
    imovel.Disponibilidade_de_venda = imovel_dados.Disponibilidade_de_venda
    db.commit()
    db.refresh(imovel)
    return {"o status": imovel_id , 
            "foi Atualizado para": imovel}

@app.delete("/imoveis/{imovel_id}/delete")
def delete_item(imovel_id: int , db: Session = Depends(get_db)):
    imovel = db.get(ImovelDB, imovel_id)
    if not imovel: 
        return {"Erro": "Id Invalido"}
    db.delete(imovel)
    db.commit()
    return {"Imovel Deletado" : imovel_id}


@app.get("/Newimoveis/")
def get_item(db: Session = Depends(get_db)):
    return db.query(ImovelDB).all() 


@app.post("/Newimoveis/")
def new_item(imovel_request: ImovelModel, db: Session = Depends(get_db)):
   novo_Imovel = ImovelDB(**imovel_request.model_dump())
   db.add(novo_Imovel)
   db.commit()
   db.refresh(novo_Imovel)
   return {
        "mensagem": "Imóvel cadastrado com sucesso", 
        "dados": novo_Imovel
    }

