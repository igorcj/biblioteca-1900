import os

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Date,
    Column,
    ForeignKey,
)
from sqlalchemy.orm import (
    relationship,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Livro(Base):

    __tablename__ = "livros"

    academico = Column(Boolean, primary_key=True)
    letra = Column(String(1), primary_key=True)
    indice = Column(Integer, primary_key=True)
    titulo = Column(String(40))
    editora = Column(String(30), nullable=True)
    edicao = Column(String(20), nullable=True)
    ano = Column(Integer, nullable=True)
    autor = Column(String(50), nullable=True)
    aluno_id = Column(Integer, ForeignKey("alunos.ID"))

    # Esse dado não é uma coluna, existe apenas em nível de abstração.
    # Quando for feita uma query em um livro, podemos achar seu dono acessando a "coluna" dono
    dono = relationship("Aluno")

    def __repr__(self):
        return f"Livro(titulo={self.titulo})"


class Aluno(Base):

    __tablename__ = "alunos"

    ID = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    telefone = Column(String(11), nullable=True)
    quarto = Column(Integer, nullable=False)
    # Mesma coisa. Não é uma coluna, mas nos permite acessar os livros
    livros = relationship(Livro, backref="alunos")

    def __repr__(self):
        return f"Aluno(nome={self.nome}, quarto={self.nome}, telefone={self.telefone})"
