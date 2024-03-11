'''
Lembrando ... quem digita .... erra

create schema restaurante;

use restaurante;

CREATE TABLE tbl_produto 
( 
    produto_id     BIGINT       NOT NULL   AUTO_INCREMENT, 
    NomeDoProduto  VARCHAR(45)  NOT NULL,
    Categoria      VARCHAR(15)  NOT NULL, 
    litros         FLOAT(5,2)       NULL, 
    Peso_kg        FLOAT(6,2)       NULL,
    Preço          FLOAT(5,2)   NOT NULL, 
    Descrição      VARCHAR(45),
    Ingredientes   VARCHAR(45), 
    PRIMARY KEY (produto_id)
);

'''

import os
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
#from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'impacta2024'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_HOST'] = '172.17.0.7'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/produto')
def showSignUp():
    return render_template('formulario_produto.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _nome = request.form['inputNome']
        _categoria = request.form['inputCategoria']
        _litros = request.form['inputLitros']
        _peso = request.form['inputPeso']
        _preco = request.form['inputPreco']
        _descricao = request.form['inputDescricao']
        _ingredientes = request.form['inputIngredientes']
    

        print(_nome)
        print(_categoria)
        print(_litros)
        print(_peso)
        print(_preco)
        print(_descricao)
        print(_ingredientes)

        # validate the received values
        if _nome and _categoria and _preco:
            
            conn = mysql.connection
            cursor = conn.cursor()
            #_hashed_password = _password
            cursor.execute('insert into tbl_produto (NomeDoProduto, Categoria, litros,Peso_kg, Preço, Descrição, Ingredientes) VALUES (%s, %s, %s, %s, %s, %s, %s)', ( _nome,_categoria,_litros, ))
            conn.commit()

            return render_template('signup.html')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        #cursor.close() 
        #conn.close()
        print('ops')

@app.route('/list',methods=['POST','GET'])
def list():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute ('select NomeDoProduto, Categoria, litros,Peso_kg, Preço, Descrição, Ingredientes from tbl_produto')
            data = cursor.fetchall()
            print(data[0])

            conn.commit()
            return render_template('signup2.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

