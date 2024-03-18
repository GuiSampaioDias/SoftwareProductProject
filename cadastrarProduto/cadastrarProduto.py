'''
Lembrando ... quem digita .... erra

CREATE SCHEMA IF NOT EXISTS restaurante;

USE restaurante;

CREATE TABLE IF NOT EXISTS tbl_produto 
( 
    produto_id     BIGINT       NOT NULL   AUTO_INCREMENT, 
    NomeDoProduto  VARCHAR(45)  NOT NULL,
    Categoria      VARCHAR(15)  NOT NULL, 
    Quantidade 	   INT          NOT NULL,
    litros         FLOAT(5,2)       NULL, 
    Peso_kg        FLOAT(6,2)       NULL,
    Preço          FLOAT(5,2)   NOT NULL, 
    Descrição      VARCHAR(45),
    Ingredientes   VARCHAR(45), 
    PRIMARY KEY (produto_id)
);


SELECT * FROM tbl_produto

'''

import os
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
#from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_HOST'] = '172.17.0.7'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('formulario_produto.html')


@app.route('/cadastrar',methods=['POST','GET'])
def signUp():
    try:
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        quantidade = request.form['inputQuantidade']
        litros = request.form['inputLitros']
        peso = request.form['inputPeso']
        preco = request.form['inputPreco']
        descricao = request.form['inputDescricao']
        ingredientes = request.form['inputIngredientes']


        if not quantidade:
            quantidade  = 0
        if not litros:
            litros = 0
        if not peso :
            peso = 0
        if not ingredientes :
            ingredientes = "Não Há"
    

        print(nome)
        print(categoria)
        print(quantidade)
        print(litros)
        print(peso)
        print(preco)
        print(descricao) 
        print(ingredientes)

        # validate the received values
        if nome and categoria and preco:
            
            conn = mysql.connection
            cursor = conn.cursor()
            #_hashed_password = _password
            cursor.execute('insert into tbl_produto (NomeDoProduto, Categoria, Quantidade, litros,Peso_kg, Preço, Descrição, Ingredientes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', ( nome,categoria,quantidade,litros,peso,preco,descricao,ingredientes ))
            conn.commit()
            msg = "Produtos cadastrados com sucesso"
            return render_template('formulario_produto.html', mensagem = msg)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/list',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute ('select NomeDoProduto, Categoria, Quantidade, litros,Peso_kg, Preço, Descrição, Ingredientes from tbl_produto')
            data = cursor.fetchall()
            print(data[0])
            return render_template('listar.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})
    


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)