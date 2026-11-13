from email.utils import format_datetime
from xmlrpc.client import DateTime

from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from models import db_session, Equipamentos, Clientes, Movimentacao



def select_todos():
    EquipamentosOrigem = aliased(Equipamentos)
    EquipamentosDestino = aliased(Equipamentos)

    movimentacoes_sql = (
        select(Movimentacao, Clientes,   EquipamentosOrigem, EquipamentosDestino)
        .join(Clientes, Movimentacao.clientes_id == Clientes.id)
        .outerjoin(EquipamentosOrigem, Movimentacao.equipamentos_origem_id == EquipamentosOrigem.id)
        .outerjoin(EquipamentosDestino, Movimentacao.equipamentos_destino_id == EquipamentosDestino.id)
    )
    movimentacoes = db_session.execute(movimentacoes_sql).all()
    return movimentacoes


def select_quantidade_total():
    movimentacoes_sql = select(func.count(Movimentacao.id))
    qtd_total = db_session.execute(movimentacoes_sql).scalar()
    return qtd_total


def salvar(clientes, equipamentos_destino):
    try:
        clientes_sql = select(Clientes).where(Clientes.id == clientes)
        clientes_resultado = db_session.execute(clientes).scalar_one_or_none()

        if not clientes_resultado:
            flash("cliente nao encontrado", "Error")
            return

        equipamentos_origem_id = clientes_resultado.equipamentos_id

        # validar se o clientes ja pertence  ao equipamentos destino
        if equipamentos_origem_id == equipamentos_destino:
            flash("o cliente ja pertence ao equipamentos", "Error")
            return

        # obter data e hora atual
        data_atual = DateTime.now()

        #atualizar o equipamentos do clientes
        clientes_resultado.equipamentos_id = equipamentos_destino

        movimentacao_nova = Movimentacao(
            clientes_id = int(clientes),
            equipamentos_origem_id = equipamentos_origem_id,
            equipamentos_destino_id =int(equipamentos_destino) ,
            data_movimentacao = data_atual,

        )
        db_session.add(movimentacao_nova)
        db_session.commit()
        flash("movimentacao realizada com sucesso", "Success")
    except SQLAlchemyError as e:
        print(e)
        db_session.rollback()
        flash("ocorreu um erro,tente novamente", "Error")
    except Exception as e:
        print(e)
        db_session.rollback()
        flash("ocorreu um erro,tente novamente", "Error")

