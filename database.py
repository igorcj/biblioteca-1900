import sqlalchemy as sa
import os
import utils
import datetime as dt

from core import Livro, Aluno, Emprestimo, Reserva, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)
session = Session()


def create_all():
    if os.path.exists("new.db"):
        os.remove("new.db")
    Base.metadata.create_all(engine)


if __name__ == "__main__":

    create_all()

    a1 = Aluno(nome="João", telefone="41984203944",
               quarto="60", matricula="B41309")
    a2 = Aluno(nome="Igor", quarto="74", matricula="B39000")
    a3 = Aluno(nome="Biblioteca", quarto="01", matricula="B00000")

    b1 = Livro(ID="0-F-01", titulo="Foo", dono=a1)
    b2 = Livro(ID="0-B-01", titulo="Bar", dono=a1)
    b3 = Livro(ID="0-F-02", titulo="FooBarr", dono=a3)

    session.add_all([a1, a2, b1, b2, b3])
    session.commit()

    e1 = Emprestimo(locatario=a1, livro=b3, data_emp=dt.datetime.today())
    r1 = Reserva(aluno=a2, livro=b3, data=dt.datetime.today())
    session.add_all([e1, r1])
    session.commit()
