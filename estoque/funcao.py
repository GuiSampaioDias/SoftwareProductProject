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

'SELECT * FROM tblEstoque ORDER BY nomeDoProduto ASC'
def extrai__tudo_com_order(tbl, coluna, ordem):
    conn, cursor = conn_cursor()
    cursor.execute (f'SELECT * FROM {tbl} ORDER BY {coluna}  {ordem}')
    resposta = cursor.fetchall()
    return resposta

def update_parametro_min_max(tbl, min, max, id):
    conn,cursor = conn_cursor()
    cursor.execute(f'UPDATE {tbl} SET min = %s, sugerido = %s WHERE produtoId = %s',(min, max, id))
    conn.commit()
    