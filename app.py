# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    UserMixin,
    current_user,
)
from database import executar_comandos
from mapas import gerar_mapa
import bcrypt

app = Flask(__name__)
app.secret_key = "chave_muito_secreta"  # em produção, usar variável de ambiente

# ===== Configuração do Flask-Login (ativa e correta) =====
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_submit"


class User(UserMixin):
    def __init__(self, id, nome, email, senha=None):
        # flask-login exige atributo .id (string ou int)
        self.id = str(id)
        self.nome = nome
        self.email = email
        self.senha = senha

    # opcional: representação
    def __repr__(self):
        return f"<User {self.id} {self.nome}>"


@login_manager.user_loader
def load_user(user_id):
    """
    Carrega usuário pelo id. Retorna None se não existir.
    """
    try:
        query = "SELECT id, nome_usuario, email FROM usuarios WHERE id = %s"
        valores = (user_id,)
        resultado = executar_comandos(query, valores, fetchone=True, retornar_id=False)

        if resultado:
            id_db, nome_usuario, email = resultado
            return User(id_db, nome_usuario, email)
    except Exception as e:
        app.logger.error("load_user error: %s", e)

    return None


# ===== Rotas =====
@app.route("/")
def principal():
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro_submit():
    if request.method == "POST":
        try:
            nome = request.form.get("nome")
            nome_usuario = request.form.get("nome_usuario")
            data_nascimento = request.form.get("data_nascimento")
            email = request.form.get("email")
            senha = request.form.get("senha")
            esporte = request.form.get("esporte")

            if not (nome and nome_usuario and email and senha):
                flash("Preencha todos os campos obrigatórios.", "warning")
                return render_template("cadastro.html")

            # gera hash (bytes) e salva como string no banco (utf-8)
            senha_hash_bytes = bcrypt.hashpw(
                senha.encode("utf-8"), bcrypt.gensalt()
            )
            senha_hash_str = senha_hash_bytes.decode("utf-8")

            query = """INSERT INTO usuarios(nome, nome_usuario, data_nascimento, email, senha_hash)
                       VALUES(%s, %s, %s, %s, %s)"""
            valores = (nome, nome_usuario, data_nascimento, email, senha_hash_str)

            id_usuario = executar_comandos(query, valores, retornar_id=True)
            app.logger.info("ID do usuário cadastrado: %s", id_usuario)

            if esporte:
                query1 = "INSERT INTO usuario_esporte(id_usuario, id_esporte) VALUES(%s, %s)"
                valores1 = (id_usuario, esporte)
                executar_comandos(query1, valores1, retornar_id=False)

            flash("Cadastro efetuado com sucesso! Faça login.", "success")
            return redirect(url_for("login_submit"))
        except Exception as e:
            app.logger.exception("Erro ao cadastrar usuário: %s", e)
            flash("Erro ao cadastrar. Tente novamente.", "danger")
            return render_template("cadastro.html")

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login_submit():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not (email and senha):
            flash("Preencha e-mail e senha.", "warning")
            return render_template("login.html")

        try:
            query = "SELECT id, nome_usuario, senha_hash FROM usuarios WHERE email = %s"
            valores = (email,)
            resultado = executar_comandos(
                query, valores, fetchone=True, retornar_id=False
            )

            if resultado:
                id_usuario, nome_usuario, senha_hash = resultado

                # senha_hash pode vir como str ou bytes dependendo do driver.
                # Garantimos bytes para bcrypt.checkpw
                if isinstance(senha_hash, str):
                    senha_hash_bytes = senha_hash.encode("utf-8")
                else:
                    senha_hash_bytes = senha_hash

                senha_bytes = senha.encode("utf-8")

                if bcrypt.checkpw(senha_bytes, senha_hash_bytes):
                    user = User(id_usuario, nome_usuario, email)
                    login_user(user)
                    flash(f"Bem-vindo, {nome_usuario}!", "success")
                    next_page = request.args.get("next")
                    return redirect(next_page or url_for("inicio"))
                else:
                    mensagem = 'Login incorreto. Tente novamente!'
                    return render_template("login.html", mensagem=mensagem)
            else:
                flash("Email não cadastrado!", "warning")
                return render_template("login.html")
        except Exception as e:
            app.logger.exception("Erro no login: %s", e)
            flash("Erro ao tentar logar. Tente novamente.", "danger")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        # remove qualquer dado customizado de session se existir
        session.pop("nome", None)
        flash("Desconectado com sucesso.", "info")
    except Exception as e:
        app.logger.exception("Erro no logout: %s", e)
        flash("Erro ao deslogar.", "warning")
    return redirect(url_for("login_submit"))


@app.route("/home", methods=["GET"])
#@login_required
def inicio():
    # exemplo: usar current_user em vez de session
    nome = current_user.nome if current_user.is_authenticated else "Visitante"
    return render_template("home.html", nome=nome)


@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    # usa current_user
    nome_usuario = current_user.nome
    # podes buscar mais dados do banco se precisares
    return render_template("perfil.html", nome_usuario=nome_usuario)


@app.route("/mapa")
#@login_required
def mapa_view():
    opcao = request.args.get('select_mapa')
    mapa_html = gerar_mapa(opcao)
    nome = current_user.nome if current_user.is_authenticated else "Visitante"
    titulo = "Mapa das academias da região"
    mensagem = "Academias da região"
    return render_template(
        "mapa.html", nome=nome, mapa_html=mapa_html, titulo=titulo, mensagem=mensagem
    )


@app.route("/mapa/lojas")
#@login_required
def mapa_view_loja():
    mapa_html = gerar_mapa("lojas")
    nome = current_user.nome if current_user.is_authenticated else "Visitante"
    titulo = "Mapa das lojas da região"
    mensagem = "Lojas da região"
    return render_template(
        "mapa.html", nome=nome, mapa_html=mapa_html, titulo=titulo, mensagem=mensagem
    )


#@app.route("/login_fake")
#def login_fake():
#    # rota de teste: cria e loga um user fake
#    user_fake = User(id=999, nome="Dev Teste", email="teste@fake.com")
#    login_user(user_fake)
#    flash("Logado como usuário fake (apenas para teste).", "info")
#    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
