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



@app.route('/',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            arquivos = os.listdir(upload_folder)
            
            cursor.execute ('SELECT * FROM tblMenu')
            data = cursor.fetchall()

            arquivos_contados = [f for f in arquivos if os.path.isfile(os.path.join(upload_folder, f))]
        
            tamanhoArquivos = len(arquivos_contados)
            return render_template('cardapio.html', data = data, lenArquivos = tamanhoArquivos)

    except Exception as e:
        return json.dumps({'error':str(e)})
    


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5007))
    app.run(host='0.0.0.0', port=port, debug=True)