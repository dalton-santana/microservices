from flask import Flask, jsonify, request
from pymemcache.client import base
import json

servico = Flask(__name__)

BANCO_VOLATIL = "banco_volatil"

# "constantes"
IS_ALIVE = "yes"
VERSION = "0.0.1"
DESCRIPTION = "Servico que realiza compras de passagens"
AUTHOR = "Dalton"
EMAIL = "dalton_jss@hotmail.com"

# rotas do meu servico
# rota de ping (o cliente deve perguntar se o servico estah atendendo)
@servico.route("/isalive/")
def is_alive():
    return IS_ALIVE


# rota que retorna informacoes basicas sobre o servico e o autor do servico
@servico.route("/info/")
def get_info():
    info = jsonify(
        version = VERSION,
        description = DESCRIPTION, 
        author = AUTHOR,
        email = EMAIL
    )

    return info

@servico.route("/compra/", methods=["POST", "GET"])
def comprar_passagem():
    voo_escolhido = request.get_json()
   
    client = base.Client((BANCO_VOLATIL, 11211))

    voos = client.get("voos")
    voos = voos.decode("utf-8")
    voos = json.loads(voos)

    reduzir_vaga_no_voo(voos, voo_escolhido)

    return "ok"

def reduzir_vaga_no_voo(voos, voo_escolhido):
    voo_escolhido = json.loads(voo_escolhido)
    for voo in voos['voos']:
        if voo['id'] == voo_escolhido['id']:
            print(voo, flush=True)
            voo['passagens_vendidas'] += 1

    client = base.Client((BANCO_VOLATIL, 11211))
    client.set("voos", json.dumps(voos))



if __name__ == "__main__":
    servico.run(
        host = "0.0.0.0",
        debug=True
    )