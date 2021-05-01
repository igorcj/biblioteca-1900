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

        e1 = core.Emprestimo(locatario=a1, livro=b3,
                             data_emp=dt.datetime.today())
        r1 = core.Reserva(aluno=a2, livro=b3, data=dt.datetime.today())
        session.add_all([e1, r1])
        session.commit()

    except (sa.exc.IntegrityError):
        assert False


def test_insets():

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

    utils.fazer_emprestimo(session=session, st_code="B41309", bk_code="0-F-02")

    with pytest.raises(ValueError):
        utils.fazer_emprestimo(
            session=session, st_code="b41309", bk_code="0-F-03")

    with pytest.raises(ValueError):
        utils.fazer_emprestimo(
            session=session, st_code="B41309", bk_code="0-F-03")
