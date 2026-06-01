
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db


URL_TESTE = "sqlite:///./teste_banco.db"

engine_teste = create_engine(
    URL_TESTE, connect_args={"check_same_thread": False}
)
SessionTeste = sessionmaker(autocommit=False, autoflush=False, bind=engine_teste)

Base.metadata.create_all(bind=engine_teste)


def get_db_teste():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_db_teste

client = TestClient(app)



dados_imovel = {
    "name": "casa",
    "Tipo": "quarto",
    "Metros2": 10,
    "Comodos": 20,
    "Area_De_lazer": True,
    "Situacao": "disponivel",
    "Disponibilidade_de_venda": True
}


def test_rota_raiz_responde():
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "O valor de itens cadastrados e" in resposta.json()


def test_cadastrar_imovel():
    resposta = client.post("/Newimoveis/", json=dados_imovel)
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Imóvel cadastrado com sucesso"


def test_validacao_dados_invalidos():
    dados_errados = {
        "name": "casa"
    }
    resposta = client.post("/Newimoveis/", json=dados_errados)
    assert resposta.status_code == 422
