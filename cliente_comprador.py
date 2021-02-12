import urllib.request
import json
import time
import requests
import random

# rotas do servico de voos (voos)
VOOS_URL_SERVICO = "http://172.28.1.1:5000/"
COMPRA_DE_PASSAGEM_URL_SERVICO = "http://172.28.1.2:5000/"
CHECK_IN_URL_SERVICO = "http://172.28.1.3:5000/"

VOOS_IS_ALIVE = VOOS_URL_SERVICO + "isalive/"
COMPRA_DE_PASSAGEM_IS_ALIVE = COMPRA_DE_PASSAGEM_URL_SERVICO + "isalive/"
CHECK_IN_IS_ALIVE = CHECK_IN_URL_SERVICO + "isalive/"

VOOS = VOOS_URL_SERVICO + "voos/"
COMPRA_DE_PASSAGEM = COMPRA_DE_PASSAGEM_URL_SERVICO + "compra/"
CHECK_IN = CHECK_IN_URL_SERVICO + "checkin/"

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

def checkin_is_alive():
    alive = False

    if acessar(CHECK_IN_IS_ALIVE) == "yes":
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
        print(">>>> Passagem comprada!")
    else:
        print(resposta.content.decode("utf-8"))

def realizar_check_in(url, voo):
    print("acessando a url:", url)
    resposta = requests.post(url, json=json.dumps(voo))
    if resposta.ok:
        print(">>>> Check-in realizado!")
    else:
        print(resposta.content.decode("utf-8"))

if __name__ == "__main__":
    while True:
        print("\n")
        # verificar se o servico de voos esta ativo
        if voos_is_alive():
            # se estiver ativo
            print("\n")
            print("#################### BUSCANDO VOOS ########################")
           
            # buscar os voos disponíveis
            voos = buscar_voos()

            # escolhendo um voo aleatório para compra
            voo_aletorio = random.randrange(0, len(voos) - 1)
            voo_escolhido = voos[voo_aletorio]
            
            print("\n")

            # compra uma passagem
            if compra_is_alive():
                print("\n")
                print("#################### NOVA COMPRA DE PASSAGEM ########################")
            
                print("serviço de compra está ativo. Realizando compra...")
                comprar_passagem(COMPRA_DE_PASSAGEM, voo_escolhido)
            else:
                print("serviço de compra está inativo!...")


            # escolhendo um voo aleatório para realizar checkin
            voo_aletorio = random.randrange(0, len(voos) - 1)
            voo_escolhido = voos[voo_aletorio]
            
            print("\n")
            
            # realizar um checkin
            if checkin_is_alive():
                print("\n")
                print("#################### NOVO CHECKIN ########################")
                realizar_check_in(CHECK_IN, voo_escolhido)
            else:
                print("serviço de checkin está inativo!...")
            

        # se nao estiver (ativo) informar que o servico esta inativo
        else:
            print("serviço de voos stá inativo!")

        time.sleep(5)