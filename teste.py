import requests
import json

link_Imoveis = "http://127.0.0.1:8000/imoveis/"
link_size = "http://127.0.0.1:8000/"
link_post = "http://127.0.0.1:8000/Newimoveis/"
imovel_id = 9
link_put= f"{link_Imoveis}{imovel_id}"
Var_status = f"{link_Imoveis}{imovel_id}/{"status"}"

dados = {
    "name": "string",
    "Tipo": "string",
    "Metros2": 0,
    "Comodos": 0,
    "Area_De_lazer": True,
    "Situacao": "string",
    "Disponibilidade_de_venda": True
  }

dados2 = {
    "name": "casa",
    "Tipo": "quato",
    "Metros2": 10,
    "Comodos": 20,
    "Area_De_lazer": True,
    "Situacao": "string",
    "Disponibilidade_de_venda": True
  }

dados3 = {
    "Situacao": "ocupado",
    "Disponibilidade_de_venda": True
  }


resposta = requests.post(link_post, json=dados)
atualizar = requests.put(link_put ,json=dados2)
reservar = requests.put(Var_status ,json=dados3)
resoista2 = requests.get(link_size)

size_int = json.loads(resoista2.text)

print (resposta.text)
print()
print(resoista2.text)
print()
print(atualizar.text)
print()
print(reservar.text)


imovel_id = 0 
while size_int["O valor de itens cadastrados e"] != 0:

    link_delet = f"{link_Imoveis}{imovel_id}{"/delete"}"  
    resoista2 = requests.delete(link_delet)
    print(resoista2.text)
    imovel_id += 1
    
    if imovel_id >= size_int["O valor de itens cadastrados e"]: 
        break