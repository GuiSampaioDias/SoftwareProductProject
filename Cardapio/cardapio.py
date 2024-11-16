import os, sys
from flask import Flask, render_template, json, jsonify
from flask_mysqldb import MySQL
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from Sqls import listarVariosSemOrdem

mysql = MySQL()
app = Flask(__name__)

upload_folder = os.path.join(os.path.dirname(__file__), '../Cardapio/static/img')

app.config.from_object(config.Config)
mysql.init_app(app)

@app.route('/imagens')
def listar_imagens():
    # Filtra arquivos apenas com extensões de imagem
    imagens = [f for f in os.listdir(upload_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return jsonify(imagens)

@app.route('/',methods=['GET'])
def list():
    try:
            arquivos = os.listdir(upload_folder)
            data = listarVariosSemOrdem('tblMenu')
            arquivos_contados = [f for f in arquivos if os.path.isfile(os.path.join(upload_folder, f))]
        
            tamanhoArquivos = len(arquivos_contados)
            return render_template('cardapio.html', data = data, lenArquivos = tamanhoArquivos)

    except Exception as e:
        return json.dumps({'error':str(e)})
    


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5007))
    app.run(host='0.0.0.0', port=port, debug=True)