import mysql.connector

def executar_comandos(query, valores=None, fetchone=False, retornar_id=False):
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="JoãoVictor15",
        database="phoenixrise"
    )
    cursor = conexao.cursor()

    cursor.execute(query, valores)

    resultado = None
    if retornar_id:
        # Caso de INSERT
        conexao.commit()
        resultado = cursor.lastrowid

    elif fetchone:
        # Caso de SELECT com apenas 1 resultado
        resultado = cursor.fetchone()

    else:
        # Caso de SELECT com vários resultados
        resultado = cursor.fetchall()

    conexao.commit()
    cursor.close()
    conexao.close()

    return resultado
