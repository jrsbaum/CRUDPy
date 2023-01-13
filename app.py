from flask import Flask, request, render_template, jsonify, redirect, flash, url_for
from pymongo import database
from werkzeug.exceptions import NotFound
import db as dbts
from produto import Produto

app = Flask(__name__)

def connect_db():
    # Centralizando a criação da conexão com o banco de dados
    return dbts.dbConnection()

def validate_product(nome, preco, quantidade):
    # Utilizando funções de validação para verificar se os campos obrigatórios foram preenchidos
    if not nome or not preco or not quantidade:
        raise NotFound("Dados incompletos")
    try:
        preco = float(preco)
        quantidade = int(quantidade)
    except ValueError:
        raise NotFound("Preco e quantidade devem ser numeros")

# rota padrao home
@app.route('/')
def home():
    produtos = connect_db()['produtos']
    produtosRecebidos = produtos.find()
    return render_template('index.html', produtos=produtosRecebidos)

# POST
@app.route('/produtos', methods=['POST'])
def addProduto():
    produtos = connect_db()['produtos']
    nome = request.form['nome']
    preco = request.form['preco']
    quantidade = request.form['quantidade']

    validate_product(nome, preco, quantidade)
    produto = Produto(nome, preco, quantidade)
    produtos.insert_one(produto.toDBCollection())
    flash("Produto adicionado com sucesso")
    return redirect(url_for('home'))

# PUT
@app.route('/edit/<string:produto_nome>', methods=['PUT'])
def edit(produto_nome):
    produtos = connect_db()['produtos']
    nome = request.form['nome']
    preco = request.form['preco']
    quantidade = request.form['quantidade']

    validate_product(nome, preco, quantidade)
    produtos.update_one({'nome': produto_nome}, {'$set': {'nome': nome, 'preco': preco, 'quantidade': quantidade}})
    flash("Produto atualizado com sucesso")
    return redirect(url_for('home'))


# DELETE

@app.route('/delete/string:produto_nome', methods=['DELETE'])
def delete(produto_nome):
    produtos = database['produtos']
    produtos.delete_one({'nome': produto_nome})
    return redirect(url_for('home'))

@app.errorhandler(404)
def notFound(erro=None):
    message ={
        'mensagem': 'Nao foi possivel localizar ' + request.url,
        'status': '404 Not Found'
    }

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'The requested resource was not found: ' + request.url,
        'status': 404
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp








if __name__ == '__main__':
    app.run(debug=True, port=4200)

