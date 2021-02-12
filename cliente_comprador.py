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
    print("acessando a url:", url)

    response = urllib.request.urlopen(url)
    data = response.read()

    return data.decode("utf-8")


def voos_is_alive():
    alive = False

    if acessar(VOOS_IS_ALIVE) == "yes":
        alive = True

    return alive


def compra_is_alive():
    alive = False

    if acessar(COMPRA_DE_PASSAGEM_IS_ALIVE) == "yes":
        alive = True

    return alive


def buscar_voos():
    data = acessar(VOOS)
    data = json.loads(data)

    return data["voos"]

def comprar_passagem(url, voo):
    print("acessando a url:", url)
    resposta = requests.post(url, json=json.dumps(voo))
    if resposta.ok:
        print("Passagem comprada")
        print(resposta.content.decode("utf-8"))
    else:
        print(resposta.content.decode("utf-8"))

if __name__ == "__main__":
    while True:
        # se estiver ativo
        print("#################### NOVA COMPRA DE PASSAGEM ########################")
        # verificar se o servico de voos esta ativo
        if voos_is_alive():

            # buscar os voos disponíveis
            print("serviço de voos está ativo. Solicitando voos...")
            voos = buscar_voos()

            # escolhendo um voo
            voo_escolhido = voos[0]
            
            # compra uma passagem
            if compra_is_alive():
                print("serviço de compra está ativo. Realizando compra...")
                comprar_passagem(COMPRA_DE_PASSAGEM, voo_escolhido)
            else:
                print("serviço de compra está inativo!...")

        # se nao estiver (ativo) informar que o servico esta inativo
        else:
            print("serviço de voos stá inativo!")

        time.sleep(5)