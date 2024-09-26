import os
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
from funcao import *


@app.route('/list',methods=['GET'])
def list():
    try:
               
            
            data = extrai__tudo_com_order('tblEstoque', 'nomeDoProduto', 'ASC')
            return render_template('listarEstoque.html', datas = data)

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/item_estoque/<id>',methods=['GET'])
def parametrizar(id):
     prod_no_estoque = extrai__tudo_com_where('tblEstoque','produtoId',int(id))
     return render_template('parametrizar.html',datas = prod_no_estoque)

@app.route('/parametrizar/', methods=['POST','GET'])
def atualizar_parametros():
    print('\n\n\noioioi')
    produtoId = int(request.form['idProd'])
    par_min = int(request.form['inputMin'])
    par_max = int(request.form['inputMaximo'])
    update_parametro_min_max('tblestoque',par_min, par_max, produtoId)
    vitoria = list()
    return vitoria
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(host='0.0.0.0', port=port, debug=True)