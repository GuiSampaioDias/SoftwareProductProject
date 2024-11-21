import os, sys
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
from datetime import datetime, timezone
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from Sqls import SelectSemOrdem, DeleteComWhere, SelectComWhere, connCursor

mysql = MySQL()
app = Flask(__name__)

app.config.from_object(config.Config)
mysql.init_app(app)


@app.route('/')
def main():
    try:
        prods = SelectSemOrdem('tblProduto', item = 'nomeDoProduto')

        return render_template('formularioItem.html',produtos=prods)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    

@app.route('/cadastrar',methods=['POST','GET'])
def cadastro():
    try:
        prods = SelectSemOrdem('tblProduto', item = 'nomeDoProduto')
        nome = request.form['inputNome']
        #title pega o comeco das palavras. Strip tira os espacoes
        quantidade = request.form['inputQuantidade']
        preco = request.form['inputPreco']
        precoTotal = float(preco) * float(quantidade)
        descricao = request.form['inputDescricao'].lower()
        #lower deixa tudo minusculo

        if not descricao:
            descricao = "Não Há"

        conn, cursor = connCursor()
        cursor.execute('INSERT into tblItemOrdem (nomeItem,quantidade,precoProduto, precoTotalPorProduto, descricao) VALUES (%s, %s, %s, %s, %s)', (nome,quantidade,preco,precoTotal,descricao))
        conn.commit()
        msg = "Item ordem cadastrados com sucesso"
            
        return render_template('formularioItem.html', mensagem = msg,produtos=prods)

    except Exception as e:
        return json.dumps({'error':str(e)})
    
    
@app.route('/list',methods=['GET'])
def list():
    try:
        data = SelectSemOrdem('tblItemOrdem')
        return render_template('listar.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):
    try:
            id = int(id)
            data = SelectComWhere('tblItemOrdem','itemOrdemId', id)

            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('SELECT nomeDoProduto FROM tblProduto ORDER BY produtoId')
            prods = cursor.fetchall()

            return render_template('editarItem.html', datas=data, produtos=prods)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        idProd = int(request.form['idProd'])
        nome = request.form['inputNome']
        quantidade = request.form['inputQuantidade']
        preco = request.form['inputPreco']
        precoTotal = float(preco) * int(quantidade)
        descricao = request.form['inputDescricao'].lower()


        if nome and quantidade and preco:
            
            conn, cursor = connCursor()
            cursor.execute('UPDATE tblItemOrdem SET nomeItem = %s, quantidade = %s, precoProduto = %s, precoTotalPorProduto = %s, descricao = %s WHERE itemOrdemId = %s', (nome,quantidade,preco,precoTotal,descricao,idProd))
            conn.commit()
            msg = "Edição realizada com sucesso"
        
            data = SelectComWhere('tblItemOrdem','itemOrdemId',idProd)
            
            return render_template('listar.html', mensagem = msg, datas=data)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/delete/<int:id>')
def delete(id):
    try:
        id = int(id)
        DeleteComWhere('tblItemOrdem','itemOrdemId', id)
        msg = "Excluido com sucesso"
        
        data = SelectSemOrdem('tblItemOrdem')

        return render_template('listar.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})  

@app.route('/estoque/<id>', methods=['POST','GET'])
def sobe_estoque(id):
    try:
        conn, cursor = connCursor()
        data = SelectComWhere('tblItemOrdem','itemOrdemId', id)
        nome = data[0][1] 
        quantidade = float(data[0][2])
        precoUnitario = data[0][3] 
        precoTotal = quantidade * precoUnitario
        dia = datetime.now()
        data = SelectComWhere('tblProduto','nomeDoProduto', nome)
        idProd = data[0][0]
        mlTotal = data[0][3] * quantidade
        gramasTotal = data[0][4] * quantidade
        cursor.execute('INSERT INTO tblEstoque (produtoId, nomeDoProduto, ml, pesoGramas, quantidade, min, sugerido) VALUES (%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE quantidade = quantidade + VALUES(quantidade), ml = ml + VALUES(ml), pesoGramas = pesoGramas + VALUES(pesoGramas)',(idProd, nome,mlTotal,gramasTotal, quantidade, 0, 0))
        conn.commit()
        tipo = 'compra'
        cursor.execute('INSERT INTO tblHistorico (produtoId, nomeDoProduto, quantidade, precoUnitario, precoTotal, data, tipo) VALUES (%s,%s,%s,%s,%s,%s,%s)',(idProd, nome,quantidade, precoUnitario, precoTotal, dia, tipo))
        delete(id)
        retorno = list()
        return retorno

    except Exception as e:
        print("except ")
        return json.dumps({'error':str(e)})
     

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port, debug=True)