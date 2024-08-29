import os
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '300102'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    conn = mysql.connection 
    cursor = conn.cursor() 
    cursor.execute("SELECT NomeCategoria FROM tbl_categoria")
    categorias=cursor.fetchall()
    return render_template('formularioItemMenu.html',categorias=categorias)




@app.route('/categoria')
def categoria():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute ('select * from tbl_categoria')
    dados = cursor.fetchall()
    
    return render_template('categoria.html', dados=dados)





# @app.route('/cadastrar_categoria',methods=['POST','GET'])
# def cadastrar_categoria():
#     try:
#         nome_categoria = request.form['inputNomeCategoria'].upper()

#         cur = mysql.connection.cursor()
#         cur.execute("SELECT NomeCategoria FROM tbl_categoria WHERE NomeCategoria = %s",(nome_categoria,))
#         resultado = cur.fetchone()

#         conn = mysql.connection
#         cursor = conn.cursor()
#         cursor.execute ('select * from tbl_categoria')
#         dados = cursor.fetchall()

#         if resultado:
#             msg = "Categoria ja cadastrada na base de dados"
#             return render_template('categoria.html',mensagem = msg, dados=dados)
#         else:
#             conn = mysql.connection
#             cursor = conn.cursor()
#             cursor.execute('insert into tbl_categoria(NomeCategoria) VALUES (%s)', ( nome_categoria,))
#             conn.commit()
#             msg = "Categoria cadastrada com sucesso"
#             return render_template('categoria.html',mensagem = msg, dados=dados)
#     except Exception as e:
#         return json.dumps({'error': str(e)})





@app.route('/cadastrar_item', methods=['POST', 'GET'])
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
            return render_template('formularioItemMenu.html',mensagem = msg)
        else:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('insert into tbl_menu (NomeDoItem, Categoria, Descricao, Preco) VALUES(%s, %s, %s, %s)',(nome, categoria,  descricao, preco))
            conn.commit()
            msg = "Item cadastrado com sucesso"
            return render_template('formularioItemMenu.html', mensagem = msg)
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
            
            return render_template('listarMenu.html', datas1=dataBebida, datas2=dataDrink,datas3 = dataPizza, datas4 = dataPrato,datas5 = dataSobremesa)

    except Exception as e:
        return json.dumps({'error':str(e)})
@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):

    try:

            id = int(id)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('select * from tbl_menu where ItemId = %s', (id,))
            print("antes do try edit prod")
            data = cursor.fetchall()
            return render_template('editarItemMenu.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        id_pro = int(request.form['id_prod'])
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']



        if request.method == 'POST':
            if nome and categoria and preco:
                conn = mysql.connection
                cursor = conn.cursor()
                print("Oi")
                cursor.execute('UPDATE tbl_menu SET NomeDoItem = %s, Categoria = %s, Descricao = %s, Preco = %s WHERE ItemId = %s ', ( nome,categoria,descricao, preco, id_pro))
                conn.commit()
                msg = "Edição realizada com sucesso"
            
            cursor.execute ('select * from tbl_menu WHERE ItemId = %s', (id_pro,))
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
        
        cursor.execute ('select * from tbl_menu WHERE ItemId = %s ', (id,))
        data = cursor.fetchall()

        return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)