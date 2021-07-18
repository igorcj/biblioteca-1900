import pytest
import utils
import core
import sqlalchemy as sa
import datetime as dt
from sqlalchemy.orm import sessionmaker

name = "teste.db"
engine = sa.create_engine("sqlite:///{}".format(name))
Session = sessionmaker(bind=engine)
session = Session()
utils.create_all(engine, name, overwrite=True)


def test_find_successor():
    IDs = [1, 1, 2, 3, 4]

    with pytest.raises(utils.IDError):
        utils.find_successor(IDs)

    IDs = []
    assert utils.find_successor(IDs) == 1

    IDs = [1, 2, 4, 5, 7, 8, 9]
    assert utils.find_successor(IDs) == 3


def test_add_aluno():

    utils.add_aluno(
        session,
        nome="Welly",
        matricula="B41300",
        quarto="66"
    )
    utils.add_aluno(
        session,
        nome="Ana",
        matricula="B41360",
        quarto="20",
        telefone="39766554433"
    )
    utils.add_aluno(
        session,
        nome="Joao",
        matricula="B41309",
        quarto="60",
        telefone="41984203944"
    )
    utils.add_aluno(
        session,
        nome="Igor",
        matricula="B40308",
        quarto="79"
    )
    utils.add_aluno(
        session,
        nome="Biblioteca",
        matricula="B00000",
        quarto="00"
    )

    with pytest.raises(ValueError):
        utils.add_aluno(session, nome="Welly", matricula="B41300", quarto="66")

    with pytest.raises(ValueError):
        utils.add_aluno(session, nome="Welly", matricula="B41300",
                        quarto="66", telefone="41984304955")

    with pytest.raises(sa.exc.IntegrityError):
        utils.add_aluno(session, nome="Ronaldo",
                        quarto="1940", matricula="B20394")

    session.rollback()

    with pytest.raises(sa.exc.IntegrityError):
        utils.add_aluno(session, nome="Ronaldo", quarto="40",
                        matricula="B20394", telefone="984399450")

    session.rollback()


def test_add_livro():
    a1 = session.query(core.Aluno).filter_by(nome="Welly").first()
    a2 = session.query(core.Aluno).filter_by(nome="Igor").first()
    a3 = session.query(core.Aluno).filter_by(nome="Joao").first()
    a4 = session.query(core.Aluno).filter_by(nome="Biblioteca").first()

    utils.add_livro(
        session,
        categoria=0,
        titulo="Fantasias Do Mar",
        dono=a1,
        editora="FGV",
        autor="Adam",
        ano=2010
    )
    utils.add_livro(
        session,
        categoria=1,
        titulo="Fantasias Do Mar",
        dono=a1,
        editora="FGV",
        autor="Adam",
        ano=2010
    )
    utils.add_livro(
        session,
        categoria=0,
        titulo="Fantasias Do Mar",
        dono=a2,
        ano=2015
    )
    utils.add_livro(
        session,
        categoria=1,
        titulo="Aventuras",
        dono=a1,
        autor="Adam",
        editora="PUC",
        ano=2010
    )
    utils.add_livro(
        session,
        categoria=0,
        titulo="Aleluia",
        dono=a2,
        autor="Renato",
        editora="PUC",
        ano=1950
    )
    utils.add_livro(
        session,
        categoria=1,
        titulo="Fantasias Do Mar",
        dono=a4,
        autor="Maria Maria",
        ano=1964
    )
    utils.add_livro(
        session,
        categoria=1,
        titulo="Fantoches do ar",
        dono=a1
    )
    utils.add_livro(
        session,
        categoria=0,
        titulo="matemática para leigos",
        dono=a3,
        autor="Descartes"
    )
    utils.add_livro(
        session,
        categoria=0,
        titulo="matemática para pessoas fodas",
        dono=a4,
        autor="Descartes"
    )

    l1 = session.query(core.Livro).filter_by(titulo="Fantasias Do Mar").first()
    assert l1 is not None

    with pytest.raises(ValueError):
        utils.add_livro(
            session,
            categoria=0,
            titulo="Fantasias do Mar",
            dono=a1,
            editora="FGV",
            autor="Adam",
            ano=2010
        )


def test_find_livro():

    l1 = session.query(core.Livro).filter_by(titulo="Fantasias Do Mar").all()
    livros = utils.find(session, core.Livro, titulo="Fantasias Do Mar")
    assert livros == l1

    livros = utils.find(session, core.Livro, autor="Adam")
    assert len(livros) == 3

    livros = utils.find(session, core.Livro, autor="Adam", editora="PUC")
    assert len(livros) == 1

    a1 = session.query(core.Aluno).filter_by(nome="Welly").first()
    assert a1 is not None
    assert a1.ID == 1

    livros = utils.find(session, core.Livro, aluno_ID=a1.ID)
    assert len(livros) == 4


def test_emprestimos():

    b1, b2, *_ = session.query(core.Livro).all()
    a1, a2, *_ = session.query(core.Aluno).all()

    utils.add_emprestimo(session=session, st_code=a1.matricula, bk_code=b1.ID)
    utils.add_emprestimo(session=session, st_code=a2.matricula, bk_code=b2.ID)

    assert b1.disponivel == False
    assert b2.disponivel == False

    with pytest.raises(ValueError):
        utils.add_emprestimo(
            session=session, st_code="b41309", bk_code="0-F-02")

    with pytest.raises(ValueError):
        utils.add_emprestimo(
            session=session, st_code="B41309", bk_code="0-F-03")

    with pytest.raises(ValueError):
        utils.add_emprestimo(
            session=session, st_code=a1.matricula, bk_code=b1.ID)

    utils.devolucao(session=session, bk_code=b1.ID)
    utils.devolucao(session=session, bk_code=b2.ID)

    assert b1.disponivel == True
    assert b2.disponivel == True


def test_reservas():

    a1, a2, a3, *_ = session.query(core.Aluno).all()
    b1, b2, b3, *_ = session.query(core.Livro).all()

    utils.add_reserva(session, a1.matricula, b1.ID)
    utils.add_reserva(session, a2.matricula, b2.ID)

    r1 = utils.check_reserva(session, b1.ID)
    r2 = utils.check_reserva(session, b2.ID)
    assert r1 is not None
    assert r2 is not None

    reserva = utils.check_reserva(session, b3.ID)
    assert reserva is None

    with pytest.raises(ValueError):
        reserva = utils.check_reserva(session, "0-Z-01")
