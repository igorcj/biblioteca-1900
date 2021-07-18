from masks import *
import sys
sys.path.append('/var/www/src')
import utils
import core

def livros_to_table(livros):
    print(home_open_table)
    for l in livros:
        atts = ['-' if elem is None else elem
                for elem in [l.ID, l.ID, l.titulo, l.editora, l.edicao,
                l.ano, l.autor, l.disponivel, l.dono.nome]]
        print(home_table_item.format(*atts))
    print(home_close_table)

def open_home():
    print("Content-Type: text/html;charset=UTF-8\n\n")
    print(home_begin)
    print(home_page)

def close_home():
    print(home_end)

def make_modal(session, modal):
    print(home_modal_config)
    d = utils.find(session, core.Livro, ID=modal)[0].disponivel
    content = 'O livro clicado está {}'.format('disponivel' if d else 'emprestado')
    print(home_modal.format(content))
    print(modal_actions)