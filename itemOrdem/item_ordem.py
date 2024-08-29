import os
from flask import Flask, render_template, json, request
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
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('select NomeDoProduto from tbl_produto')
        prods = cursor.fetchall()

        return render_template('formulario_item.html',produtos=prods)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    

@app.route('/cadastrar',methods=['POST','GET'])
def cadastro():
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('select NomeDoProduto from tbl_produto')
        prods = cursor.fetchall()
        nome = request.form['inputNome']
        #title pega o comeco das palavras. Strip tira os espacoes
        quantidade = request.form['inputQuantidade']
        preco = request.form['inputPreco']
        preco_total = float(preco) * float(quantidade)
        descricao = request.form['inputDescricao'].lower()
        #lower deixa tudo minusculo

        if not descricao:
            descricao = "Não Há"

        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('insert into tbl_item_ordem (NomeItem,Quantidade,PreçoProduto, PreçoTotalPorProduto, Descrição) VALUES (%s, %s, %s, %s, %s)', ( nome,quantidade,preco,preco_total,descricao))
        conn.commit()
        msg = "Item ordem cadastrados com sucesso"
            
        return render_template('formulario_item.html', mensagem = msg,produtos=prods)

    except Exception as e:
        return json.dumps({'error':str(e)})
    



@app.route('/list',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute ('select * from tbl_item_ordem')
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
            cursor.execute('select * from tbl_item_ordem where ItemOrdem_id = %s', (id,))
            data = cursor.fetchall()

    
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('select NomeDoProduto from tbl_produto order by produto_id')
            prods = cursor.fetchall()

            return render_template('editarItem.html', datas=data, produtos=prods)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        id_pro = int(request.form['id_prod'])
        nome = request.form['inputNome']
        quantidade = request.form['inputQuantidade']
        preco = request.form['inputPreco']
        preco_total = float(preco) * int(quantidade)
        descricao = request.form['inputDescricao'].lower()


        if nome and quantidade and preco:
            
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('UPDATE tbl_item_ordem SET NomeItem = %s, Quantidade = %s, PreçoProduto = %s, PreçoTotalPorProduto = %s, Descrição = %s where ItemOrdem_id = %s', (nome,quantidade,preco,preco_total,descricao,id_pro))
            conn.commit()
            msg = "Edição realizada com sucesso"
            
            cursor.execute ('select * from tbl_item_ordem WHERE ItemOrdem_id = %s', (id_pro,))
            data = cursor.fetchall()
            
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
        cursor.execute('DELETE FROM tbl_item_ordem WHERE ItemOrdem_id = %s', (id,))
        conn.commit()
        msg = "Excluido com sucesso"
        
        cursor.execute ('select * from tbl_item_ordem')
        data = cursor.fetchall()

        return render_template('listar.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})  

@app.route('/estoque/<id>', methods=['POST','GET'])
def sobe_estoque(id):
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('select * from tbl_item_ordem where ItemOrdem_id = %s', (id,))
        data = cursor.fetchall()
        nome = data[0][1] 
        quantidade = float(data[0][2])
        cursor.execute('select * from tbl_produto where NomeDoProduto = %s', (nome,))
        data = cursor.fetchall()
        id_prod = data[0][0]
        ml_total = data[0][3] * quantidade
        gramas_total = data[0][4] * quantidade
        cursor.execute('INSERT INTO tbl_estoque (Produto_id, NomeDoProduto, Ml, Peso_gramas, quantidade) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE quantidade = quantidade + VALUES(quantidade), Ml = Ml + VALUES(Ml), Peso_gramas = Peso_gramas + VALUES(Peso_gramas)',(id_prod, nome,ml_total,gramas_total, quantidade))
        conn.commit()
        list()
        delete(id)
        return render_template('listar.html')

    except Exception as e:
        print("except ")
        return json.dumps({'error':str(e)})
     

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port, debug=True)