from flask_mysqldb import MySQL
mysql = MySQL()

def conn_cursor():
    conn = mysql.connection
    cursor = conn.cursor()
    return conn, cursor

def extrai__tudo_com_where(tbl, coluna, valor):
    conn, cursor = conn_cursor()
    cursor.execute (f'SELECT * FROM {tbl} WHERE {coluna} = %s',(valor, ))
    resposta = cursor.fetchall()
    return resposta