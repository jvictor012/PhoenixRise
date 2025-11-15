# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
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
from cloudinary_service import cloudinary

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

    def __repr__(self):
        return f"<User {self.id} {self.nome}>"


@login_manager.user_loader
def load_user(user_id):
    try:
        query = "SELECT id, nome_usuario, email FROM usuarios WHERE id = ?"
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

            # gera hash e salva como string
            senha_hash_bytes = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
            senha_hash_str = senha_hash_bytes.decode("utf-8")

            query = """INSERT INTO usuarios(nome, nome_usuario, data_nascimento, email, senha_hash, foto_url)
                       VALUES(?, ?, ?, ?, ?, ?)"""
            valores = (nome, nome_usuario, data_nascimento, email, senha_hash_str, None)

            id_usuario = executar_comandos(query, valores, retornar_id=True)
            app.logger.info("ID do usuário cadastrado: %s", id_usuario)

            if esporte:
                query1 = "INSERT INTO usuario_esporte(id_usuario, id_esporte) VALUES(?, ?)"
                valores1 = (id_usuario, esporte)
                executar_comandos(query1, valores1)

            return redirect(url_for("login_submit"))
        except Exception as e:
            app.logger.exception("Erro ao cadastrar usuário: %s", e)
            erro = "Ocorreu um erro. Por favor, tente novamente!"
            return render_template("cadastro.html", erro=erro)

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
            query = "SELECT id, nome_usuario, senha_hash FROM usuarios WHERE email = ?"
            valores = (email,)
            resultado = executar_comandos(query, valores, fetchone=True, retornar_id=False)

            if resultado:
                id_usuario, nome_usuario, senha_hash = resultado

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
                    mensagem = "Login incorreto. Tente novamente!"
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
        session.pop("nome", None)
        flash("Desconectado com sucesso.", "info")
    except Exception as e:
        app.logger.exception("Erro no logout: %s", e)
        flash("Erro ao deslogar.", "warning")
    return redirect(url_for("login_submit"))


@app.route("/home", methods=["GET"])
def inicio():
    nome = current_user.nome if current_user.is_authenticated else "Visitante"
    query = "SELECT url_image, usuario_id, descricao, data_publicacao FROM posts"
    posts = executar_comandos(query)
    return render_template("home.html", nome=nome, posts=posts)


