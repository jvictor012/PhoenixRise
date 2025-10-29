from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from database import executar_comandos
from mapas import gerar_mapa
import bcrypt

app = Flask(__name__)
app.secret_key = 'chave_muito_secreta'

# Configuração Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_submit'

class User(UserMixin):
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

@login_manager.user_loader
def load_user(user_id):
    query = "SELECT id, nome_usuario, email FROM usuarios WHERE id = %s"
    valores = user_id
    resultado = executar_comandos(query, valores, fetchone = True, retornar_id = False)

    if resultado:
        id, nome_usuario, email = resultado
        return User(id, nome_usuario, email)

    return None

#Rotas
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

        #Gerando a query  para fazer o login
        query = "SELECT senha_hash, id FROM usuarios WHERE email = %s"
        valores = (email,)
        resultado = executar_comandos(query, valores,fetchone=True, retornar_id=False)            

        if resultado:
            id_usuario, nome_usuario, senha_hash = resultado

            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
                user = User(id_usuario, nome_usuario, email)
                login_user = user

                session['nome'] = nome_usuario

                return redirect(url_for('home'))
            else:
                mensagem = 'Senha incorreta!'
                return render_template('login.html', mensagem = mensagem)
        
        else:
            mensagem = "Email não cadastrado!"
            return render_template('login.html',mensagem = mensagem)    
        
    return  render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('nome', None)
    return redirect(url_for('login_submit'))

@app.route('/home',methods=['GET'])
#@login_required
def inicio():
    return render_template('home.html')

@app.route('/perfil', methods=['GET', 'POST'])
#@login_required
def perfil():
    usuario_id = session['usuario_id']
    query = '''SELECT nome_usuario FROM usuarios WHERE id = %s'''
    value = (usuario_id,)
    resultado = executar_comandos(query, value, fetchone=True)
    if resultado:
        nome_usuario = resultado[0]
    else:
        nome_usuario = 'Usuário não encontrado!'

    return render_template('perfil.html', nome_usuario = nome_usuario)

@app.route('/mapa/academia')
#@login_required
def mapa_view_academia():
    mapa_html = gerar_mapa('academia')
    nome = session.get('nome', 'Visitante')
    return render_template('mapa.html', nome=nome, mapa_html=mapa_html)

@app.route('/mapa/lojas')
#@login_required
def mapa_view_loja():
    mapa_html = gerar_mapa('lojas')
    nome = session.get('nome', 'Visitante')
    return render_template('mapa.html', nome=nome, mapa_html=mapa_html)

if __name__ == '__main__':
    app.run(debug=True)