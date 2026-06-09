from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.DataBaseConfig.database import get_db
from app.DataBaseConfig.imovel_db import ImovelDB
from app.schemas_pydentic.schemas_pydentic import ImovelModel , ReservaModel
from app.core.core import ImovelCore

router = APIRouter(prefix="/imoveis", tags=["Imóveis"])



# Consulta o endereco de um CEP usando a API externa ViaCEP funcao fica para o proximo envio 
# Seguindo a adicao de mais de uma tabela para entrada dos dados de endereco bencomo a adequacao
# do endereco como outro campo json

@router.get("/cep/{cep}")
def consultar_cep(cep: str):
    endereco = ImovelCore.buscar_cep(cep)
    return {
        "cep": endereco.get("cep"),
        "rua": endereco.get("logradouro"),
        "bairro": endereco.get("bairro"),
        "cidade": endereco.get("localidade"),
        "estado": endereco.get("uf"),
    }


# Opcional (remover apos Deploy)
@router.get("/size")
def read_root(db: Session = Depends(get_db)):
    size = db.scalar(select(func.count()).select_from(ImovelDB))
    return {"O valor de itens cadastrados e" : size}


# retorna uma lista com todos os imoveis cadastrados
@router.get("/all")
def list_item(db: Session = Depends(get_db)):
    return db.query(ImovelDB).all()


# retorna o Imovel com o Id referente
@router.get("/{imovel_id}")
def read_item(imovel_id: int, db: Session = Depends(get_db)):
    imovel = db.get(ImovelDB, imovel_id)
    if not imovel:
        raise HTTPException(status_code=404, detail="ID de imovel inexistente")
    return imovel


# Atualiza o imovel com o id referente
@router.put("/{imovel_id}")
def updat_item(imovel_id: int , imovel_dados:ImovelModel , db: Session = Depends(get_db)):
    imovel = db.get(ImovelDB, imovel_id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Id Invalido")

    # Valida o Imovel antes de Salvar
    ImovelCore.ValidarImovel(imovel_dados)

    imovel.name = imovel_dados.name
    imovel.Tipo = imovel_dados.Tipo
    imovel.Endereco = imovel_dados.Endereco
    imovel.Metros2 = imovel_dados.Metros2
    imovel.Comodos = imovel_dados.Comodos
    imovel.Area_De_lazer = imovel_dados.Area_De_lazer
    imovel.Situacao = imovel_dados.Situacao
    imovel.Disponibilidade_de_reserva = imovel_dados.Disponibilidade_de_reserva

    db.commit()
    db.refresh(imovel)
    return {"o Item": imovel_id ,
            "foi Atualizado para": imovel_dados}


# reservar um imovel
@router.put("/reserve/{imovel_id}")
def reservar_Imovel(imovel_id: int ,imovel_dados:ReservaModel , db: Session = Depends(get_db)):
    imovel = db.get(ImovelDB, imovel_id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Id Invalido")

    # se o imovel ja esta reservado/indisponivel, nao deixa reservar de novo
    if not imovel.Disponibilidade_de_reserva:
        raise HTTPException(status_code=400, detail="Imovel indisponivel para reserva")

    # valida as datas da reserva
    ImovelCore.reservarImovel(imovel_dados)

    imovel.Situacao = "RESERVADO"
    imovel.Disponibilidade_de_reserva = False
    imovel.Data_Inicial_reserva = imovel_dados.Data_Inicial_reserva
    imovel.Data_Final_reserva = imovel_dados.Data_Final_reserva
    db.commit()
    db.refresh(imovel)

    return {"o Item": imovel_id ,
            "foi reservado para": imovel_dados}


# Cadastro de novo Imovel
@router.post("/")
def new_item(imovel_request: ImovelModel, db: Session = Depends(get_db)):
    # valida as regras de negocio antes de cadastrar
    ImovelCore.ValidarImovel(imovel_request)

    novo_Imovel = ImovelDB(**imovel_request.model_dump())
    db.add(novo_Imovel)
    db.commit()
    db.refresh(novo_Imovel)
    return {
            "mensagem": "Imóvel cadastrado com sucesso",
            "dados": novo_Imovel
    }


@router.delete("/{imovel_id}")
def delete_item(imovel_id: int , db: Session = Depends(get_db)):
    imovel = db.get(ImovelDB, imovel_id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Id Invalido")
    db.delete(imovel)
    db.commit()
    return {"Imovel Deletado" : imovel_id}
