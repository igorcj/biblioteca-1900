import os

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Date,
    Column,
    ForeignKey,
    ForeignKeyConstraint
)
from sqlalchemy.orm import (
    relationship,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Livro(Base):

    __tablename__ = "livro"

    # ID
    categoria = Column(Integer, primary_key=True)
    letra = Column(String(1), primary_key=True)
    indice = Column(Integer, primary_key=True)

    # Dados
    titulo = Column(String(40))
    editora = Column(String(30), nullable=True)
    edicao = Column(String(20), nullable=True)
    ano = Column(Integer, nullable=True)
    autor = Column(String(50), nullable=True)
    disponivel = Column(Boolean, default=True)

    # Relações
    aluno_ID = Column(Integer, ForeignKey("aluno.ID"))
    dono = relationship("Aluno", back_populates="livros")

    def __repr__(self):
        return f"Livro(titulo={self.titulo})"


class Aluno(Base):

    __tablename__ = "aluno"

    # ID
    ID = Column(Integer, primary_key=True)

    # Dados
    nome = Column(String(50), nullable=False)
    matricula = Column(String(6), nullable=False)
    telefone = Column(String(11), nullable=True)
    quarto = Column(Integer, nullable=False)

    # Relações
    livros = relationship(Livro, back_populates="dono", cascade="all, delete")

    def __repr__(self):
        return f"Aluno(nome={self.nome}, quarto={self.nome}, telefone={self.telefone})"


class Emprestimo(Base):

    __tablename__ = "emprestimo"

    ID = Column(Integer, primary_key=True)

    # Alunos
    locatario_ID = Column(Integer, ForeignKey("aluno.ID"))

    # Livro
    livro_categoria = Column(Integer)
    livro_letra = Column(String(1))
    livro_indice = Column(Integer)

    # Dados
    data_emp = Column(Date, nullable=False)
    data_dev = Column(Date, nullable=True)

    # Relações
    locatario = relationship("Aluno", foreign_keys=[locatario_ID])
    livro = relationship("Livro", foreign_keys=[
                         livro_categoria, livro_letra, livro_indice])

    __table_args__ = (ForeignKeyConstraint([livro_categoria, livro_letra, livro_indice],
                                           [Livro.categoria, Livro.letra, Livro.indice]), {})

    def __repr__(self):
        return f"Emprestimo(locatario={self.locatario.nome}, livro={self.livro.titulo})"


class Reserva(Base):

    __tablename__ = "reserva"

    ID = Column(Integer, primary_key=True)

    # Aluno
    aluno_ID = Column(Integer, ForeignKey("aluno.ID"))

    # Livro
    livro_categoria = Column(Integer)
    livro_letra = Column(String(1))
    livro_indice = Column(Integer)

    # Data
    data = Column(Date, nullable=False)

    aluno = relationship("Aluno")
    livro = relationship("Livro", foreign_keys=[
                         livro_categoria, livro_letra, livro_indice])

    __table_args__ = (ForeignKeyConstraint([livro_categoria, livro_letra, livro_indice],
                                           [Livro.categoria, Livro.letra, Livro.indice]), {})

    def __repr__(self):
        return f"Reserva(aluno={self.aluno.nome}, livro={self.livro.titulo}, data={self.data.strftime('%d/%m/%Y')})"
