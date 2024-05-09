'''
CREATE TABLE IF NOT EXISTS tbl_cardapio
( 
    item_id     BIGINT       NOT NULL   AUTO_INCREMENT, 
    item_nome  VARCHAR(45)  NOT NULL,
    item_ordem  BIGINT       NOT NULL,
    item_categoria      VARCHAR(15)  NOT NULL,
    item_descricao      VARCHAR(110)NOT NULL,
    item_preco          DECIMAL(5,2)   NOT NULL, 
    item_imagem     VARCHAR(60)  NOT NULL,   
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

@app.route('/cardapio_layout/')
def cardapio_layout():

    conn = mysql.connection 
    cursor = conn.cursor() 
    categoria = "SELECT * FROM tbl_categoria ORDER BY categoria_ordem"
    cursor.execute(categoria)
    categoria = cursor.fetchall()

   

    conn = mysql.connection 
    cursor = conn.cursor() 
    tuplas_cardapio = "SELECT * FROM tbl_cardapio  ORDER BY item_ordem"
    cursor.execute(tuplas_cardapio)
    tuplas_cardapio= cursor.fetchall()
    print(tuplas_cardapio)

    return render_template('cardapio_layout.html',categoria=categoria,tuplas_cardapio=tuplas_cardapio)

@app.route('/cardapio_listar',methods=['GET'])
def cardapio_lista():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute ('select * from tbl_categoria ORDER BY categoria_ordem')
    categoria = cursor.fetchall()
    

    conn = mysql.connection 
    cursor = conn.cursor() 
    cardapio = "SELECT * FROM tbl_cardapio ORDER BY item_ordem"
    cursor.execute(cardapio)
    cardapio = cursor.fetchall()
    
    return render_template('cardapio_lista.html', categoria=categoria, cardapio=cardapio)



@app.route('/novo')
def novo():
    conn = mysql.connection 
    cursor = conn.cursor() 
    cursor.execute("SELECT categoria_nome FROM tbl_categoria")
    categorias=cursor.fetchall()
    return render_template('cardapio_novo_item.html',categorias=categorias)


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
        data = cursor.fetchone()
        
        print(data)
        
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
        conn = mysql.connection 
        cursor = conn.cursor() 
        cursor.execute("SELECT categoria_nome FROM tbl_categoria")
        categorias=cursor.fetchall()
        return render_template("cardapio_atualizar.html", data=data, categorias=categorias)

@app.route('/categoria')
def categoria():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute ('select * from tbl_categoria  ORDER BY categoria_ordem')
    dados = cursor.fetchall()
    
    return render_template('categoria.html', dados=dados)

@app.route('/novoItem_categoria',methods=['POST','GET'])
def novo_item_categoria():
    item = request.form['inputCategoria'].upper()
    ordem = request.form['inputOrdem']
   
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('insert into tbl_categoria(categoria_nome, categoria_ordem) VALUES (%s, %s)', ( item,ordem))
    conn.commit()

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute ('select * from tbl_categoria')
    dados = cursor.fetchall()

    return render_template('categoria.html',dados=dados)

@app.route("/categoiar_atualizar_item/<int:id>", methods=['GET', 'POST'])
def categoria_atualizar(id):
    id = id
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('select * from tbl_categoria where categoria_id = %s', (id,))
    data = cursor.fetchall()

    if request.method == 'POST':
        categoria_id = request.form['categoria_id']
        categoria = request.form['inputCategoria'].upper()
        ordem = request.form['inputOrdem']

        conn = mysql.connection   
        cursor = conn.cursor()
        cursor.execute('UPDATE tbl_categoria SET categoria_nome=%s, categoria_ordem=%s WHERE categoria_id = %s ',(categoria, ordem, categoria_id))
        conn.commit()
        return redirect(url_for('categoria'))
    return render_template("categoria_atualizar_teste.html", data=data)


@app.route("/categoria_excluir_item/<int:id>")
def categoria_excluir(id):
    id = id
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tbl_categoria WHERE categoria_id = %s', (id,))
    conn.commit()
    return redirect(url_for('categoria'))



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)