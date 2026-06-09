from datetime import date, timedelta
from unittest.mock import patch, MagicMock

import pytest
from fastapi import HTTPException

from app.core.core import ImovelCore
from app.schemas_pydentic.schemas_pydentic import ImovelModel, ReservaModel


# Imovel de exemplo valido (>= 2 comodos, >= 5 metros, campos preenchidos)
dados_imovel = {
    "name": "casa",
    "Tipo": "apartamento",
    "Endereco": "Rua A, 123",
    "Metros2": 50,
    "Comodos": 3,
    "Area_De_lazer": True,
    "Situacao": "disponivel",
    "Disponibilidade_de_reserva": True,
}


# Ajuda a montar um ImovelModel valido, trocando so o que a gente quiser
def imovel_valido(**mudancas):
    base = dict(
        name="casa", Tipo="apto", Endereco="Rua A",
        Metros2=50, Comodos=3, Situacao="disponivel",
    )
    base.update(mudancas)
    return ImovelModel(**base)


# =====================================================================
# TESTES UNITARIOS DA LOGICA DE NEGOCIO (ImovelCore) - sem banco, sem rede
# =====================================================================

def test_validar_imovel_ok():
    assert ImovelCore.ValidarImovel(imovel_valido()) is True

def test_validar_imovel_poucos_comodos():
    with pytest.raises(HTTPException):
        ImovelCore.ValidarImovel(imovel_valido(Comodos=1))

def test_validar_imovel_area_pequena():
    with pytest.raises(HTTPException):
        ImovelCore.ValidarImovel(imovel_valido(Metros2=3))

def test_reservar_datas_validas():
    hoje = date.today()
    reserva = ReservaModel(
        Situacao="disponivel",
        Data_Inicial_reserva=hoje + timedelta(days=1),
        Data_Final_reserva=hoje + timedelta(days=5),
    )
    assert ImovelCore.reservarImovel(reserva) is True

def test_reservar_data_no_passado():
    hoje = date.today()
    reserva = ReservaModel(
        Situacao="disponivel",
        Data_Inicial_reserva=hoje - timedelta(days=1),
        Data_Final_reserva=hoje + timedelta(days=5),
    )
    with pytest.raises(HTTPException):
        ImovelCore.reservarImovel(reserva)

def test_reservar_data_final_invalida():
    hoje = date.today()
    reserva = ReservaModel(
        Situacao="disponivel",
        Data_Inicial_reserva=hoje + timedelta(days=5),
        Data_Final_reserva=hoje + timedelta(days=1),
    )
    with pytest.raises(HTTPException):
        ImovelCore.reservarImovel(reserva)


# =====================================================================
# TESTES DE INTEGRACAO (rotas + banco juntos) - usam a fixture 'client'
# =====================================================================

def test_fluxo_completo_imovel(client):
    criar = client.post("/imoveis/", json=dados_imovel)
    assert criar.status_code == 200
    novo_id = criar.json()["dados"]["id"]

    buscar = client.get(f"/imoveis/{novo_id}")
    assert buscar.status_code == 200
    assert buscar.json()["name"] == "casa"

    dados_novos = dict(dados_imovel)
    dados_novos["name"] = "casa atualizada"
    atualizar = client.put(f"/imoveis/{novo_id}", json=dados_novos)
    assert atualizar.status_code == 200

    conferir = client.get(f"/imoveis/{novo_id}")
    assert conferir.json()["name"] == "casa atualizada"

    deletar = client.delete(f"/imoveis/{novo_id}")
    assert deletar.status_code == 200

    sumiu = client.get(f"/imoveis/{novo_id}")
    assert sumiu.status_code == 404


def test_fluxo_reserva(client):
    criar = client.post("/imoveis/", json=dados_imovel)
    novo_id = criar.json()["dados"]["id"]

    hoje = date.today()
    reserva = {
        "Situacao": "disponivel",
        "Data_Inicial_reserva": str(hoje + timedelta(days=1)),
        "Data_Final_reserva": str(hoje + timedelta(days=5)),
    }
    reservar = client.put(f"/imoveis/reserve/{novo_id}", json=reserva)
    assert reservar.status_code == 200

    buscar = client.get(f"/imoveis/{novo_id}")
    assert buscar.json()["Situacao"] == "RESERVADO"
    assert buscar.json()["Disponibilidade_de_reserva"] is False


# =====================================================================
# TESTES DE CENARIOS DE ERRO (tratamento de falhas) - usam a fixture 'client'
# =====================================================================

def test_buscar_imovel_inexistente(client):
    resposta = client.get("/imoveis/999999")
    assert resposta.status_code == 404

def test_cadastrar_dados_invalidos(client):
    resposta = client.post("/imoveis/", json={"name": "casa"})
    assert resposta.status_code == 422

def test_cadastrar_quebrando_regra(client):
    dados_ruins = dict(dados_imovel)
    dados_ruins["Comodos"] = 1
    resposta = client.post("/imoveis/", json=dados_ruins)
    assert resposta.status_code == 400

def test_reservar_imovel_indisponivel(client):
    criar = client.post("/imoveis/", json=dados_imovel)
    novo_id = criar.json()["dados"]["id"]

    hoje = date.today()
    reserva = {
        "Situacao": "disponivel",
        "Data_Inicial_reserva": str(hoje + timedelta(days=1)),
        "Data_Final_reserva": str(hoje + timedelta(days=5)),
    }
    client.put(f"/imoveis/reserve/{novo_id}", json=reserva)
    de_novo = client.put(f"/imoveis/reserve/{novo_id}", json=reserva)
    assert de_novo.status_code == 400


# =====================================================================
# MOCK DA API EXTERNA (ViaCEP)
# "Fingimos" a resposta da ViaCEP para o teste nao depender da internet.
# =====================================================================

# Mock de sucesso: a ViaCEP devolve um endereco
def test_consultar_cep_com_mock(client):
    resposta_falsa = MagicMock()
    resposta_falsa.status_code = 200
    resposta_falsa.json.return_value = {
        "cep": "01001-000",
        "logradouro": "Praca da Se",
        "bairro": "Se",
        "localidade": "Sao Paulo",
        "uf": "SP",
    }
    with patch("app.core.core.requests.get", return_value=resposta_falsa):
        resposta = client.get("/imoveis/cep/01001000")
    assert resposta.status_code == 200
    assert resposta.json()["cidade"] == "Sao Paulo"


# Mock de erro: a ViaCEP diz que o CEP nao existe -> esperamos 404
def test_consultar_cep_inexistente(client):
    resposta_falsa = MagicMock()
    resposta_falsa.status_code = 200
    resposta_falsa.json.return_value = {"erro": True}
    with patch("app.core.core.requests.get", return_value=resposta_falsa):
        resposta = client.get("/imoveis/cep/00000000")
    assert resposta.status_code == 404


# Mock de falha: a ViaCEP esta fora do ar (status 500) -> esperamos 502
def test_consultar_cep_servico_fora_do_ar(client):
    resposta_falsa = MagicMock()
    resposta_falsa.status_code = 500
    with patch("app.core.core.requests.get", return_value=resposta_falsa):
        resposta = client.get("/imoveis/cep/01001000")
    assert resposta.status_code == 502
