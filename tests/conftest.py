
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.DataBaseConfig.database import Base, get_db



TEST_DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@db_test:5432/test_db'

# O connect_args so e necessario para SQLite; no Postgres fica vazio
connect_args = {"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {}
engine_teste = create_engine(TEST_DATABASE_URL, connect_args=connect_args)
SessionTeste = sessionmaker(autocommit=False, autoflush=False, bind=engine_teste)


@pytest.fixture(scope="session", autouse=True)
def preparar_banco():
    Base.metadata.create_all(bind=engine_teste)
    yield
    Base.metadata.drop_all(bind=engine_teste)



@pytest.fixture
def db_session():
    conexao = engine_teste.connect()
    transacao = conexao.begin()
    sessao = SessionTeste(bind=conexao, join_transaction_mode="create_savepoint")
    try:
        yield sessao
    finally:
        sessao.close()
        transacao.rollback()
        conexao.close()


@pytest.fixture
def client(db_session):
    def get_db_teste():
        yield db_session

    app.dependency_overrides[get_db] = get_db_teste
    yield TestClient(app)
    app.dependency_overrides.clear()