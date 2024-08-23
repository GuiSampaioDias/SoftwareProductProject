'''
Lembrando ... quem digita .... erra

CREATE SCHEMA IF NOT EXISTS restaurante;

USE restaurante;

CREATE TABLE IF NOT EXISTS tbl_produto 
( 
    produto_id     BIGINT       NOT NULL   AUTO_INCREMENT, 
    NomeDoProduto  VARCHAR(45)  NOT NULL,
    Categoria      VARCHAR(15)  NOT NULL, 
    ml         FLOAT(5,2)       NULL, 
    Peso_kg        FLOAT(6,2)       NULL,
    Preço          FLOAT(5,2)   NOT NULL, 
    Descrição      VARCHAR(45),
    Ingredientes   VARCHAR(45), 
    PRIMARY KEY (produto_id)
);


SELECT * FROM tbl_produto;

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
    return render_template('formulario_produto.html')



@app.route('/cadastrar', methods=['GET','POST'])
def cadastro():
    try:
        nome = request.form['inputNome'].title().strip()
        #title pega o comeco das palavras e transforma em maiusculo. Strip tira os espacos
        categoria = request.form['inputCategoria']
        ml = request.form['inputML']
        peso = request.form['inputPeso']
        preco = request.form['inputPreco']
        descricao = request.form['inputDescricao'].lower()
        #lower deixa tudo minusculo

        if not ml:
            ml = 0
        if not peso :
            peso = 0
        if not descricao:
            descricao = "Não Há"
    
        cur = mysql.connection.cursor()

        cur.execute("SELECT NomeDoProduto FROM tbl_produto WHERE NomeDoProduto = %s", (nome,))

        resultado = cur.fetchone()

        if resultado:
            msg = "Produto ja cadastrados na base de dados"
            return render_template('formulario_produto.html', mensagem = msg)
        else:
                       
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('insert into tbl_produto (NomeDoProduto, Categoria, ml,Peso_kg, Preço, Descrição) VALUES (%s, %s, %s, %s, %s, %s)', ( nome,categoria,ml,peso,preco,descricao))
            conn.commit()
            msg = "Produtos cadastrados com sucesso"
            return render_template('formulario_produto.html', mensagem = msg)

    except Exception as e:
        return json.dumps({'error':str(e)})
    



@app.route('/list',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute ('select * from tbl_produto')
            data = cursor.fetchall()
            return render_template('listar.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):
    try:
            id = int(id)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('select * from tbl_produto where produto_id = %s', (id,))
            data = cursor.fetchall()
            return render_template('editarProduto.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        id_pro = int(request.form['id_prod'])
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        ml = request.form['inputML']
        peso = request.form['inputPeso']
        preco = request.form['inputPreco']
        descricao = request.form['inputDescricao']

        if not ml:
            ml = 0
        if not peso :
            peso = 0

        if nome and categoria and preco:
            
            conn = mysql.connection
            cursor = conn.cursor()
            print("antes do cursor execute")
            cursor.execute('UPDATE tbl_produto SET NomeDoProduto = %s, Categoria = %s, ml = %s,Peso_kg = %s, Preço = %s, Descrição = %s WHERE produto_id = %s ', ( nome,categoria,ml,peso,preco,descricao,id_pro))
            conn.commit()
            msg = "Edição realizada com sucesso"
            
            cursor.execute ('select * from tbl_produto WHERE produto_id = %s ', (id_pro,))
            data = cursor.fetchall()
            print (data)
            
            return render_template('listar.html', mensagem = msg, datas=data)
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
        cursor.execute('DELETE FROM tbl_produto WHERE produto_id = %s', (id,))
        conn.commit()
        msg = "Excluido com sucesso"
        
        cursor.execute ('select * from tbl_produto')
        data = cursor.fetchall()

        return render_template('listar.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)