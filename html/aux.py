from masks import *

def livros_to_table(livros):
    print(home_open_table)
    for l in livros:
        atts = ['-' if elem is None else elem
                for elem in [l.ID, l.ID, l.titulo, l.editora, l.edicao,
                l.ano, l.autor, l.disponivel, l.dono.nome]]
        print(home_table_item.format(*atts))
    print(home_close_table)
