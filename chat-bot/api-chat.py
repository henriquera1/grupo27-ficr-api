from http.client import OK
from flask_cors import CORS, cross_origin
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#GET
@app.route("/pergunta/<id>", methods=["GET"])
@cross_origin()
def getReport(id):

    res = ""

    if(id == '1'):
        res = "Nosso objetivo é alinhar as demandas da população, bem como as urgências advindas de catástrofes naturais. Mostrando de forma enfática as necessidades mais urgentes e pontuais da sociedade recifense. Fazendo assim, com que a cidade fique mais sustentável e agradável de se viver."

    elif(id == '2'):
        res = "Com os devidos apontamentos da população recifense, traremos uma ideia de cidade mais participativa e agradável para todos."

    else:
        res = "Insira um valor entre 1 e 2"


    return gera_response(200, "resposta", res)



def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run()