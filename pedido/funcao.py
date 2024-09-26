from flask_mysqldb import MySQL
from flask import Flask
mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)
def conn_cursor():
    conn = mysql.connection
    cursor = conn.cursor()
    return conn, cursor

def extrai__tudo_com_where(tbl, coluna, valor):
    conn, cursor = conn_cursor()
    cursor.execute (f'SELECT * FROM {tbl} WHERE {coluna} = %s',(valor, ))
    resposta = cursor.fetchall()
    return resposta