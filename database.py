import mysql.connector

def executar_comandos(query, valores=None, retornar_id=False):
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="JoãoVictor15",
        database="phoenixrise"
    )
    cursor = conexao.cursor()
    
    cursor.execute(query, valores)
    conexao.commit()
    
    if retornar_id:
        resultado = cursor.lastrowid
    else:
        resultado = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    return resultado