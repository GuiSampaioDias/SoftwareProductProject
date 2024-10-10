import os
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)


upload_folder = os.path.join(os.path.dirname(__file__), '../Cardapio/static/img')

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

def proximo_nome_arquivo():
    arquivos_existentes = os.listdir(upload_folder)
    
    # Filtrar apenas arquivos de imagem
    imagens_existentes = [f for f in arquivos_existentes if f.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}]
    
    # Definir o próximo número da sequência
    return str(len(imagens_existentes) + 1)






@app.route('/')
def main():
    conn = mysql.connection 
    cursor = conn.cursor() 
    cursor.execute("SELECT nomeCategoria FROM tblCategoria")
    categorias=cursor.fetchall()
    return render_template('formularioItemMenu.html',categorias=categorias)




# @app.route('/categoria')
# def categoria():
#     conn = mysql.connection
#     cursor = conn.cursor()
#     cursor.execute ('SELECT * FROM tblCategoria')
#     dados = cursor.fetchall()
    
#     return render_template('categoria.html', dados=dados)





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





@app.route('/cadastrarItem', methods=['POST', 'GET'])
def cadastro():
    try:
        nome = request.form['inputNome'].title().strip()
        #title pega o comeco das palavras. Strip tira os espacoes
        categoria = request.form['inputCategoria']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']
        arquivo = request.files['imagem']



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
            extensao = arquivo.filename.rsplit('.', 1)[1].lower()

    # Gerar o próximo nome de arquivo (1, 2, 3, etc.)
            nome_arquivo = proximo_nome_arquivo() + '.' + extensao

    # Caminho completo para salvar o arquivo
            caminho_arquivo = os.path.join(upload_folder, nome_arquivo)




    # Salvar o arquivo na pasta especificada
            arquivo.save(caminho_arquivo)
            return render_template('formularioItemMenu.html', mensagem = msg)
    except Exception as e:
        return json.dumps({'error': str(e)})





@app.route('/list',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            
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
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tblMenu WHERE itemId = %s', (id,))
            data = cursor.fetchall()
            return render_template('editarItemMenu.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto2/<id>',methods=['GET'])    
def editProdNoPrato(id):

    try:

            id = int(id)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tblItemXProd WHERE IdItemXProd = %s', (id,))
            print("antes do try edit prod")
            data = cursor.fetchall()
            return render_template('editarProdutoNoPrato.html', datas=data)
    
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
                conn = mysql.connection
                cursor = conn.cursor()
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
    
@app.route('/produto2/<id>',methods=['POST','GET'])
def editarProduto2(id):
    
    try:
        idItemXProd = int(id)
        peso = request.form['inputPeso']
        
        if request.method == 'POST':
            if peso and idItemXProd :
                conn = mysql.connection
                cursor = conn.cursor()

                cursor.execute ('SELECT * FROM tblItemXProd WHERE idItemXProd = %s',(idItemXProd,))
                produtoNoPrato = cursor.fetchall()
                #pegando os valores do produto selecionado
                cursor.execute ('SELECT * FROM tblProduto WHERE  produtoId = %s',(produtoNoPrato[0][3],))
                prodSelecionado = cursor.fetchall()
                print(prodSelecionado)

                if produtoNoPrato[0][5] == 0:
                    gramas = peso
                    quantidade = float(gramas) /prodSelecionado[0][4]
                    ml = 0
                else:
                    ml = peso
                    quantidade = float(ml) /prodSelecionado[0][3]
                    gramas = 0
                cursor.execute('UPDATE tblItemXProd SET ml = %s, pesoGramas = %s, quantidade = %s WHERE idItemXProd = %s ', ( ml,gramas, quantidade, idItemXProd))
                conn.commit()
                msg = "Edição realizada com sucesso"
            
            renderizar = listaIngredienteNoPrato(produtoNoPrato[0][1])
            return renderizar
            #return render_template('listarUnicoMenu.html', mensagem = msg, )
           
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

        cursor.execute('SELECT * FROM tblItemXProd WHERE ItemMenuId = %s', (id,))
        itemXProd = cursor.fetchall()

        if itemXProd == ():
            cursor.execute('DELETE FROM tblMenu WHERE itemId = %s', (id,))
            conn.commit()
            msg = "Excluido com sucesso"
        else:
            msg = "Item não pode ser excluido pois está associado a outra tabela"
        
        cursor.execute ('SELECT * FROM tblMenu WHERE itemId = %s ', (id,))
        data = cursor.fetchall()

        return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   
    

@app.route('/addprod/<id>',methods=['POST','GET'])
def listaIngredienteNoPrato(id):
    conn = mysql.connection
    cursor = conn.cursor()
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

@app.route('/igrediente/delete/<int:idItemXProd>')
def deleteingredientedoPrato(idItemXProd):
    try:
        idItemXProd = int(idItemXProd)   
        print(f'id_item_x_prod: {idItemXProd}')
        conn = mysql.connection
        cursor = conn.cursor()
        
        #pegando o id do prato que vai ter o produto deletado         
        cursor.execute ('SELECT ItemMenuId FROM tblItemXProd WHERE idItemXProd = %s',(idItemXProd,))
        idPrato = cursor.fetchall()
        
        cursor.execute('DELETE FROM tblItemXProd WHERE idItemXProd = %s ', (idItemXProd,))
        conn.commit()
        msg = "Excluido com sucesso"
        
        
         
       # cursor.execute ('SELECT * FROM tblMenu WHERE itemId = %s ', (id,))datas=data
        #data = cursor.fetchall()

        #return render_template('listarUnicoMenu.html', mensagem = msg )
        renderizar = listaIngredienteNoPrato(idPrato)
        return renderizar
    
    except Exception as e:
        return json.dumps({'error': str(e)})   
    

@app.route('/addprod/addigrediente', methods=['POST', 'GET'])
def addIgredienteNoPrato():
    
    nomeProd = request.form['inputNome']    
    nomePrato = request.form['pratoNome']
    idPrato = request.form['idPrato']
    
    conn = mysql.connection
    cursor = conn.cursor()
    #pegando os valores do produto selecionado
    cursor.execute ('SELECT * FROM tblProduto WHERE  nomeDoProduto = %s',(nomeProd,))
    prodSelecionado = cursor.fetchall()
    idProd = prodSelecionado[0][0]
    #criando duas variáveis para ver para saber se estamos lhe dando com um produto em mL ou em gramas
    
    
    cursor.execute ('SELECT * FROM tblMenu WHERE ItemId = %s',(idPrato,))
    itemMenu = cursor.fetchall()

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
    
    if resultado:
        msg = "Produto ja cadastrados na base de dados"
        listaIngredienteNoPrato(idPrato)
        vitoria = listaIngredienteNoPrato(idPrato)
        return vitoria
    else:
        cursor.execute('INSERT INTO tblItemXProd (ItemMenuId, nomeItemMenu, produtoId, nomeDoProduto, ml, pesoGramas, quantidade) VALUES(%s, %s, %s, %s, %s, %s, %s)',(idPrato, nomePrato, idProd, nomeProd, ml,peso, quantidade))
        conn.commit()
        vitoria = listaIngredienteNoPrato(idPrato)
        msg = "Item cadastrado com sucesso"
        return vitoria 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)