from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from banco import tabela_clientes, tabela_equipamentos, tabela_ordens, tabela_movimentacao
from sqlalchemy.testing.pickleable import User
from models import Clientes, Equipamentos, OrdemDeServicos, db_session, Usuario
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.secret_key = "matua"
# apenas em momento de criação,em produçao deve ser protegida
app.secret_key = "chave-secreta-interclasse-2026"

# configuração do flask login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "faça login para acessar"


#################################################################

@app.route("/")
@login_required
def index():
    return render_template('index.html')
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# carregar imformações do usuario logado
@login_manager.user_loader
def load_user(user_id):
    return db_session.get(Usuario, int(user_id))

def roles_required(*papeis_permitidos):
# decorator para restringir acesso baseado no papel do usuario logado
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.papel not in papeis_permitidos:
                flash("Acesso negado: Voce nao tem permissão para acessar esta pagina", "danger")
                return redirect(url_for("index"))
            return f(*args,**kwargs)
        return decorated_function
    return decorator

# interface de autenticação
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario_sql = select(Usuario).where(Usuario.email == email)
        usuario_resultado = db_session.execute(usuario_sql).scalar()

        if not usuario_resultado:
            flash("Falha na Autenticação: E-mail não encontrado", "Error")
            return redirect(url_for("login"))

        if usuario_resultado and usuario_resultado.check_password(senha):
            login_user(usuario_resultado)
            return redirect(url_for("index"))
        else:
            flash("falha na autenticação: senha incorreta", "Error")

    return render_template(
        "login.html",
        registro=request.args.get("registro") == "True",

    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not nome and not email and not senha:
            flash("Preencher todos os campos", "Error")
            return redirect(url_for("registro"))

        usuario_sql = select(Usuario).where(Usuario.email == email)
        usuario_email = db_session.execute(usuario_sql).scalar_one_or_none()
        if usuario_email:
            flash("E-mail ja cadastrado")
            return redirect(url_for("registro"))

        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email
            )

            novo_usuario.set_password(senha)
            db_session.add(novo_usuario)
            db_session.commit()
            flash("usuario criado com suceso", "success")
            return redirect(url_for("login"))

        except SQLAlchemyError as e:
            print(f"SQLAlchemyError: {e}")
            flash(f"erro no banco")
            return redirect(url_for("registro"))
        except Exception as e:
            print(f"Erro ao registrar: {e}")
            flash("Erro ao registrar", "Error")
            return render_template("registro.html")

    return render_template("login.html")


@app.route("/nova_movimentacao", methods=["GET", "POST"])
@roles_required('admin')
def nova_movimentacao():
    return render_template("movimentacoes.html")


@app.route("/clientes")
def listar_clientes():
    clientes = tabela_clientes.select_todos()
    return render_template("clientes.html", clientes=clientes)


@app.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    if request.method == "POST":
        # 1 - pegar os valores digitados no form
        nome = request.form.get("nome", "").strip()
        data_clientes = request.form.get("data_clientes")
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        # 2 - verificar se foi digitado
        if not nome:
            flash("preencha o nome", 'error')
            return redirect(url_for("novo_cliente"))
        if not data_clientes:
            flash("preencha a data de nascimento", 'error')
            return redirect(url_for("novo_cliente"))
        if not email:
            flash("preencha seu email", 'error')
            return redirect(url_for("novo_cliente"))
        if not senha:
            flash("preencha sua senha", 'error')
            return redirect(url_for("novo_cliente"))

        tabela_clientes.salvar(nome=nome, data_clientes=data_clientes, senha=senha, email=email)
        flash("Cliente cadastrado com sucesso!", "success")
        return redirect(url_for("listar_clientes"))

    clientes=tabela_clientes.select_todos()
    return render_template("clientes.html",clientes=clientes)

@app.route("/equipamentos")
def listar_equipamentos():
    equipamentos = tabela_equipamentos.select_todos()
    print(equipamentos)
    return render_template("listar_equipamentos.html", equipamentos=equipamentos)


@app.route("/equipamentos/novo", methods=["GET", "POST"])
def novo_equipamento():
    if request.method == "POST":
        # 1 - pegar os valores digitados no form
        nome_equipamentos = request.form.get("nome_equipamentos", "").strip()
        descricao = request.form.get("descricao")

        # 2 - verificar se foi digitado
        if not nome_equipamentos:
            flash("preencha o nome", 'error')
            return redirect(url_for("novo_equipamento"))

        if not descricao:
            flash("preencha a descrição", 'error')
            return redirect(url_for("novo_equipamento"))

        # 3 - Salvar no banco de dados
        tabela_equipamentos.salvar(nome_equipamentos=nome_equipamentos, descricao=descricao)
        flash("Equipamento cadastrado com sucesso!", "success")

    return render_template("equipamentos.html")


@app.route("/ordens")
def listar_ordens():
    ordens_sql = select(
        OrdemDeServicos.id,
        OrdemDeServicos.id_clientes,
        OrdemDeServicos.descricao
    ).join(Clientes, OrdemDeServicos.id_clientes == Clientes.id)

    ordens = db_session.execute(ordens_sql).all()
    return render_template("ordens.html", ordens=ordens)


@app.route("/ordens/nova", methods=["GET", "POST"])
def nova_ordens():
    if request.method == "POST":
        nome_pessoa = request.form.get("nome_pessoa_id")
        equipamento = request.form.get("equipamento_id")
        descrição = request.form.get("descrição") or 0

        if not nome_pessoa:
            flash("preencha o nome_pessoa", 'error')
            return redirect(url_for("nova_ordens"))
        if not equipamento:
            flash("preencha o equipamento", 'error')
            return redirect(url_for("nova_ordens"))
        if not descrição:
            flash("preencha a descrição", 'error')
            return redirect(url_for("nova_ordens"))

        # 3 - salvar no banco
        tabela_ordens.salvar(nome_pessoa=nome_pessoa, equipamento=equipamento, descrição=descrição)
        flash("Ordem de serviço aberta com sucesso!", "success")
        return redirect(url_for("listar_ordens"))

    ordens = tabela_ordens.select_todos()
    clientes = tabela_clientes.select_todos()
    return render_template("ordens.html", ordens=ordens, cliente=clientes)


@app.route("recursos/novo", methods=["GET", "POST"])
def novo_recursos


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5001)
