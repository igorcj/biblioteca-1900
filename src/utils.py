import inspect
import datetime
import os

import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker

from core import Livro, Aluno, Emprestimo, Reserva, Base

from string import ascii_uppercase


class IDError(Exception):
    pass


"""
name = "teste.db"
engine = sa.create_engine("sqlite:///{}".format(name))
Session = sessionmaker(bind=engine)
session = Session()
create_all(engine, name=name, overwrite=True, populate=True)
"""


def find_next_ID(session, categoria: int, letra: str) -> int:
    """
    Retorna o menor inteiro disponível para ser usado como índice no ID de um livro

    Parametros
    ----------
    academico : string
    letra : string
    session : sqlalchemy session

    Retorna
    -------
    int
    """

    letra = letra.upper()
    IDs = []
    livros = session.query(Livro).all()

    for livro in livros:
        ID = livro.ID
        if int(ID[0]) == categoria and ID[2] == letra:
            IDs.append(int(ID[4:]))

    return find_successor(IDs)


def find_successor(IDs: list) -> int:
    """
    Retorna o sucessor do menor número cujo sucessor não está na lista
    """

    IDs.sort()

    if len(IDs) == 0:
        return 1

    for pos in range(len(IDs) - 1):

        if IDs[pos] == IDs[pos + 1]:
            raise IDError("Não podem existir dois IDs iguais")

        if IDs[pos] + 1 != IDs[pos + 1]:
            return IDs[pos] + 1

    return IDs[-1] + 1


def add_emprestimo(session, bk_code: str = None, st_code: str = None, reserva: Reserva = None):
    """
    Faz um empréstimo

    Parametros
    ----------
    st_code : string
        string no formato "B00000"

    bk_code : string
        string do ID do livro no formato "C-L-00"    

    reserva : Reserva
        Objeto Reserva referente ao livro, se houver    
    """

    if reserva is not None:

        st_code = reserva.aluno.matricula
        bk_code = reserva.livro.ID

    livro = session.query(Livro).filter_by(ID=bk_code).first()
    if livro is None:
        raise ValueError("Livro não encontrado")

    locatario = session.query(Aluno).filter_by(matricula=st_code).first()
    if locatario is None:
        raise ValueError("Locatário não encontrado")

    emprestado = not livro.disponivel
    if emprestado:
        raise ValueError("Livro emprestado")

    reservado = check_reserva(session, bk_code)

    if reservado != reserva:
        raise ValueError("Livro reservado")

    emprestimo = Emprestimo(locatario=locatario, livro=livro)

    livro.disponivel = False

    session.add(emprestimo)

    if reserva:
        session.delete(reserva)

    session.commit()


def add_aluno(session, **kwargs):
    """
    Adiciona aluno à database
    """

    kwargs["nome"] = kwargs["nome"].title()

    exists = session.query(Aluno).filter(
        sa.or_(Aluno.nome == kwargs["nome"], Aluno.matricula == kwargs["matricula"])).first()

    if exists:
        raise ValueError("Aluno já cadastrado")

    aluno = Aluno(**kwargs)
    session.add(aluno)
    session.commit()


def add_livro(session, categoria: int, titulo: str, dono, **kwargs):
    """
    Adiciona livro à database
    """

    titulo = titulo.title()
    exists = session.query(Livro).filter_by(titulo=titulo, **kwargs).all()
    exists = [l for l in exists if int(l.ID[0]) == categoria]

    if exists:
        raise ValueError("Livro já cadastrado")

    letra = titulo[0]
    num_ID = find_next_ID(session, categoria=categoria, letra=letra)
    ID = f"{categoria}-{letra}-{num_ID:02}"

    livro = Livro(ID=ID, titulo=titulo, dono=dono, **kwargs)
    session.add(livro)
    session.commit()


def add_reserva(session, st_code, bk_code):
    """
    Adiciona reserva à database
    """
    aluno = session.query(Aluno).filter_by(matricula=st_code).all()
    assert len(aluno) == 1

    livro = session.query(Livro).filter_by(ID=bk_code).all()
    assert len(livro) == 1

    reserva = Reserva(aluno=aluno[0], livro=livro[0])
    session.add(reserva)
    session.commit()


def find(session, classe, **kwargs) -> list:
    """
    Retorna os objetos da database correspondentes à query
    """

    if len(kwargs) == 0:
        objetos = session.query(classe).all()

    else:
        objetos = session.query(classe).filter_by(**kwargs).all()

    return objetos


