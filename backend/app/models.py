from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)

class Escola(Base):
    __tablename__ = 'escolas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

class Turma(Base):
    __tablename__ = 'turmas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    escola_id = Column(Integer, ForeignKey('escolas.id'))
    escola = relationship('Escola')

class ContaContabil(Base):
    __tablename__ = 'contas_contabeis'
    id = Column(Integer, primary_key=True)
    descricao = Column(String)

class Lancamento(Base):
    __tablename__ = 'lancamentos'
    id = Column(Integer, primary_key=True)
    valor = Column(Integer)
    conta_id = Column(Integer, ForeignKey('contas_contabeis.id'))
    conta = relationship('ContaContabil')

class Atividade(Base):
    __tablename__ = 'atividades'
    id = Column(Integer, primary_key=True)
    descricao = Column(String)

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    comentario = Column(String)