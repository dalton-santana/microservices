import requests
import json
from time import sleep

VOOS = "/home/dalton/Área de Trabalho/Trabalho pos/microservices/lsita-voos/voos.json"

URL_VOOS = "http://172.28.1.1:5000/gravar/"

def enviar(url, json_noticias):
    arquivo = open(json_noticias, "r")
    dados = json.load(arquivo)
    arquivo.close()

    resposta = "nenhuma voo para enviar"
    if dados:
        resposta = requests.post(url, json=json.dumps(dados))
        if resposta.ok:
            resposta = "voos enviadas"
        else:
            resposta = "erro de envio: " + resposta.text

    return resposta


if __name__ == "__main__":
    resposta = enviar(URL_VOOS, VOOS)
    print(resposta, "[VOOS]")

    sleep(10)