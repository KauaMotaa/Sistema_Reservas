# Sistema de Reservas (FastAPI)

API REST feita com FastAPI e SQLAlchemy para cadastrar, gerenciar e reservar imóveis.
Projeto da disciplina de Projeto de Testes e Teste/Qualidade de Software.

## Tecnologias
- Python
- FastAPI
- SQLAlchemy + PostgreSQL
- Pydantic (validação)
- pytest (testes)
- Docker / Docker Compose

## Estrutura do projeto

```
app/
  DataBaseConfig/          # modelos do banco (ImovelDB) e conexao 
  schemas_pydentic/        # validacao de entrada (Pydantic)
  core/                    # regras de negocio (ImovelCore)
  routers/                 # rotas/endpoints + integracao ViaCEP
  tests/                   # Modelos de Teste Pytests 
main.py                    # ponto de entrada da aplicacao
                 
```

## Como rodar com Docker (recomendado)

Crie um arquivo `.env` na raiz com as variáveis do banco:

```
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=imoveis
DB_PORT=5432
```

Depois suba tudo:

```bash
docker compose up --build
```

A API fica em `http://127.0.0.1:8000` e a documentação automática em
`http://127.0.0.1:8000/docs`.

## Endpoints

| Método | Rota                        | O que faz                          |
|--------|-----------------------------|------------------------------------|
| HEAD   | `/`                         | Health check (status da API)       |
| GET    | `/imoveis/size`             | Conta quantos imóveis existem      |
| GET    | `/imoveis/all`              | Lista todos os imóveis             |
| POST   | `/imoveis/`                 | Cadastra um imóvel                 |
| GET    | `/imoveis/{id}`             | Busca um imóvel pelo id            |
| PUT    | `/imoveis/{id}`             | Atualiza um imóvel                 |
| PUT    | `/imoveis/reserve/{id}`     | Reserva um imóvel                  |
| DELETE | `/imoveis/{id}`             | Apaga um imóvel                    |
| GET    | `/imoveis/cep/{cep}`        | Consulta endereço por CEP (ViaCEP) |

## Como rodar os testes

Os testes usam um banco de teste separado (via `TEST_DATABASE_URL`), com fixtures
do pytest e rollback automático.

```bash
# com Postgres de teste:
export TEST_DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"
pytest -v

# ou, para checagem rapida sem Postgres:
export TEST_DATABASE_URL="sqlite:///./teste_banco.db"
pytest -v
```

Veja `TESTES.md` para a descrição de cada cenário testado.