@app.route("/feed")
@login_required
def feed():
    query = """
        SELECT p.descricao, p.url_image, p.data_publicacao, u.nome_usuario, u.foto_url
        FROM posts p
        JOIN usuarios u ON p.usuario_id = u.id
        ORDER BY p.data_publicacao DESC
    """
    posts_raw = executar_comandos(query)

    posts = []
    for p in posts_raw:
        descricao, url_image, data_publicacao, nome_usuario, foto_url = p

        # Converter string para datetime (se vier como string)
        if isinstance(data_publicacao, str):
            try:
                data_publicacao = datetime.strptime(data_publicacao, "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    data_publicacao = datetime.strptime(data_publicacao, "%Y-%m-%d")
                except:
                    data_publicacao = None  # evita erros

        posts.append((descricao, url_image, data_publicacao, nome_usuario, foto_url))

    return render_template("feed.html", posts=posts)


@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    usuario_id = current_user.id
    nome_usuario = current_user.nome

    if request.method == "POST":

        if "imagem_perfil" in request.files:
            imagem_perfil = request.files.get("imagem_perfil")
            if imagem_perfil and imagem_perfil.filename != "":
                image = cloudinary.uploader.upload(imagem_perfil)
                url_imagem_perfil = image["secure_url"]

                query = "UPDATE usuarios SET foto_url = ? WHERE id = ?"
                executar_comandos(query, (url_imagem_perfil, usuario_id))
                return redirect(url_for("perfil"))

        nivel_esportivo = request.form.get("nivel_esportivo")
        if nivel_esportivo:
            query = "UPDATE usuarios SET nivel_esportivo = ? WHERE id = ?"
            executar_comandos(query, (nivel_esportivo, usuario_id))
            return redirect(url_for("perfil"))

        interesses_selecionados = request.form.getlist("interesses")
        if interesses_selecionados:
            for nome_esporte in interesses_selecionados:
                query = "SELECT id_esporte FROM esportes WHERE nome_esporte = ?"
                resultado = executar_comandos(query, (nome_esporte,), fetchone=True)
                if resultado:
                    id_esporte = resultado[0]
                    query_check = "SELECT * FROM usuario_esporte WHERE id_usuario = ? AND id_esporte = ?"
                    existe = executar_comandos(query_check, (usuario_id, id_esporte), fetchone=True)
                    if not existe:
                        query_insert = "INSERT INTO usuario_esporte (id_usuario, id_esporte) VALUES(?, ?)"
                        executar_comandos(query_insert, (usuario_id, id_esporte))
            return redirect(url_for("perfil"))

    query = "SELECT nome_usuario, email, foto_url, nivel_esportivo FROM usuarios WHERE id = ?"
    usuario = executar_comandos(query, (usuario_id,), fetchone=True)

    if usuario:
        nome_usuario, email, foto_url, nivel_esportivo = usuario
    else:
        nome_usuario, email, foto_url, nivel_esportivo = "", "", None, ""

    query_interesses = """
        SELECT e.nome_esporte
        FROM usuario_esporte ue
        JOIN esportes e ON ue.id_esporte = e.id_esporte        
        WHERE ue.id_usuario = ?
    """
    interesses_usuario = executar_comandos(query_interesses, (usuario_id,))
    interesses_lista = [i[0] for i in interesses_usuario] if interesses_usuario else []

    return render_template(
        "perfil.html",
        resultado=foto_url,
        nome_usuario=nome_usuario,
        email=email,
        nivel_esportivo=nivel_esportivo,
        interesses=interesses_lista,
    )


@app.route("/interesses", methods=["GET", "POST"])
def interesses():
    if request.method == "POST":
        interesses = request.form.getlist("interesses")
        usuario_id = current_user.id

        if interesses:
            for nome_esporte in interesses:
                query = "SELECT id_esporte FROM esportes WHERE nome_esporte = ?"
                resultado = executar_comandos(query, (nome_esporte,), fetchone=True)
                if resultado:
                    id_esporte = resultado[0]
                    query_check = "SELECT * FROM usuario_esporte WHERE id_usuario = ? AND id_esporte = ?"
                    existe = executar_comandos(query_check, (usuario_id, id_esporte), fetchone=True)
                    if not existe:
                        query_insert = "INSERT INTO usuario_esporte (id_usuario, id_esporte) VALUES(?, ?)"
                        executar_comandos(query_insert, (usuario_id, id_esporte))
            return redirect(url_for("perfil"))

    return render_template("interesses.html")


@app.route("/mapa")
def mapa_view():
    opcao = request.args.get("select_mapa", "0")
    nome = current_user.nome if current_user.is_authenticated else "Visitante"
    mensagem = "Visualize academias, quadras e lojas esportivas"
    mapa_html = gerar_mapa(opcao)

    consultas = {
        "1": (
            "ACADEMIAS",
            """
            SELECT nome, mensalidade, descricao, cidade, rua, complemento, dias_funcionamento, contato_principal, imagem_url
            FROM academias
            """,
        ),
        "2": (
            "ACADEMIAS LIVRES",
            """
            SELECT nome, NULL AS mensalidade, NULL AS descricao, cidade, rua, complemento, NULL AS dias_funcionamento, NULL AS contato_principal, imagem_url
            FROM academias_livres
            """,
        ),
        "3": (
            "QUADRAS",
            """
            SELECT nome, NULL AS mensalidade, NULL AS descricao, cidade, rua, complemento, dias_funcionamento, NULL AS contato_principal, imagem_url
            FROM quadras
            """,
        ),
        "4": (
            "CROSSFITS",
            """
            SELECT nome, mensalidade, descricao, cidade, rua, complemento, dias_funcionamento, contato_principal, imagem_url
            FROM crossfits
            """,
        ),
        "5": (
            "LOJAS",
            """
            SELECT nome, NULL AS mensalidade, NULL AS descricao, cidade, rua, complemento, dias_funcionamento, contato_principal, imagem_url
            FROM lojas
            """,
        ),
    }

    consulta = []

    if opcao in consultas:
        tipo, query = consultas[opcao]
        resultados = executar_comandos(query)
        for r_tupla in resultados:
            r_lista = list(r_tupla)
            r_lista.append(tipo)
            consulta.append(r_lista)
    else:
        for tipo, query in consultas.values():
            resultados = executar_comandos(query)
            for r_tupla in resultados:
                r_lista = list(r_tupla)
                r_lista.append(tipo)
                consulta.append(r_lista)

    return render_template(
        "mapa.html", nome=nome, mapa_html=mapa_html, mensagem=mensagem, consulta=consulta
    )


@app.route("/postagem", methods=["GET"])
@login_required
def postagem():
    return render_template("postagem.html")


@app.route("/fazer_postagem", methods=["POST"])
@login_required
def fazer_postagem():
    imagem = request.files["post_label"]
    descricao = request.form["descricao"]

    resultado = cloudinary.uploader.upload(imagem)
    url_imagem = resultado["secure_url"]
    usuario_id = current_user.id

    query = "INSERT INTO posts(descricao, url_image, usuario_id) VALUES(?, ?, ?)"
    valores = (descricao, url_imagem, usuario_id)
    executar_comandos(query, valores)

    return redirect("/postagem")


if __name__ == "__main__":
    app.run(debug=True)
