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

# Rotas 
@app.route('/')
def principal():
    return render_template('index.html')

# Rota para processar o formulário enviado
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_submit():
    if request.method == "POST":
        try:
            nome = request.form.get('nome')
            nome_usuario = request.form.get('nome_usuario')
            data_nascimento = request.form.get('data_nascimento')
            email = request.form.get('email')
            senha = request.form.get('senha')
            esporte = request.form.get('esporte')

            if not all([nome, nome_usuario, data_nascimento, email, senha, esporte]):
                raise ValueError('Preencha todos os campos.')
            
            from datetime import datetime
            data_valida = datetime.strptime(data_nascimento, '%Y-%m-%d').date()

            if data_valida.year <1900 or data_valida.year > datetime.now().year:
                raise ValueError('Data de nascimento inválida.')
            
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            query_check = 'SELECT id FROM usuarios WHERE email = %s'
            resultado = executar_comandos(query_check, (email,), fetchone=True)

            if resultado: 
                raise ValueError('Este email já está cadastrado. Tente outro')
            
            query = '''INSERT INTO usuarios(nome, nome_usuario, data_nascimento, email, senha_hash) VALUES(%s, %s, %s, %s, %s)'''
            valores = (nome, nome_usuario, data_nascimento, email, senha_hash)
        
            id_usuario = executar_comandos(query, valores, retornar_id=True)
            print("ID do usuário cadastrado:", id_usuario)


            query1 = '''INSERT INTO usuario_esporte(id_usuario, id_esporte) VALUES(%s, %s)'''
            valores1 = (id_usuario, esporte)
            executar_comandos(query1, valores1, retornar_id=False)
            mensagem = "Cadastro efetuado com sucesso!"

        # Exemplo de segunda query com o ID
        # query2 = "INSERT INTO esportes(esporte, id_usuario) VALUES (%s, %s)"
        # executar_query(query2, (esporte, id_usuario))

            return render_template('login.html', mensagem = mensagem)
        
        except Exception as e:
            mensagem = f'Erro ao cadastrar:{str(e)}.'
            return render_template ('cadastro.html', mensagem = mensagem)
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login_submit():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        query = "SELECT id, nome_usuario, senha_hash FROM usuarios WHERE email = %s"
        valores = (email)
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

            password = resultado[0]
            nome = resultado[1]
            if bcrypt.checkpw(senha.encode('utf-8'), password.encode('utf-8')):
                return redirect(url_for('inicio'))
            
            mensagem = "Erro! Digite os campos novamente!"
            return render_template('login.html',mensagem = mensagem)
        
        else:
            mensagem = "Email não cadastrado! Tente novamente!"
            return render_template('login.html',mensagem = mensagem)    
        

    return  render_template('login.html')

@app.route('/home',methods=['GET'])
@login_required #Só abre se o usuário estiver autenticado, se quiser acessar comente "@login_required".
def inicio():
    return render_template('home.html')

@app.route('/mapa/academia')
@login_required
def mapa_view_academia():
    mapa_html = gerar_mapa('academia')
    #nome = session.get('nome', 'Visitante')
    nome = current_user.nome_usuario 
    return render_template('mapa.html', nome=nome, mapa_html=mapa_html)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('nome', None)
    return redirect(url_for('login_submit'))

@app.route('/mapa/lojas')
@login_required
def mapa_view_loja():
    mapa_html = gerar_mapa('lojas')
    nome = session.get('nome', 'Visitante')
    return render_template('mapa.html', nome=nome, mapa_html=mapa_html)

if __name__ == '__main__':
    app.run(debug=True)
