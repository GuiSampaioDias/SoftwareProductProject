from flask_mysqldb import MySQL
mysql = MySQL()

def connCursor():
    conn = mysql.connection
    cursor = conn.cursor()
    return conn, cursor

def listarVariosSemOrdem(tbl):
    conn, cursor = connCursor()
    cursor.execute (f'SELECT * FROM {tbl}')
    resposta = cursor.fetchall()
    return resposta