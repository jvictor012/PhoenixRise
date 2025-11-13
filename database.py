import mysql.connector

def executar_comandos(query, valores=None, fetchone=False, retornar_id=False):
    conexao = mysql.connector.connect(
        host="localhost",
        user="phoenix",
        password="1920eu",
        database="phoenixrise"
    )
    cursor = conexao.cursor()

    cursor.execute(query, valores)
    resultado = None

    # detecta tipo de query
    comando = query.strip().split()[0].upper()

    if comando == "SELECT":
        if fetchone:
            resultado = cursor.fetchone()
        else:
            resultado = cursor.fetchall()

    elif comando == "INSERT" and retornar_id:
        conexao.commit()
        resultado = cursor.lastrowid

    else:
        conexao.commit()

    cursor.close()
    conexao.close()
    return resultado

