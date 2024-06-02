'''
CREATE TABLE IF NOT EXISTS tbl_menu
(
    item_menu_id      BIGINT       NOT NULL AUTO_INCREMENT,
    NomeDoItem   VARCHAR(45)  NOT NULL,
    Categoria      VARCHAR(15)  NOT NULL,
    Descricao      VARCHAR(85)  NULL,
    Preco          FLOAT(6,2),
    PRIMARY KEY (item_menu_id)

);

'''

import os
from flask import Flask, render_template, json, request,jsonify
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
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
        cur = mysql.connection.cursor()
        cur.execute("SELECT NomeDoItem FROM tbl_menu WHERE NomeDoItem = %s",(nome,))

        resultado = cur.fetchone()
        if resultado:
            msg = "Produto ja cadastrados na base de dados"
            return render_template('formulario_item_menu.html',mensagem = msg)
        else:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('insert into tbl_menu (NomeDoItem, Categoria, Descricao, Preco) VALUES(%s, %s, %s, %s)',(nome, categoria, descricao, preco))
            conn.commit()
            msg = "Item cadastrado com sucesso"
            return render_template('formulario_item_menu.html', mensagem = msg)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/list',methods=['GET'])
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
            return render_template('listar_menu.html', datas1=dataBebida, datas2=dataDrink,datas3 = dataPizza, datas4 = dataPrato,datas5 = dataSobremesa)

    except Exception as e:
        return json.dumps({'error':str(e)})
       
@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):
    try:

            id = int(id)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('select * from tbl_menu where item_menu_id = %s', (id,))
            data = cursor.fetchall()
            print(data)
            return render_template('editarItemMenu.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        id_item = int(request.form['id_item_menu'])
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']



        if nome and categoria and preco:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('UPDATE tbl_menu SET NomeDoItem = %s, Categoria = %s, Descricao = %s, Preco = %s WHERE item_menu_id = %s ', ( nome,categoria,descricao, preco, id_item))
            conn.commit()
            msg = "Edição realizada com sucesso"
            
            cursor.execute ('select * from tbl_menu WHERE item_menu_id = %s ', (id_item,))
            data = cursor.fetchall()
            print(data)
            
            return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/delete/<int:id>')
def delete(id):
    try:
        id = int(id)
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tbl_menu WHERE item_menu_id = %s', (id,))
        conn.commit()
        msg = "Excluido com sucesso"
        
        cursor.execute ('select * from tbl_menu WHERE item_menu_id = %s ', (id,))
        data = cursor.fetchall()

        return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)