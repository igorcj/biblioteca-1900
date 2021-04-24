from core import Livro, Aluno, Emprestimo
import inspect


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

    return find_sucessor(IDs)


def find_sucessor(IDs: list) -> int:
    """
    Retorna o menor número cujo sucessor não está na lista
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
