import os, sys
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from Sqls import updateParametroMinMax, SelectComWhere, SelectComOrder


mysql = MySQL()
app = Flask(__name__)
app.config.from_object(config.Config)
mysql.init_app(app)

@app.route('/list',methods=['GET'])
def list():
    try:
            data = SelectComOrder('tblEstoque', 'nomeDoProduto', 'ASC')
            return render_template('listarEstoque.html', datas = data)

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/item_estoque/<id>',methods=['GET'])
def parametrizar(id):
     prod_no_estoque = SelectComWhere('tblEstoque','produtoId',int(id))
     return render_template('parametrizar.html',datas = prod_no_estoque)

@app.route('/parametrizar/', methods=['POST','GET'])
def atualizar_parametros():
    produtoId = int(request.form['idProd'])
    par_min = int(request.form['inputMin'])
    par_max = int(request.form['inputMaximo'])
    updateParametroMinMax('tblestoque',par_min, par_max, produtoId)
    vitoria = list()
    return vitoria
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(host='0.0.0.0', port=port, debug=True)