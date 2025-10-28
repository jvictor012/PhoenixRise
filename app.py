from flask import Flask, render_template, request, redirect, url_for, session
from database import executar_comandos
from map import mapa
import bcrypt

app = Flask(__name__)
app.secret_key = 'chave_muito_secreta'

#rota de 
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
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        esporte = request.form.get('esporte')

        query = '''INSERT INTO usuarios(nome, nome_usuario, data_nascimento, email, senha_hash) VALUES(%s, %s, %s, %s, %s)'''
        valores = (nome, nome_usuario, data_nascimento, email, senha_hash)
        
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
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        '''Gerando a query  para fazer o login'''
        query = "SELECT senha_hash, nome_usuario FROM usuarios WHERE email = %s"
        valores = (email,)

        resultado = executar_comandos(query, valores,fetchone=True, retornar_id=False)            
        

        if resultado:
            password = resultado[0]
            nome = resultado[1]
            if bcrypt.checkpw(senha.encode('utf-8'), password.encode('utf-8')):
                return redirect(url_for('home'))
            
            mensagem = "Erro! Digite os campos novamente!"
            return render_template('login.html',mensagem = mensagem)
        
        else:
            mensagem = "Email não cadastrado! Tente novamente!"
            return render_template('login.html',mensagem = mensagem)    
    return  render_template('login.html')


@app.route('/home', methods = ['GET'])
def home():
    mapa_html = mapa._repr_html_() 
    nome = session.get('nome', 'Visitante')
    return render_template('home.html', nome=nome, mapa_html = mapa_html)


if __name__ == '__main__':
    app.run(debug=True)
