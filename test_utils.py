import pytest
import utils as u


def test_aluno_errado():
    matriculas = ["b41309", "B4130", "134543", "34354", "B41309d", "B413H5"]

    for matricula in matriculas:
        assert u.verify_st_code(matricula) == False


def test_aluno_certo():
    matriculas = ["B41309", "B41303", "B34543"]

    for matricula in matriculas:
        assert u.verify_st_code(matricula) == True


def test_livro_errado():
    codigos = ["A-F-1", "0 F-1", "0-c-2", "0-F-0"]
    for codigo in codigos:
        assert u.verify_bk_code(codigo) == False


def test_livro_certo():
    codigos = ["1-F-1", "3-H-7"]
    for codigo in codigos:
        assert u.verify_bk_code(codigo) == True


def test_find_successor():
    IDs = [1, 1, 2, 3, 4]

    with pytest.raises(u.IDError):
        u.find_successor(IDs)

    IDs = []
    assert u.find_successor(IDs) == 1

    IDs = [1, 2, 4, 5, 7, 8, 9]
    assert u.find_successor(IDs) == 3
