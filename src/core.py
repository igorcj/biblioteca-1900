import os
import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    CheckConstraint
)
from sqlalchemy.orm import (
    relationship,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Livro(Base):

    __tablename__ = "livro"

    # ID
    ID = Column(String(6), primary_key=True)

    # Dados
    titulo = Column(String(40))
    editora = Column(String(30), nullable=True)
    edicao = Column(String(20), nullable=True)
    ano = Column(Integer, nullable=True)
    autor = Column(String(50), nullable=True)
    disponivel = Column(Boolean, default=True)

    # Checks
    __table_args__ = (
        CheckConstraint(
            r"ID REGEXP('^\d-\w-\d\d$')", name="check_ID"),
        CheckConstraint(
            r"SUBSTR(ID,3,1) = SUBSTR(titulo,1,1)", name="check_titulo"),
    )

    # Relações
    aluno_ID = Column(Integer, ForeignKey("aluno.ID"), nullable=False)
    dono = relationship("Aluno", back_populates="livros")

    def __repr__(self):
        return f"Livro(titulo=\"{self.titulo}\")"

    def __eq__(self, other):

        return all(
            self.titulo == other.titulo,
            self.editora == other.editora,
            self.edicao == other.edicao,
            self.ano == other.ano,
            self.autor == other.autor,
        )


class Aluno(Base):

    __tablename__ = "aluno"

    # ID
    ID = Column(Integer, primary_key=True)

    # Dados
    nome = Column(String(50), nullable=False)
    matricula = Column(String(6), nullable=False)
    telefone = Column(String(11), nullable=True)
    quarto = Column(String(2), nullable=False)

    # Relações
    livros = relationship(Livro, back_populates="dono", cascade="all, delete")

    # Checks
    __table_args__ = \
        (CheckConstraint(
            r"matricula REGEXP('^B(\d){5}$')", name="check_matricula"),
         CheckConstraint(
            r"quarto REGEXP('^(\d){2}$')", name="check_quarto"),
         CheckConstraint(
            r"telefone REGEXP('^\d{11}$')", name="check_telefone"),
         )

    def __repr__(self):
        return f"Aluno(nome=\"{self.nome}\", quarto={self.quarto}, telefone=\"{self.telefone}\")"


class Emprestimo(Base):

    __tablename__ = "emprestimo"

    ID = Column(Integer, primary_key=True)

    # Alunos
    locatario_ID = Column(Integer, ForeignKey("aluno.ID"))

    # Livro
    livro_ID = Column(String(6), ForeignKey("livro.ID"))

    # Dados
    data_emp = Column(DateTime, default=datetime.datetime.now)
    data_dev = Column(DateTime, nullable=True)

    # Relações
    locatario = relationship("Aluno", foreign_keys=[locatario_ID])
    livro = relationship("Livro")

    def __repr__(self):
        return f"Emprestimo(locatario=\"{self.locatario.nome}\", livro=\"{self.livro.titulo}\")"


class Reserva(Base):

    __tablename__ = "reserva"

    ID = Column(Integer, primary_key=True)

    # Aluno
    aluno_ID = Column(Integer, ForeignKey("aluno.ID"))

    # Livro
    livro_ID = Column(String(6), ForeignKey("livro.ID"))

    # Data
    data = Column(DateTime, default=datetime.datetime.now)

    aluno = relationship("Aluno")
    livro = relationship("Livro")

    def __repr__(self):
        return f"Reserva(aluno=\"{self.aluno.nome}\", livro=\"{self.livro.titulo}\", data={self.data.strftime('%d/%m/%Y')})"
