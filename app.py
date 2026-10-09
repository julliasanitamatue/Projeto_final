from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_jogador, tabela_partida
from database import Jogador, Time, db_session, Partida

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times = tabela_time.select_quantidade_total()
    jogadores = tabela_jogador.select_quantidade_total()
    partidas = tabela_partida.select_quantidade_total()

    return render_template(
        "clientes.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas,

    )


@app.route("/jogadores")
def listar_jogadores():
    jogadores = tabela_jogador.select_todos()
    return render_template("jogadores.html", jogadores=jogadores)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None
        if not nome:
            flash("Preencha o nome do jogador", "Error")
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash("Preencha o numero da camisa do jogador", "Error")
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash("Preencha a posição do jogador", "Error")
            return redirect(url_for("novo_jogador"))
        if not time_id:
            flash("Preencha o time do jogador", "Error")
            return redirect(url_for("novo_jogador"))
        tabela_jogador.salvar(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos()

    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/times")
def listar_times():
    # buscar todos os time no banco
    # 1- montar o select
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        # 1-pegar os valores digitados no forms
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        turma = request.form.get("turma", "").strip()
        # 2-verificar se foi digitado
        if not nome:
            flash("Preencha o nome do time", "Error")
            return redirect(url_for("novo_time"))
        if not responsavel:
            flash("Preencha o nome do responsavel pelo time", "Error")
            return redirect(url_for("novo_time"))
        if not turma:
            flash("Preencha a turma do time", "Error")
            return redirect(url_for("novo_time"))
        # 3-salvar no banco
        tabela_time.salvar(nome=nome, responsavel=responsavel, turma=turma)
    times = tabela_time.select_todos()

    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todos()

    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        if not time_casa_id:
            flash("Preencha o time da casa", "Error")
            return redirect(url_for("nova_partida"))
        if time_visitante_id == time_casa_id:
            flash("Cadastre times diferentes em uma partida", "Error")
            return redirect(url_for("nova_partida"))

        if not time_visitante_id:
            flash("Preencha o nome do time visitante", "Error")
            return redirect(url_for("nova_partida"))
        if not gols_casa:
            flash("Preencha os gols do time da casa", "Error")
            return redirect(url_for("nova_partida"))
        if not gols_visitante:
            flash("Preencha os gols do time visitante", "Error")
            return redirect(url_for("nova_partida"))
        if not data_partida:
            flash("Preencha a data da partida", "Error")
            return redirect(url_for("nova_partida"))
        tabela_partida.salvar(time_casa_id=int(time_casa_id), time_visitante_id=int(time_visitante_id), gols_casa=int(gols_casa), gols_visitante=int(gols_visitante),data_partida=data_partida)
    times = tabela_time.select_todos()
    partidas = tabela_partida.select_todos()

    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)
