import pytest
import utils
import core
import database as db
from database import session
import sqlalchemy as sa


def test_aluno():
    matriculas = ["b41309", "B4130", "134543", "34354", "B41309d", "B413H5"]

    for matricula in matriculas:
        assert utils.verify_st_code(matricula) == False

    matriculas = ["B41309", "B41303", "B34543"]

    for matricula in matriculas:
        assert utils.verify_st_code(matricula) == True


def test_livro():
    codigos = ["A-F-1", "0 F-1", "0-c-2", "0-F-0"]
    for codigo in codigos:
        assert utils.verify_bk_code(codigo) == False

    codigos = ["1-F-1", "3-H-7"]
    for codigo in codigos:
        assert utils.verify_bk_code(codigo) == True


def test_find_successor():
    IDs = [1, 1, 2, 3, 4]

    with pytest.raises(utils.IDError):
        utils.find_successor(IDs)

    IDs = []
    assert utils.find_successor(IDs) == 1

    IDs = [1, 2, 4, 5, 7, 8, 9]
    assert utils.find_successor(IDs) == 3


def test_insert_aluno():
    db.create_all()

    try:
        a1 = core.Aluno(nome="João", telefone="41984203944",
                        quarto="60", matricula="B41309")
        a2 = core.Aluno(nome="Igor", quarto="74", matricula="B39000")
        a3 = core.Aluno(nome="Biblioteca", quarto="01", matricula="B00000")
        db.session.add_all([a1, a2, a3])
        db.session.commit()

    except (sa.exc.IntegrityError):
        db.session.rollback()
        assert False

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
