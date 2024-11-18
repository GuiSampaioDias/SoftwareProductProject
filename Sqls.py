from flask_mysqldb import MySQL
mysql = MySQL()

def connCursor():
    conn = mysql.connection
    cursor = conn.cursor()
    return conn, cursor

def SelectSemOrdem(tbl, item = '*'):
    conn, cursor = connCursor()
    cursor.execute (f'SELECT {item} FROM {tbl}')
    resposta = cursor.fetchall()
    return resposta

def SelectComWhere(tbl, coluna, valor, item = '*'):
    conn, cursor = connCursor()
    cursor.execute (f'SELECT {item} FROM {tbl} WHERE {coluna} = %s',(valor, ))
    resposta = cursor.fetchall()
    return resposta

def DeleteComWhere(tbl, coluna, valor):
    conn, cursor = connCursor()
    cursor.execute (f'DELETE FROM {tbl} WHERE {coluna} = %s',(valor, ))
    resposta = conn.commit()
    return resposta

data =SelectComWhere('tblItemOrdem','itemOrdemId',id)