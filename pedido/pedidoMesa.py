import os, sys
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
from funcao import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from Sqls import connCursor

mysql = MySQL()
app = Flask(__name__)

app.config.from_object(config.Config)
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('selectMesa.html')

@app.route('/processar_selecao', methods=['POST'])
def processar_selecao():
    numeroMesa = request.form.get('numero')

    bebida = extrai__tudo_com_where('tblMenu','categoria','Bebida')
    pizza = extrai__tudo_com_where('tblMenu','categoria','Pizza')
    prato = extrai__tudo_com_where('tblMenu','categoria','Prato')
    drink = extrai__tudo_com_where('tblMenu','categoria','Drink')
    sobremesa = extrai__tudo_com_where('tblMenu','categoria','Sobremesa')

    
    return render_template('anotarPedido2.html', pizzas = pizza, bebidas = bebida, pratos = prato, drinks = drink, sobremesas = sobremesa,mesa = numeroMesa)



@app.route('/cadastrarItem', methods=['POST', 'GET'])
def cadastro():
    try:
        nome = request.form['inputNome'].title().strip()
        #title pega o comeco das palavras. Strip tira os espacoes
        categoria = request.form['inputCategoria']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']


        cur = mysql.connection.cursor()
        cur.execute("SELECT nomeDoItem FROM tblMenu WHERE nomeDoItem = %s",(nome,))

        resultado = cur.fetchone()
        if resultado:
            msg = "Produto ja cadastrados na base de dados"
            return render_template('formularioItemMenu.html',mensagem = msg)
        else:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tblMenu (nomeDoItem, categoria, descricao, preco) VALUES(%s, %s, %s, %s)',(nome, categoria,  descricao, preco))
            conn.commit()
            msg = "Item cadastrado com sucesso"
            return render_template('formularioItemMenu.html', mensagem = msg)
    except Exception as e:
        return json.dumps({'error': str(e)})





@app.route('/list',methods=['GET'])
def list():
    try:
            conn, cursor = connCursor()
            cursor.execute ('SELECT * FROM tblMenu WHERE Categoria = "Bebida"')
            dataBebida = cursor.fetchall()

            cursor.execute ('select * from tblMenu WHERE Categoria = "Drink"')
            dataDrink = cursor.fetchall()

            cursor.execute ('select * from tblMenu WHERE Categoria = "Pizza"')
            dataPizza = cursor.fetchall()
            
            cursor.execute ('select * from tblMenu WHERE Categoria = "Prato"')
            dataPrato = cursor.fetchall()

            cursor.execute ('select * from tblMenu WHERE Categoria = "Sobremesa"')
            dataSobremesa = cursor.fetchall()
            
            return render_template('listarMenu.html', datas1=dataBebida, datas2=dataDrink,datas3 = dataPizza, datas4 = dataPrato,datas5 = dataSobremesa)

    except Exception as e:
        return json.dumps({'error':str(e)})
@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):

    try:

            id = int(id)
            conn, cursor = connCursor()
            cursor.execute('SELECT * FROM tblMenu WHERE itemId = %s', (id,))
            data = cursor.fetchall()
            return render_template('editarItemMenu.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        idProd = int(request.form['idProd'])
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']



        if request.method == 'POST':
            if nome and categoria and preco:
                conn, cursor = connCursor()
                cursor.execute('UPDATE tblMenu SET nomeDoItem = %s, categoria = %s, descricao = %s, preco = %s WHERE ItemId = %s ', ( nome,categoria,descricao, preco, idProd))
                conn.commit()
                msg = "Edição realizada com sucesso"
            
            cursor.execute ('SELECT * FROM tblMenu WHERE itemId = %s', (idProd,))
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
        conn, cursor = connCursor()
        cursor.execute('DELETE FROM tblMenu WHERE itemId = %s', (id,))
        conn.commit()
        msg = "Excluido com sucesso"
        
        cursor.execute ('SELECT * FROM tblMenu WHERE itemId = %s ', (id,))
        data = cursor.fetchall()

        return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   
    

@app.route('/addprod/<id>',methods=['POST','GET'])
def listaIngredienteNoPrato(id):
    conn, cursor = connCursor()
    #pegando todos os produtos que fazem cadastrados no prato        
    cursor.execute ('SELECT * FROM tblItemXProd WHERE ItemMenuId = %s',(id,))
    listaProdMenu = cursor.fetchall()

    #pegando todos os produtos cadastrados
    cursor.execute ('SELECT * FROM tblProduto ')
    todosProdutos = cursor.fetchall()
    #pegando o nome do item do menu
    cursor.execute ('SELECT * FROM tblMenu WHERE ItemId = %s',(id,))
    itemMenu = cursor.fetchall()
    

    return render_template('produtoMenu.html', prodMenu = listaProdMenu,totalProd = todosProdutos, prato = itemMenu )

@app.route('/igrediente/delete/<int:idProduto>/<int:idPrato>')
def deleteingredientedoPrato(idProduto,idPrato):
    try:
        idProduto = int(idProduto)
        idPrato = int(idPrato)
        print(f'id prod: {idProduto}')
        print(f'id prato: {idPrato}')
        conn, cursor = connCursor()
        cursor.execute('DELETE FROM tblItemXProd') #WHERE produtoId = %s and ItemMenuId = %s', (idProduto, idPrato))
        conn.commit()
        msg = "Excluido com sucesso"
         
       # cursor.execute ('SELECT * FROM tblMenu WHERE itemId = %s ', (id,))datas=data
        #data = cursor.fetchall()

        return render_template('listarUnicoMenu.html', mensagem = msg )
    
    except Exception as e:
        return json.dumps({'error': str(e)})   
@app.route('/addprod/addigrediente', methods=['POST', 'GET'])
def addIgredienteNoPrato():
    
    nomeProd = request.form['inputNome']    
    nomePrato = request.form['pratoNome']
    idPrato = request.form['idPrato']
    
    conn, cursor = connCursor()
    #pegando os valores do produto selecionado
    cursor.execute ('SELECT * FROM tblProduto WHERE  nomeDoProduto = %s',(nomeProd,))
    prodSelecionado = cursor.fetchall()
    idProd = prodSelecionado[0][0]
    #criando duas variáveis para ver para saber se estamos lhe dando com um produto em mL ou em gramas
    
    mlProd = prodSelecionado[0][3]
    pesoProd = prodSelecionado[0][4]
    
    if mlProd == 0:
        peso = request.form['inputMlGram']
        quantidade = float(peso) /pesoProd
        ml = 0

    else:
        ml = request.form['inputMlGram']
        quantidade = float(ml)/mlProd
        peso = 0
    cursor.execute("SELECT * FROM tblItemXProd WHERE ItemMenuId = %s AND produtoId = %s",(idPrato,idProd))
    resultado = cursor.fetchone()
    vitoria = listaIngredienteNoPrato(idPrato)
    if resultado:
        msg = "Produto ja cadastrados na base de dados"
        return vitoria
    else:
        cursor.execute('INSERT INTO tblItemXProd (ItemMenuId, nomeItemMenu, produtoId, nomeDoProduto, ml, pesoGramas, quantidade) VALUES(%s, %s, %s, %s, %s, %s, %s)',(idPrato, nomePrato, idProd, nomeProd, ml,peso, quantidade))
        conn.commit()
        msg = "Item cadastrado com sucesso"
        return vitoria 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5006))
    app.run(host='0.0.0.0', port=port, debug=True)