import requests
import json
from time import sleep

NOTICIAS_JOGATINA = "/misc/ifba/workspaces/orientacao a servicos/version4/noticias/VOOS.json"
NOTICIAS_SISTEMAS = "/misc/ifba/workspaces/orientacao a servicos/version4/noticias/sistemas.json"

URL_JOGATINA = "http://172.28.1.1:5000/gravar/"
URL_SISTEMAS = "http://172.28.1.2:5000/gravar/"

def enviar(url, json_noticias):
    arquivo = open(json_noticias, "r")
    dados = json.load(arquivo)
    arquivo.close()

    resposta = "nenhuma notícias para enviar"
    if dados:
        resposta = requests.post(url, json=json.dumps(dados))
        if resposta.ok:
            resposta = "notícias enviadas"
        else:
            resposta = "erro de envio: " + resposta.text

    return resposta


if __name__ == "__main__":
    while True:
        resposta = enviar(URL_JOGATINA, NOTICIAS_JOGATINA)
        print(resposta, "[VOOS]")

        resposta = enviar(URL_SISTEMAS, NOTICIAS_SISTEMAS)
        print(resposta, "[SISTEMAS]")

        sleep(10)