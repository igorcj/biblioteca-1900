#!/usr/bin/python3

import cgi
import sys
sys.path.append('/var/www/src')

import aux
import utils
import core

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)

form = cgi.FieldStorage()

aux.open_home()

with Session() as session:
    livros = utils.find(session, core.Livro)
    aux.livros_to_table(livros)

    modal = form.getvalue('modal')

    if modal is not None:
        aux.make_modal(session, modal)

aux.close_home()