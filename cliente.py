import urllib.request
import json
import time

# rotas do servico de voos (voos)
VOOS_URL_SERVICO = "http://172.28.1.1:5000/"
VOOS_IS_ALIVE = VOOS_URL_SERVICO + "isalive/"
VOOS = VOOS_URL_SERVICO + "voos/"


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

def imprimir_voos(voos):
    for VOO in voos:
        print(VOO["data"])
        print(VOO["titulo"])
        print("url:", VOO["endereco"])

def get_voos():
    data = acessar(VOOS)
    data = json.loads(data)

    return data["voos"]


if __name__ == "__main__":
    while True:
        # verificar se o servico de voos estah ativo
        if voos_is_alive():
            # se estiver ativo
            print("serviço de voos está ativo. Solicitando voos...")
            # imprimir as voos sobre jogos eletronicos
            voos = get_voos()

            print("\n\n")
            print("###############################################################")
            print("#################### JOGOS ELETRÔNICOS ########################")
            print("###############################################################")
            imprimir_voos(voos)
        # se nao estiver (ativo) informar que o servico estah inativo
        else:
            print("serviço de voos não está ativo!")

        time.sleep(5)