def devolucao(session, bk_code: str):
    """
    Faz a devoluçao do livro
    """

    emprestimo = session.query(Emprestimo).join(
        Livro, Emprestimo.livro).filter(Livro.ID == bk_code).first()

    if emprestimo is None:
        raise ValueError("Emprestimo não encontrado")

    emprestimo.data_dev = datetime.datetime.now()
    emprestimo.livro.disponivel = True


def check_reserva(session, bk_code: str) -> Reserva:
    """
    Checa se há reserva pelo livro. Se tiver, retorna a reserva, senão, retorna None
    """

    bk = session.query(Livro).filter_by(ID=bk_code).first()
    if bk is None:
        raise ValueError("Livro não encontrado")

    reserva = session.query(Reserva, func.min(
        Reserva.data)).filter_by(livro_ID=bk_code).first()
    return reserva[0]


def create_all(engine, name="new.db", overwrite=False, populate=False):
    """
    Recria o banco de dados
    """
    if os.path.exists(name) and overwrite:
        print("Removendo banco atual")
        os.remove(name)

    print("Criando novo banco")
    Base.metadata.create_all(engine)

    if populate:

        Session = sessionmaker(bind=engine)
        session = Session()

        ###########################
        #          ALUNOS         #
        ###########################

        add_aluno(
            session,
            nome="Welly",
            matricula="B41300",
            quarto="66"
        )
        add_aluno(
            session,
            nome="Ana",
            matricula="B41360",
            quarto="20",
            telefone="39766554433"
        )
        add_aluno(
            session,
            nome="Joao",
            matricula="B41309",
            quarto="60",
            telefone="41984203944"
        )
        add_aluno(
            session,
            nome="Igor",
            matricula="B40308",
            quarto="79"
        )
        add_aluno(
            session,
            nome="Biblioteca",
            matricula="B00000",
            quarto="00"
        )

        ###########################
        #          LIVROS         #
        ###########################

        a1 = session.query(Aluno).filter_by(nome="Welly").first()
        a2 = session.query(Aluno).filter_by(nome="Igor").first()
        a3 = session.query(Aluno).filter_by(nome="Joao").first()
        a4 = session.query(Aluno).filter_by(nome="Biblioteca").first()

        add_livro(
            session,
            categoria=0,
            titulo="Fantasias Do Mar",
            dono=a1,
            editora="FGV",
            autor="Adam",
            ano=2010
        )
        add_livro(
            session,
            categoria=1,
            titulo="Aventuras no Vento",
            dono=a1,
            editora="FGV",
            autor="Adam",
            ano=2010
        )
        add_livro(
            session,
            categoria=0,
            titulo="Perdidos em Sao Paulo",
            dono=a2,
            ano=2015
        )
        add_livro(
            session,
            categoria=1,
            titulo="Aventuras",
            dono=a1,
            autor="Adam",
            editora="PUC",
            ano=2010
        )
        add_livro(
            session,
            categoria=0,
            titulo="Aleluia",
            dono=a2,
            autor="Renato",
            editora="PUC",
            ano=1950
        )
        add_livro(
            session,
            categoria=1,
            titulo="Enfim, ferias",
            dono=a4,
            autor="Maria Maria",
            ano=1964
        )
        add_livro(
            session,
            categoria=1,
            titulo="Somos Apenas Marionetes",
            dono=a1
        )
        add_livro(
            session,
            categoria=0,
            titulo="Matematica Para Leigos",
            dono=a3,
            autor="Descartes"
        )
        add_livro(
            session,
            categoria=0,
            titulo="Atirei o Pau no Cachorro",
            dono=a4,
            autor="Dona Xica"
        )

        ###########################
        #        EMPRÉSTIMOS      #
        ###########################

        b1, b2, *_ = session.query(Livro).all()
        a1, a2, *_ = session.query(Aluno).all()

        add_emprestimo(session=session, st_code=a1.matricula, bk_code=b1.ID)
        add_emprestimo(session=session, st_code=a2.matricula, bk_code=b2.ID)

        ###########################
        #         RESERVAS        #
        ###########################

        add_reserva(session, a1.matricula, b1.ID)
        add_reserva(session, a2.matricula, b2.ID)

        session.close()
