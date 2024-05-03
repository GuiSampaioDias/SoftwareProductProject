'''
use restaurante;

    CREATE TABLE IF NOT EXISTS tbl_cardapio
    ( 
        item_id     BIGINT       NOT NULL   AUTO_INCREMENT, 
        item_nome  VARCHAR(45)  NOT NULL,
        item_ordem  BIGINT       NOT NULL,
        item_categoria      VARCHAR(15)  NOT NULL,
        item_descricao      VARCHAR(45)NOT NULL,
        item_preco          FLOAT(4,2)   NOT NULL, 
        item_imagem     VARCHAR(45)  NOT NULL,   
        PRIMARY KEY (item_id)
    );
'''


import os
from flask import Flask, render_template, json, request,jsonify, url_for, redirect
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

mysql = MySQL()
app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
app.config['UPLOAD_FILES'] = r'static/data'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('cardapio_home.html')

@app.route('/novo')
def novo():
    return render_template('cardapio_novo_item.html')


@app.route('/novoItem',methods=['POST','GET'])
def novo_item():
    item = request.form['inputItem']
    categoria = request.form['inputCategoria']
    ordem = request.form['inputOrdem']
    descricao = request.form['inputDescricao']
    preco = request.form['inputPreco']

    imagem = request.files['imagem']
    
    nome_seguro = secure_filename(imagem.filename)
    caminho =  os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    app.config['UPLOAD_FILES'],
    'cardapio',
    nome_seguro
    )
    imagem.save(caminho)

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('insert into tbl_cardapio(item_nome, item_categoria, item_ordem, item_descricao, item_preco,item_imagem) VALUES (%s, %s, %s, %s, %s, %s )', ( item,categoria,ordem,descricao,preco,nome_seguro ))
    conn.commit()
    return redirect(url_for('cardapio_lista'))

@app.route('/listar',methods=['GET'])
def cardapio_lista():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute ('select * from tbl_cardapio')
    dados = cursor.fetchall()
    return render_template('cardapio_lista.html', dados=dados)

    
@app.route("/item_excluir/<int:id>")
def excluir(id):
    id = int(id)
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tbl_cardapio WHERE item_id = %s', (id,))
    conn.commit()
    return redirect(url_for('cardapio_lista'))

@app.route("/item_atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
        id = id
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('select * from tbl_cardapio where item_id = %s', (id,))
        data = cursor.fetchall()
        
        if request.method == 'POST':
            item_id = request.form['item_id']
            item = request.form['inputItem']
            categoria = request.form['inputCategoria']
            ordem = request.form['inputOrdem']
            descricao = request.form['inputDescricao']
            preco = request.form['inputPreco']

            imagem = request.files['imagem']

            nome_seguro = secure_filename(imagem.filename)
            caminho =  os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FILES'],
            'cardapio',
            nome_seguro
            )
            imagem.save(caminho)
           
            conn = mysql.connection   
            cursor = conn.cursor()
            cursor.execute('UPDATE tbl_cardapio SET item_nome = %s, item_categoria = %s, item_ordem = %s, item_descricao = %s,item_preco = %s, item_imagem = %s WHERE item_id = %s'  , ( item,categoria,ordem,descricao,preco,nome_seguro, item_id))
            conn.commit()
            return redirect(url_for('cardapio_lista'))
        return render_template("cardapio_atualizar.html", data=data)


@app.route('/cardapio_layout/')
def cardapio_layout():

    conn = mysql.connection 
    cursor = conn.cursor() 
    petisco = "SELECT * FROM tbl_cardapio WHERE item_categoria = 'Petisco' ORDER BY item_ordem"
    cursor.execute(petisco)
    resultado_petiscos = cursor.fetchall()


    cursor = conn.cursor() 
    pizza = "SELECT * FROM tbl_cardapio WHERE item_categoria = 'Pizza' ORDER BY item_ordem"
    cursor.execute(pizza)
    resultado_pizza = cursor.fetchall()

    cursor = conn.cursor() 
    bebida = "SELECT * FROM tbl_cardapio WHERE item_categoria = 'Bebida' ORDER BY item_ordem"
    cursor.execute(bebida)
    resultado_bebida = cursor.fetchall()


    cursor = conn.cursor() 
    sobremesa = "SELECT * FROM tbl_cardapio WHERE item_categoria = 'Sobremesa' ORDER BY item_ordem"
    cursor.execute(sobremesa)
    resultado_sobremesa = cursor.fetchall()

    cursor = conn.cursor() 
    drinks = "SELECT * FROM tbl_cardapio WHERE item_categoria = 'Drink' ORDER BY item_ordem"
    cursor.execute(drinks)
    resultado_drinks = cursor.fetchall()

    
    return render_template('cardapio_layout.html', resultado_petiscos=resultado_petiscos, 
                           resultado_pizza=resultado_pizza,
                           resultado_bebida=resultado_bebida,
                           resultado_sobremesa=resultado_sobremesa,
                           resultado_drinks=resultado_drinks)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port, debug=True)