import sqlite3

DB_PATH = "phoenixrise.db"  # seu arquivo

def executar_comandos(query, valores=None, fetchone=False, retornar_id=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
        cur = conn.cursor()

        if valores:
            cur.execute(query, valores)
        else:
            cur.execute(query)

        if retornar_id:
            conn.commit()
            return cur.lastrowid

        if fetchone:
            resultado = cur.fetchone()
        else:
            resultado = cur.fetchall()

        conn.commit()
        return resultado

    except Exception as e:
        print("ERRO SQLITE:", e)
        return None

    finally:
        conn.close()
