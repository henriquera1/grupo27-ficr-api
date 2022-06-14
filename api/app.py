from http.client import OK
from flask_cors import CORS, cross_origin
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/hydratedb'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50))
    sobrenome = db.Column(db.String(50))
    cpf = db.Column(db.String(11))
    bairro = db.Column(db.String(50))
    endereco = db.Column(db.String(50))
    ocorrencia = db.Column(db.Integer)
    situacao = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "sobrenome": self.sobrenome, "cpf": self.cpf, "bairro": self.bairro, "endereco": self.endereco, "ocorrencia": self.ocorrencia, "situacao": self.situacao}


#GET
@app.route("/report", methods=["GET"])
@cross_origin()
def getReport():
    user = Usuario.query.all()
    user_json = [usuario.to_json() for usuario in user]

    return gera_response(200, "usuarios", user_json)


#GET BY ID
@app.route("/report/<id>", methods=["GET"])
@cross_origin()
def getReportById(id):
    user = Usuario.query.filter_by(id=id).first()
    user_json = user.to_json()

    return gera_response(200, "usuario", user_json)

#POST
@app.route("/report", methods=["POST"])
@cross_origin()
def postReport():
    body = request.get_json()
    
    try:
        user = Usuario(nome=body["nome"], sobrenome=body["sobrenome"], cpf=body["cpf"], bairro=body["bairro"], endereco=body["endereco"], ocorrencia=body["ocorrencia"], situacao=body["situacao"])
        db.session.add(user)
        db.session.commit()
        return gera_response(201, "usuario", user.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar")


#GERAR RESPONSE
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()