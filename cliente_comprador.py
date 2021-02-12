import urllib.request
import json
import time
import requests

# rotas do servico de voos (voos)
VOOS_URL_SERVICO = "http://172.28.1.1:5000/"
COMPRA_DE_PASSAGEM_URL_SERVICO = "http://172.28.1.2:5000/"

VOOS_IS_ALIVE = VOOS_URL_SERVICO + "isalive/"
COMPRA_DE_PASSAGEM_IS_ALIVE = COMPRA_DE_PASSAGEM_URL_SERVICO + "isalive/"

VOOS = VOOS_URL_SERVICO + "voos/"
COMPRA_DE_PASSAGEM = COMPRA_DE_PASSAGEM_URL_SERVICO + "compra/"

def acessar(url):
    print("\n")
    print("acessando a url:", url)

    response = urllib.request.urlopen(url)
    data = response.read()

    return data.decode("utf-8")


def voos_is_alive():
    alive = False

    if acessar(VOOS_IS_ALIVE) == "yes":
        alive = True

    return alive

def buscar_voos():
    data = acessar(VOOS)
    data = json.loads(data)

    return data["voos"]

def comprar_passagem(url, voo):
    resposta = requests.post(url, json=json.dumps(voo))
    if resposta.ok:
        print("Passagem comprada")
        print(resposta.content.decode("utf-8"))
    else:
        print(resposta.content.decode("utf-8"))

if __name__ == "__main__":
    while True:
        # verificar se o servico de voos estah ativo
        if voos_is_alive():
            # se estiver ativo
            print("\n\n")

            print("###############################################################")
            print("#################### NOVA COMPRA DE PASSAGEM ########################")
            print("###############################################################")

            # buscar os voos disponíveis
            print("serviço de voos está ativo. Solicitando voos...")
            voos = buscar_voos()

            # escolhe um voo
            voo_escolhido = voos[0]
            
            # compra uma passagem
            comprar_passagem(COMPRA_DE_PASSAGEM, voo_escolhido)

        # se nao estiver (ativo) informar que o servico estah inativo
        else:
            print("serviço de compras de voos não está ativo!")

        time.sleep(5)