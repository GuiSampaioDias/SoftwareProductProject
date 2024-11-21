import os, sys
from flask import Flask, render_template, json
from flask_mysqldb import MySQL
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config 
from Sqls import connCursor
mysql = MySQL()
app = Flask(__name__)

app.config.from_object(config.Config)
mysql.init_app(app)

@app.route('/list',methods=['GET'])
def list():
    try:
            conn, cursor = connCursor()
            cursor.execute ('SELECT * FROM tblHistorico WHERE tipo = "compra" ORDER BY  data DESC')
            data = cursor.fetchall()
            cursor.execute('SELECT * FROM tblHistorico WHERE tipo = "venda" ORDER BY data DESC')
            data2 = cursor.fetchall()
            return render_template('listarHistorico.html', datasCompra=data, datasVenda=data2)

    except Exception as e:
        return json.dumps({'error':str(e)})




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    app.run(host='0.0.0.0', port=port, debug=True)