from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET'])
def cadastro_form():
    return render_template('cadastro.html')

# Rota para processar o formulário enviado
@app.route('/cadastro', methods=['POST'])
def cadastro_submit():
    nome = request.form.get('nome')
    nome_usuario = request.form.get('nome_usuario')
    data_nascimento = request.form.get('data_nascimento')
    email = request.form.get('email')
    senha = request.form.get('senha')
    esporte = request.form.get('esporte')

    # Aqui você pode adicionar validação, salvar no banco, etc.
    print(f"Cadastro recebido: {nome}, {nome_usuario}, {data_nascimento}, {email}, {esporte}")

    # Depois redirecione para a página de login, ou outra
    return redirect(url_for('login.html'))

@app.route('/login', methods=['GET'])
def cadastro_form():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_submit():
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    print(f"Login concluído")
    return redirect(url_for('index.html'))

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
