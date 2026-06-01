# API de Imóveis (FastAPI)

API REST feita com FastAPI e SQLAlchemy para cadastrar e gerenciar imóveis.
Projeto da disciplina de Projeto de Testes e Teste/Qualidade de Software.

## Tecnologias
- Python
- FastAPI
- SQLAlchemy + SQLite
- Pydantic (validação)
- pytest (testes)

## Como instalar

```bash
pip install -r requirements.txt
```

## Como rodar a aplicação

```bash
uvicorn main:app --reload
```

Depois é só abrir a documentação automática no navegador:
`http://127.0.0.1:8000/docs`

## Endpoints

| Método | Rota                          | O que faz                       |
|--------|-------------------------------|---------------------------------|
| GET    | `/`                           | Conta quantos imóveis existem   |
| GET    | `/Newimoveis/`                | Lista todos os imóveis          |
| POST   | `/Newimoveis/`                | Cadastra um imóvel              |
| GET    | `/imoveis/{id}`               | Busca um imóvel pelo id         |
| PUT    | `/imoveis/{id}`               | Atualiza um imóvel              |
| PUT    | `/imoveis/{id}/status`        | Atualiza só a situação/venda    |
| DELETE | `/imoveis/{id}/delete`        | Apaga um imóvel                 |

## Como rodar os testes

```bash
pytest -v
```

Os testes usam o `TestClient` do FastAPI e um banco separado (`teste_banco.db`),
então não precisam do servidor ligado nem mexem no banco de verdade.
