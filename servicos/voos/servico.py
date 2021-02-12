from flask import Flask, jsonify, request
from pymemcache.client import base

servico = Flask(__name__)

BANCO_VOLATIL = "banco_volatil"

# "constantes"
IS_ALIVE = "yes"
VERSION = "0.0.1"
DESCRIPTION = "Servico que retorna todos os voos"
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

# rota que grava a lista de voos inicial
@servico.route("/gravar/", methods=["POST", "GET"])
def gravar():
    voos = request.get_json()
    if voos:
        client = base.Client((BANCO_VOLATIL, 11211))
        client.set("voos", voos)

    return "Ok"

# rota que retorna todos os voos
@servico.route("/voos/")
def get_voos():
    resultado = "erro: voos não adicionados"

    client = base.Client((BANCO_VOLATIL, 11211))
    voos = client.get("voos")
    if voos:
        resultado = voos

    return resultado

if __name__ == "__main__":
    servico.run(
        host = "0.0.0.0",
        debug=True
    )