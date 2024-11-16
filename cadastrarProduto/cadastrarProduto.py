import os, sys
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from Sqls import SelectVariosSemOrdem, SelectTudoComWhere

mysql = MySQL()
app = Flask(__name__)

app.config.from_object(config.Config)
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('formularioProduto.html')



@app.route('/cadastrar', methods=['GET','POST'])
def cadastro():
    try:
        nome = request.form['inputNome'].title().strip()
        #title pega o comeco das palavras e transforma em maiusculo. Strip tira os espacos
        categoria = request.form['inputCategoria']
        ml = request.form['inputML']
        peso = request.form['inputPeso']
        descricao = request.form['inputDescricao'].lower()
        #lower deixa tudo minusculo
        if not ml:
            ml = 0
        else:
            peso = 0
        if not descricao:
            descricao = "Não Há"

        if not ml and not peso:
            msg = "Cadastre alguma gramatura ou volume"
            return render_template('formularioProduto.html', mensagem = msg)
    
        cur = mysql.connection.cursor()

        cur.execute("SELECT nomeDoProduto FROM tblProduto WHERE nomeDoProduto = %s", (nome,))
        resultado = cur.fetchone()

        if resultado:
            msg = "Produto ja cadastrados na base de dados"
            return render_template('formularioProduto.html', mensagem = msg)
        else:
                       
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tblProduto (nomeDoProduto, categoria, ml,pesoGramas, descricao) VALUES (%s, %s, %s, %s, %s)', ( nome,categoria,ml,peso,descricao))
            conn.commit()
            msg = "Produtos cadastrados com sucesso"
            return render_template('formularioProduto.html', mensagem = msg)

    except Exception as e:
        return json.dumps({'error':str(e)})
    



@app.route('/list',methods=['GET'])
def list():
    try:
            pesquisa = request.args.get('pesquisa', '')
            if pesquisa:
                
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tblProduto WHERE nomeDoProduto LIKE %s ORDER BY nomeDoProduto", (f"%{pesquisa}%",))
                data = cursor.fetchall()
                return render_template('listar.html', datas=data)
            else:
                data = SelectVariosSemOrdem('tblProduto')
                return render_template('listar.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):
    try:
            id = int(id)
            data =  SelectTudoComWhere('tblproduto','produtoId', id)
            return render_template('editarProduto.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    try:
        idProd = int(request.form['idProd'])
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        ml = request.form['inputML']
        peso = request.form['inputPeso']
        descricao = request.form['inputDescricao']

        if not ml:
            ml = 0
        if not peso :
            peso = 0

        if nome and categoria:
            
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('UPDATE tblProduto SET nomeDoProduto = %s, categoria = %s, ml = %s,pesoGramas = %s, descricao = %s WHERE produtoId = %s ', (nome,categoria,ml,peso,descricao,idProd))
            conn.commit()
            msg = "Edição realizada com sucesso"
    
            data =  SelectTudoComWhere('tblproduto','produtoId', idProd)
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

        cursor.execute('SELECT nomeDoProduto FROM tblProduto WHERE produtoId = %s', (id,))
        nome = cursor.fetchall()  
        cursor.execute('SELECT * FROM tblHistorico WHERE produtoId = %s', (id,))
        tabelaHistorico = cursor.fetchall()
        cursor.execute('SELECT * FROM tblItemXProd WHERE produtoId = %s', (id,))
        tabelaItemXProd = cursor.fetchall()

        cursor.execute('SELECT * FROM tblItemOrdem WHERE nomeItem = %s', (nome,))
        tabelaOrdem = cursor.fetchall()



        if tabelaHistorico == () and tabelaItemXProd == () and tabelaOrdem == ():
            cursor.execute('DELETE FROM tblProduto WHERE produtoId = %s', (id,))
            conn.commit()
            msg = "Excluido com sucesso"

        else:
            msg = "Item não pode ser excluido pois está associado a outra tabela"
        
        data = None

        return render_template('delete.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)