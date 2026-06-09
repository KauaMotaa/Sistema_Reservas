# Cenários de Teste

Os testes ficam em `test_main.py` (na raiz) e a configuração do banco de teste
fica em `conftest.py`. Rodam com `pytest -v`.

## Banco de teste (Postgres + fixtures + rollback)

- **Instância de teste Postgres:** os testes rodam num banco Postgres separado
  (não no banco de produção). A URL vem da variável `TEST_DATABASE_URL`.
- **Fixtures (`conftest.py`):** preparações reaproveitáveis que o pytest entrega
  pronto pra cada teste — uma sessão de banco (`db_session`) e um cliente de
  teste (`client`).
- **Rollback automático:** cada teste roda dentro de uma transação que é desfeita
  no final, então um teste nunca suja o banco do outro.

### Como rodar localmente
```bash
# com Postgres de teste (ajuste usuario/senha/porta/banco):
export TEST_DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"
pytest -v

# ou, para checagem rapida sem Postgres:
export TEST_DATABASE_URL="sqlite:///./teste_banco.db"
pytest -v
```

## Testes unitários da lógica de negócio (ImovelCore)

| Teste | O que verifica | Esperado |
|-------|----------------|----------|
| `test_validar_imovel_ok` | Imóvel válido passa na validação | True |
| `test_validar_imovel_poucos_comodos` | Imóvel com menos de 2 cômodos | erro (HTTPException) |
| `test_validar_imovel_area_pequena` | Imóvel com menos de 5 m² | erro (HTTPException) |
| `test_reservar_datas_validas` | Reserva com datas no futuro | True |
| `test_reservar_data_no_passado` | Reserva começando no passado | erro (HTTPException) |
| `test_reservar_data_final_invalida` | Data final antes da inicial | erro (HTTPException) |

## Testes de integração (rotas + banco)

| Teste | O que verifica | Esperado |
|-------|----------------|----------|
| `test_fluxo_completo_imovel` | Cadastra → busca → atualiza → confere → deleta → confere que sumiu | 200 em cada etapa; 404 no fim |
| `test_fluxo_reserva` | Cadastra um imóvel disponível e reserva | 200; fica "RESERVADO" e indisponível |

## Testes de cenários de erro (tratamento de falhas)

| Teste | O que verifica | Esperado |
|-------|----------------|----------|
| `test_buscar_imovel_inexistente` | Busca id que não existe | 404 |
| `test_cadastrar_dados_invalidos` | Cadastro com campos faltando | 422 |
| `test_cadastrar_quebrando_regra` | Cadastro de imóvel com 1 cômodo | 400 |
| `test_reservar_imovel_indisponivel` | Reservar um imóvel já reservado | 400 |

## Mock da API externa (ViaCEP)

A aplicação tem a rota `GET /imoveis/cep/{cep}`, que consulta a API externa
**ViaCEP** para descobrir o endereço a partir de um CEP. Nos testes, essa chamada
externa é **mockada** (fingida), para não depender da internet nem do serviço
estar no ar.

| Teste | O que verifica | Esperado |
|-------|----------------|----------|
| `test_consultar_cep_com_mock` | Finge uma resposta de sucesso da ViaCEP | 200 e o endereço esperado |
| `test_consultar_cep_inexistente` | Finge a ViaCEP dizendo que o CEP não existe | 404 |
| `test_consultar_cep_servico_fora_do_ar` | Finge a ViaCEP fora do ar (status 500) | 502 |

## Pipeline (CI)

O `.github/workflows/ci.yml` sobe um **Postgres de teste** e roda todos esses
testes automaticamente a cada `push`.
