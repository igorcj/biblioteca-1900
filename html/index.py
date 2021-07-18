#!/usr/bin/python3

import cgi
import sys
sys.path.append('/var/www/src')

import aux
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



with Session() as session:
    livros = utils.find(session, core.Livro)
    aux.livros_to_table(livros)

    modal = form.getvalue('modal')

    if modal is not None:
        print(masks.home_modal)


print(masks.home_end)