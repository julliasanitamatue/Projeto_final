from logging import exception

from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.elements import or_


from models import db_session, Equipamentos


def select_todos():
    # 1- Montar o select para listar todos os equipamentos ordenados pelo nome
    equipamento_sql = select(Equipamentos)
    equipamentos = db_session.execute(equipamento_sql).scalars()
    # 2- Executar o select retornando a lista de objetos pura
    equipamentos = db_session.execute(equipamento_sql).scalars().all()
    return equipamentos


def select_quantidade_total():
    # Conta a quantidade total de equipamentos cadastrados no sistema
    equipamento_sql = select(func.count(Equipamentos.id))
    qtd_total = db_session.execute(equipamento_sql).scalar()
    return qtd_total


def salvar(nome_equipamentos, descricao):
    try:
        # Cria a nova instância do equipamento com os atributos enviados
        equipamento_novo = Equipamentos(
            nome_equipamentos=nome_equipamentos,
            descricao=descricao
        )
        db_session.add(equipamento_novo)
        db_session.commit()
        flash("Equipamento adicionado com sucesso", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        print(e)
        flash("Ocorreu um erro ao salvar no banco, tente novamente", "error")
    except Exception as e:
        db_session.rollback()
        print(e)
        flash("Ocorreu um erro inesperado, tente novamente", "error")


def select_por_termo(termo_busca):
    # Busca equipamentos por trechos do Nome OU pelo Código de Patrimônio
    equipamentos_sql = (
        select(Equipamentos)
        .where(
            or_(
                Equipamentos.nome.ilike(f"%{termo_busca}%"),
                Equipamentos.codigo_patrimonio.ilike(f"%{termo_busca}%")
            )
        )
    )
    equipamentos_filtrados = db_session.execute(equipamentos_sql).scalars().all()
    return equipamentos_filtrados
