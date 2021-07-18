#!/usr/bin/python3

import cgi
import sys
sys.path.append('/var/www/src')

import utils
import masks
import core
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)
form = cgi.FieldStorage()

print("Content-Type: text/html;charset=UTF-8\n\n")

print(masks.home_begin)
print(masks.home_page)
print(masks.home_open_table)




# print(searchterm)

with Session() as session:
    livros = utils.find(session, core.Livro)


    for l in livros:
        print(masks.home_table_item.format(
            *['-' if elem is None else elem
            for elem in [l.ID, l.ID, l.titulo, l.editora, l.edicao,
            l.ano, l.autor, l.disponivel, l.dono.nome]]))


print(masks.home_close_table)

modal = form.getvalue('modal')

if modal is not None:
    print("Abrir modal {}".format(modal))
    print(masks.home_modal)


print(masks.home_end)