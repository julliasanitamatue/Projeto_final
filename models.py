from flask_login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime,func,engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

engine=create_engine("mysql+pymysql://matua:senaisp@10.135.232.14:3306/banco_projeto_final")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class Clientes(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    data_clientes = Column(DateTime, nullable=False)
    email = Column(String(50), nullable=False)
class Equipamentos(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_equipamentos = Column(String(50), nullable=False)
    descricao = Column(String(250), nullable=False)
    equipamento_criado_em = Column(DateTime, nullable=False, server_default=func.now())


class OrdemDeServicos(Base):
    __tablename__ = "ordem_de_servicos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    id_clientes = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    ordem_criado_em = Column(DateTime, nullable=False, server_default=func.now())
    nome_cliente = Column(String(50), nullable=False)
    descricao = Column(String(250))
    responsavel = Column(String(50), nullable=False)


class OrdemCadastrada(Base):
    __tablename__ = "ordem_cadastrada"

    id = Column(Integer, primary_key=True, autoincrement=True)

    id_ordem_de_servico = Column(Integer, ForeignKey('ordem_de_servicos.id'), nullable=False)

    id_equipamentos = Column(Integer, ForeignKey('equipamentos.id'), nullable=False)



class Movimentacao(Base):
    __tablename__ = "movimentacoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    clientes_id = Column(Integer, ForeignKey("clienteses.id",ondelete="SET NULL"))
    equipamentos_origem_id = Column(Integer, ForeignKey("equipamentoss.id",ondelete="SET NULL"))
    equipamentos_destino_id = Column(Integer, ForeignKey("equipamentoss.id",ondelete="SET NULL"))
    data_movimentacao = Column(DateTime)

    def __repr__(self):
        return f"<Movimentacao: {self.clientes_id}>"



class Usuario(Base, UserMixin):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(120),unique=True,nullable=False)
    papel = Column(String(50),default="usuario",nullable=False)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime,server_default=func.now())
    atualizado_em = Column (DateTime, onupdate=func.now())

    #senha
    def set_password(self,password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.senha_hash,password)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")