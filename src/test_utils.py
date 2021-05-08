import pytest
import utils
import core
import database as db
from database import session
import sqlalchemy as sa
import datetime as dt

db.create_all()


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
        nome="João",
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
    a1 = session.query(core.Aluno).filter_by(nome="welly").first()
    a2 = session.query(core.Aluno).filter_by(nome="igor").first()
    a3 = session.query(core.Aluno).filter_by(nome="joão").first()
    a4 = session.query(core.Aluno).filter_by(nome="biblioteca").first()

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
    livros = utils.find_livro(session, titulo="Fantasias Do Mar")
    assert livros == l1

    livros = utils.find_livro(session, autor="Adam")
    assert len(livros) == 3

    livros = utils.find_livro(session, autor="Adam", editora="PUC")
    assert len(livros) == 1

    a1 = session.query(core.Aluno).filter_by(nome="welly").first()
    assert a1 is not None
    assert a1.ID == 1

    livros = utils.find_livro(session, aluno_ID=a1.ID)
    assert len(livros) == 4


def test_emprestimos():

    utils.add_emprestimo(session=session, st_code="B41309", bk_code="0-F-02")
    # utils.add_emprestimo(session=session)

    test_bk = session.query(core.Livro).filter_by(
        ID="0-F-02").first()
    disp = test_bk.disponivel

    assert disp == False

    with pytest.raises(ValueError):
        utils.add_emprestimo(
            session=session, st_code="b41309", bk_code="0-F-02")

    with pytest.raises(ValueError):
        utils.add_emprestimo(
            session=session, st_code="B41309", bk_code="0-F-03")

    utils.devolucao(session=session, bk_code="0-F-02")

    disp = test_bk.disponivel

    assert disp == True


def test_reservas():

    a = session.query(core.Aluno).all()
    a1 = a[0]
    a2 = a[1]
    bs = session.query(core.Livro).all()
    b1 = bs[0]
    b2 = bs[1]
    b3 = bs[2]

    r1 = core.Reserva(aluno=a1, livro=b1)
    r2 = core.Reserva(aluno=a2, livro=b2)
    r3 = core.Reserva(aluno=a1, livro=b2)

    session.add_all([r1, r2, r3])
    session.commit()

    reserva = utils.check_reserva(session, b2.ID)
    assert reserva == r2

    reserva = utils.check_reserva(session, b1.ID)
    assert reserva == r1

    reserva = utils.check_reserva(session, b3.ID)
    assert reserva == None

    with pytest.raises(ValueError):
        reserva = utils.check_reserva(session, "0-Z-01")
