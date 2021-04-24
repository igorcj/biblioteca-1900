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

    __tablename__ = "livro"

    # ID
    academico = Column(Boolean, primary_key=True)
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
    aluno_id = Column(Integer, ForeignKey("aluno.ID"))
    dono = relationship("Aluno", back_populates="livros")

    def __repr__(self):
        return f"Livro(titulo={self.titulo})"


class Aluno(Base):

    __tablename__ = "aluno"

    # ID
    ID = Column(Integer, primary_key=True)

    # Dados
    nome = Column(String(50), nullable=False)
    telefone = Column(String(11), nullable=True)
    quarto = Column(Integer, nullable=False)

    # Relações
    livros = relationship(Livro, back_populates="dono", cascade="all, delete")

    def __repr__(self):
        return f"Aluno(nome={self.nome}, quarto={self.nome}, telefone={self.telefone})"
