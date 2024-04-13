'''
CREATE TABLE IF NOT EXISTS tbl_menu
(
    item_menu_id      BIGINT       NOT NULL AUTO_INCREMENT,
    NomeDoItem   VARCHAR(45)  NOT NULL,
    Categoria      VARCHAR(15)  NOT NULL,
    Descrição      VARCHAR(85)  NULL,
    Preço          FLOAT(6,2),
    PRIMARY KEY (pedido_id)

);

'''

import os
from flask import Flask, render_template, json, request,jsonify
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'impacta1234'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('formulario_item_menu.html')

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastro():
    try:
        nome = request.form['inputNome'].title().strip()
        #title pega o comeco das palavras. Strip tira os espacoes
        categoria = request.form['inputCategoria']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']
        print('Estou aqui')
        cur = mysql.connection.cursor()
        cur.execute("SELECT NomeDoItem FROM tbl_menu WHERE NomeDoItem = %s",(nome,))

        resultado = cur.fetchone()
        if resultado:
            msg = "Produto ja cadastrados na base de dados"
            return render_template('formulario_item_menu.html',mensagem = msg)
        else:
            conn = mysql.connection
            cursor = conn.cursor()
            print('Estou aqui agora')
            cursor.execute('insert into tbl_menu (NomeDoItem, Categoria, Descrição, Preço) VALUES(%s, %s, %s, %s)',(nome, categoria, descricao, preco))
            conn.commit()
            msg = "Item cadastrado com sucesso"
            return render_template('formulario_item_menu.html', mensagem = msg)
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)