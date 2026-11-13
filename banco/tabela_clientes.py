from logging import exception

from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.elements import or_

from models import db_session, Clientes


def select_todos():
    # 1- montar o select para listar todos os clientes ordenados pelo nome
    cliente_sql = select(Clientes)
    clientes = db_session.execute(cliente_sql).scalars()




    return clientes
    # 2- executar o select
    todos_clientes = db_session.execute(cliente_sql).scalars().all()
    return todos_clientes


def select_quantidade_total():
    cliente_sql = select(func.count(Clientes.id))
    qtd_total = db_session.execute(cliente_sql).scalar()
    return qtd_total


def salvar(nome, email,data_clientes,senha):
    try:
        clientenovo = Clientes(
            nome=nome,
            email=email,
            data_clientes=data_clientes,
            senha=senha
        )
        db_session.add(clientenovo)
        db_session.commit()
        flash("Cliente adicionado com sucesso", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro ao salvar no banco, tente novamente", "error")
        print(e)

    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro inesperado, tente novamente", "error")
        print(e)

def select_por_termo(termo_busca):
    # Busca clientes que tenham o termo enviado no Nome OU no Email
    clientes_sql = (
        select(Clientes)
        .where(
            or_(
                Clientes.nome.ilike(f"%{termo_busca}%"),
                Clientes.email.ilike(f"%{termo_busca}%")
            )
        )
    )
    clientes_filtrados = db_session.execute(clientes_sql).scalars().all()
    return clientes_filtrados


# Exemplo de teste: buscando clientes que tenham "Silva" no nome ou email
print(select_por_termo("Silva"))
