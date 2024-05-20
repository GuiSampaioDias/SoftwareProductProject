'''
CREATE TABLE IF NOT EXISTS tbl_menu
(
    ItemId      BIGINT       NOT NULL AUTO_INCREMENT,
    NomeDoItem   VARCHAR(45)  NOT NULL,
    Categoria      VARCHAR(15)  NOT NULL,
    OrdemDoItem  BIGINT       NOT NULL,
    Descricao      VARCHAR(85)  NULL,
    Preco          FLOAT(6,2),
    ImagemItem     VARCHAR(45)  NOT NULL, 
    PRIMARY KEY (ItemId)

);

CREATE TABLE IF NOT EXISTS tbl_categoria
(
    CategoriaId      BIGINT       NOT NULL AUTO_INCREMENT,
    NomeCategoria   VARCHAR(45)  NOT NULL,
    OrdemCategoria  BIGINT       NOT NULL, 
    PRIMARY KEY (CategoriaId)

);

'''

import os
from flask import Flask, render_template, json, request,jsonify, url_for, redirect
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
app.config['UPLOAD_FILES'] = r'static/data'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('formularioItemMenu.html')

@app.route('/cadastrar_categoria',methods=['POST','GET'])
def cadastrar_categoria():
    nome_categoria = request.form['inputCategoria'].upper()
    ordem_categoria = request.form['inputOrdem']
   
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('insert into tbl_categoria(NomeCategoria, OrdemCategoria) VALUES (%s, %s)', ( nome_categoria, ordem_categoria))
    conn.commit()

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute ('select * from tbl_categoria')
    dados = cursor.fetchall()

    return render_template('listarCategoria.html',dados=dados)

@app.route('/cadastrar_item', methods=['POST', 'GET'])
def cadastro():
    try:
        nome = request.form['inputNome'].title().strip()
        #title pega o comeco das palavras. Strip tira os espacoes
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

        cur = mysql.connection.cursor()
        cur.execute("SELECT NomeDoItem FROM tbl_menu WHERE NomeDoItem = %s",(nome,))

        resultado = cur.fetchone()
        if resultado:
            msg = "Produto ja cadastrados na base de dados"
            return render_template('formularioItemMenu.html',mensagem = msg)
        else:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('insert into tbl_menu (NomeDoItem, Categoria, OrdemDoItem, Descricao, Preco, ImagemItem) VALUES(%s, %s, %s, %s, %s, %s)',(nome, categoria, ordem, descricao, preco, imagem))
            conn.commit()
            msg = "Item cadastrado com sucesso"
            return render_template('formularioItemMenu.html', mensagem = msg)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/menu',methods=['GET'])
def menu():

        conn = mysql.connection 
        cursor = conn.cursor() 
        categoria = "SELECT * FROM tbl_categoria ORDER BY OrdemCategoria"
        cursor.execute(categoria)
        categoria = cursor.fetchall()

    

        conn = mysql.connection 
        cursor = conn.cursor() 
        tuplas_cardapio = "SELECT * FROM tbl_cardapio ORDER BY OrdemDoItem"
        cursor.execute(tuplas_cardapio)
        tuplas_cardapio= cursor.fetchall()
        print(tuplas_cardapio)

        return render_template('listarMenuLayout.html',categoria=categoria,tuplas_cardapio=tuplas_cardapio)

@app.route('/list_categoria')
def categoria():

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute ('select * from tbl_categoria  ORDER BY OrdemCategoria')
    dados = cursor.fetchall()
    
    return render_template('listarCategoria.html', dados=dados)

@app.route('/list_produto',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            
            cursor.execute ('select * from tbl_menu where Categoria = "Bebida"')
            dataBebida = cursor.fetchall()

            cursor.execute ('select * from tbl_menu where Categoria = "Drink"')
            dataDrink = cursor.fetchall()

            cursor.execute ('select * from tbl_menu where Categoria = "Pizza"')
            dataPizza = cursor.fetchall()
            
            cursor.execute ('select * from tbl_menu where Categoria = "Prato"')
            dataPrato = cursor.fetchall()

            cursor.execute ('select * from tbl_menu where Categoria = "Sobremesa"')
            dataSobremesa = cursor.fetchall()
            
            return render_template('listarMenu.html', datas1=dataBebida, datas2=dataDrink,datas3 = dataPizza, datas4 = dataPrato,datas5 = dataSobremesa)

    except Exception as e:
        return json.dumps({'error':str(e)})   
    
@app.route("/atualizar_categoria/<int:id>", methods=['GET', 'POST'])
def categoria_atualizar(id):
    
    id = id
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('select * from tbl_categoria where CategoriaId = %s', (id,))
    data = cursor.fetchall()

    if request.method == 'POST':
        Id = request.form['inputCategoriaId']
        nome_categoria = request.form['inputCategoria'].upper()
        ordem_categoria = request.form['inputOrdem']

        conn = mysql.connection   
        cursor = conn.cursor()
        cursor.execute('UPDATE tbl_categoria SET NomeCategoria = %s, OrdemCategoria = %s WHERE CategoriaId = %s ',(nome_categoria, ordem_categoria, Id))
        conn.commit()

    return render_template("editarCategoria.html", data=data)


@app.route("/excluir_categoria/<int:id>")
def categoria_excluir(id):
    
    id = id
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tbl_categoria WHERE CategoriaId = %s', (id,))
    conn.commit()
    return render_template("listarCategoria.html") 
   
@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):
    try:

            id = int(id)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('select * from tbl_menu where ItemId = %s', (id,))
            data = cursor.fetchall()
            return render_template('editarItemMenu.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        id_pro = int(request.form['ItemId'])
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        ordem = request.form['inputOrdem']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']
        imagem = request.files['imagem']



        if nome and ordem and categoria and preco:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('UPDATE tbl_menu SET NomeDoItem = %s, Categoria = %s, OrdemDoItem = %s, Descricao = %s, Preco = %s, Imagem = %s, WHERE ItemId = %s ', ( nome, categoria, ordem, descricao, preco, imagem, id_pro))
            conn.commit()
            msg = "Edição realizada com sucesso"
            
            cursor.execute ('select * from tbl_menu WHERE ItemId = %s ', (id_pro,))
            data = cursor.fetchall()
            
            return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/delete/<int:id>')
def deleteProduto(id):
    try:
        id = int(id)
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tbl_menu WHERE ItemId = %s', (id,))
        conn.commit()
        msg = "Excluido com sucesso"
        
        cursor.execute ('select * from tbl_menu')
        data = cursor.fetchall()

        return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)