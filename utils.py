import inspect
import datetime
from core import Livro, Aluno, Emprestimo, Reserva
from string import ascii_uppercase
from sqlalchemy.sql.expression import func


class IDError(Exception):
    pass


def find_next_ID(session=None, categoria: int = None, letra: str = None) -> int:
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

    if not all([isinstance(categoria, int), isinstance(letra, str), session is not None]):
        raise TypeError("Tipo das variáveis errados")

    letra = letra.upper()

    IDs = []

    livros = session.query(Livro).all()

    for livro in livros:
        ID = livro.ID
        if ID[0] == categoria and ID[2] == letra:
            IDs.append(ID)

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


def emprestimo(session, st_code: str, bk_code: str):
    """
    Faz um empréstimo

    Parametros
    ----------
    st_code : string
        string no formato "B00000"

    bk_code : string
        string do ID do livro no formato "C-L-00"    
    """

    livro = session.query(Livro).filter_by(ID=bk_code).first()
    locatario = session.query(Aluno).filter_by(matricula=st_code).first()

    if livro is None:
        raise ValueError("Livro não encontrado")

    if locatario is None:
        raise ValueError("Locatário não encontrado")

    emprestimo = Emprestimo(locatario=locatario, livro=livro)

    livro.disponivel = False

    session.add(emprestimo)
    session.commit()


def devolucao(session, bk_code: str):
    """
    Faz a devoluçao do livro
    """

    emprestimo = session.query(Emprestimo).join(
        Livro, Emprestimo.livro).filter(Livro.ID == bk_code).first()

    if emprestimo is None:
        raise ValueError("Emprestimo não encontrado")

    emprestimo.data_dev = datetime.datetime.today()
    emprestimo.livro.disponivel = True


def checar_reserva(session, bk_code: str):
    """
    Checa se há reserva pelo livro. Se tiver, retorna a reserva, senão, retorna None
    """

    bk = session.query(Livro).filter_by(ID=bk_code).first()
    if bk is None:
        raise ValueError("Livro não encontrado")

    reserva = session.query(Reserva, func.min(
        Reserva.data)).filter_by(livro_ID=bk_code).first()
    return reserva[0]
