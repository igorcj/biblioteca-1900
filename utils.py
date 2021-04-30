import inspect
import datetime
from core import Livro, Aluno, Emprestimo
from string import ascii_uppercase


class IDError(Exception):
    pass


def find_next_ID(session=None, academico: bool = None, letra: str = None) -> int:
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

    if not all([isinstance(academico, bool), isinstance(letra, str), session is not None]):
        raise TypeError("Tipo das variáveis errados")

    letra = letra.upper()

    IDs = []

    livros = session.query(Livro)\
        .filter_by(academico=academico, letra=letra)\
        .all()

    for livro in livros:
        IDs.append(livro.indice)

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


def verify_st_code(st_code: str) -> bool:

    try:
        assert len(st_code) == 6
        _ = int(st_code[1:])
        cond = st_code[0] == 'B'
        assert cond == True

    except (ValueError, TypeError, AssertionError):
        return False

    return True


def verify_bk_code(bk_code: str) -> bool:

    try:
        assert len(bk_code.split("-")) == 3

        categoria, letra, indice = bk_code.split("-")
        categoria, indice = int(categoria), int(indice)

        assert indice != 0

        cond = all([isinstance(categoria, int),
                   letra in ascii_uppercase, isinstance(indice, int)])
        assert cond == True

    except (AssertionError, TypeError, ValueError):
        return False

    return True


def fazer_emprestimo(session=None, st_code: str = None, bk_code: str = None):
    """
    Faz um empréstimo

    Parametros
    ----------
    st_code : string
        string no formato "B00000"

    bk_code : string
        string do ID do livro no formato C-L-00    
    """

    if not (verify_bk_code(bk_code) and verify_st_code(st_code)):
        raise ValueError("session, matrícula ou código do livro inválido(s)")

    categoria, letra, indice = bk_code.split("-")
    letra = letra.upper()
    categoria, indice = int(categoria), int(indice)

    livro = session.query(Livro).filter_by(
        categoria=categoria, letra=letra, indice=indice).first()
    locatario = session.query(Aluno).filter_by(matricula=st_code).first()

    if livro is None:
        raise ValueError("Livro não encontrado")

    if locatario is None:
        raise ValueError("Locatário não encontrado")

    dono = livro.dono
    emprestimo = Emprestimo(dono=dono, locatario=locatario,
                            livro=livro, data_emp=datetime.datetime.today())

    session.add(emprestimo)
    session.commit()

    return True
