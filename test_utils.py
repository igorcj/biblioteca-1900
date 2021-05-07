import pytest
import utils
import core
import database as db
from database import session
import sqlalchemy as sa
import datetime as dt


def test_find_successor():
    IDs = [1, 1, 2, 3, 4]

    with pytest.raises(utils.IDError):
        utils.find_successor(IDs)

    IDs = []
    assert utils.find_successor(IDs) == 1

    IDs = [1, 2, 4, 5, 7, 8, 9]
    assert utils.find_successor(IDs) == 3


def test_basic_inserts():
    db.create_all()

    try:
        a1 = core.Aluno(nome="João", telefone="41984203944",
                        quarto="60", matricula="B41309")
        a2 = core.Aluno(nome="Igor", quarto="74", matricula="B39000")
        a3 = core.Aluno(nome="Biblioteca", quarto="01", matricula="B00000")
        db.session.add_all([a1])
        db.session.commit()

        b1 = core.Livro(ID="0-F-01", titulo="Foo", dono=a1)
        b2 = core.Livro(ID="0-B-01", titulo="Bar", dono=a1)
        b3 = core.Livro(ID="0-F-02", titulo="FooBarr", dono=a3)
        b4 = core.Livro(ID="0-B-02", titulo="Barr", dono=a2)
        db.session.add_all([b1, b2, b3, b4])
        db.session.commit()

    except (sa.exc.IntegrityError):
        assert False


def test_inserts():

    a1 = session.query(core.Aluno).first()

    with pytest.raises(sa.exc.IntegrityError):
        a4 = core.Aluno(nome="Ana", quarto="1974", matricula="B39000")
        session.add(a4)
        session.commit()

    session.rollback()

    with pytest.raises(sa.exc.IntegrityError):
        a5 = core.Aluno(nome="Vitor", quarto="05", matricula="b39000")
        session.add(a5)
        session.commit()

    session.rollback()

    with pytest.raises(sa.exc.IntegrityError):
        b5 = core.Livro(ID="0-A-02", titulo="Parr", dono=a1)
        session.add(b5)
        session.commit()

    session.rollback()

    with pytest.raises(sa.exc.IntegrityError):
        b6 = core.Livro(ID="0 A-1", titulo="Parr", dono=a1)
        session.add(b6)
        session.commit()

    session.rollback()

    with pytest.raises(sa.exc.IntegrityError):
        b6 = core.Livro(ID="A-Z-01", titulo="Parr", dono=a1)
        session.add(b6)
        session.commit()

    session.rollback()


def test_emprestimos():

    utils.add_emprestimo(session=session, st_code="B41309", bk_code="0-F-02")

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


def test_add_aluno():

    utils.add_aluno(session, nome="Welly", matricula="B41300", quarto="66")
    utils.add_aluno(session, nome="Ana", matricula="B41360",
                    quarto="20", telefone="39766554433")

    with pytest.raises(ValueError):
        utils.add_aluno(session, nome="Welly", matricula="B41300", quarto="66")

    with pytest.raises(ValueError):
        utils.add_aluno(session, nome="Welly", matricula="B41300",
                        quarto="66", telefone="41984304955")


def test_add_livro():
    a1 = session.query(core.Aluno).first()

    utils.add_livro(session, categoria=0, titulo="Fantasias do Mar", dono=a1)
    l1 = session.query(core.Livro).filter_by(titulo="Fantasias do Mar").first()
    assert l1 is not None

    with pytest.raises(ValueError):
        utils.add_livro(session, categoria=0,
                        titulo="Fantasias do Mar", dono=a1)

    utils.add_livro(session, categoria=1, titulo="Fantoches do ar", dono=a1)
