from flask import Flask, render_template, request, redirect, url_for
from database import executar_comandos


app = Flask(__name__)

@app.route('/')
def principal():
    return render_template('index.html')

# Rota para processar o formulário enviado
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_submit():
    if request.method == "POST":
        nome = request.form.get('nome')
        nome_usuario = request.form.get('nome_usuario')
        data_nascimento = request.form.get('data_nascimento')
        email = request.form.get('email')
        senha = request.form.get('senha')
        esporte = request.form.get('esporte')

        query = '''INSERT INTO usuarios(nome, nome_usuario, data_nascimento, email, senha_hash) VALUES(%s, %s, %s, %s, %s)'''
        valores = (nome, nome_usuario, data_nascimento, email, senha)
        
        id_usuario = executar_comandos(query, valores, retornar_id=True)
        print("ID do usuário cadastrado:", id_usuario)



        query1 = '''INSERT INTO usuario_esporte(id_usuario, id_esporte) VALUES(%s, %s)'''
        valores1 = (id_usuario, esporte)
        executar_comandos(query1, valores1, retornar_id=False)

        # Exemplo de segunda query com o ID
        # query2 = "INSERT INTO esportes(esporte, id_usuario) VALUES (%s, %s)"
        # executar_query(query2, (esporte, id_usuario))

        mensagem = "Cadastro efetuado com sucesso!"
        return render_template('login.html', mensagem=mensagem)
    
    return render_template('cadastro.html')




@app.route('/login', methods=['GET', 'POST'])
def login_submit():
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    print(f"Login concluído")
    return  render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
