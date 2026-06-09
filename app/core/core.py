from fastapi import HTTPException, status
from app.schemas_pydentic.schemas_pydentic import ImovelModel, ReservaModel
from datetime import date
import requests
URL_VIACEP = "https://viacep.com.br/ws"

class ImovelCore:

    @staticmethod
    def ValidarImovel(dados: ImovelModel):
        # Regra: o imovel precisa ter no minimo 2 comodos
        if dados.Comodos < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Imovel deve ter no minimo 2 comodos."
            )
        # Regra: o imovel precisa ter no minimo 5 metros quadrados
        if dados.Metros2 < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Imovel deve ter no minimo 5 metros quadrados."
            )
        # Regra: campos obrigatorios nao podem vir vazios
        if not dados.name or not dados.Tipo or not dados.Endereco or not dados.Situacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campos obrigatorios estao vazios."
            )
        return True

    @staticmethod
    def reservarImovel(dados: ReservaModel):
        # Regra: a reserva precisa ter data de inicio e fim
        if dados.Data_Inicial_reserva is None or dados.Data_Final_reserva is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A reserva precisa de data inicial e final."
            )
        # Regra: nao da pra reservar comecando no passado
        if dados.Data_Inicial_reserva < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data inicial nao pode estar no passado."
            )
        # Regra: a data final tem que ser depois da inicial
        if dados.Data_Final_reserva < dados.Data_Inicial_reserva:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data final deve ser depois da data inicial."
            )
        return True

    
    @staticmethod
    def buscar_cep(cep: str):
        
        resposta = requests.get(f"{URL_VIACEP}/{cep}/json/")

        if resposta.status_code != 200:
            raise HTTPException(status_code=502, detail="Servico de CEP indisponivel")

        dados = resposta.json()

        if dados.get("erro"):
            raise HTTPException(status_code=404, detail="CEP nao encontrado")

        return dados