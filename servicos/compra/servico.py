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

@servico.route("/compra/", methods=["POST"])
def comprar_passagem():
    # pega o voo escolhido pelo cliente
    voo_escolhido = request.get_json()
    
    # busca os voos disponiveis
    client = base.Client((BANCO_VOLATIL, 11211))

    voos = client.get("voos")
    voos = voos.decode("utf-8")
    voos = json.loads(voos)

    # escolher o voo e comprar a passagem se existir e atualizar info do voo
    resposta = escolher_voo(voos, voo_escolhido)

    return resposta

def escolher_voo(voos, voo_escolhido):
    resposta = "voo nao encontrado"

    voo_escolhido = json.loads(voo_escolhido)

    # verifica se o voo existe
    for voo in voos['voos']:
        if voo['id'] == voo_escolhido['id'] and voo['vagas'] != voo['passagens_vendidas']:
            voo['passagens_vendidas'] += 1
            resposta = "ok"

    # salva a relação de voos atualizada com a passagem vendida ou a lista anterior sem venda              
    client = base.Client((BANCO_VOLATIL, 11211))
    client.set("voos", json.dumps(voos))

    return resposta

if __name__ == "__main__":
    servico.run(
        host = "0.0.0.0",
        debug=True
    )