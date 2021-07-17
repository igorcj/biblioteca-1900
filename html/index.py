#!/usr/bin/python3

import sys
sys.path.append('/var/www/src')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import utils
import masks

engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)
print("Content-Type: text/html;charset=UTF-8\n\n")


print(masks.begin)

print(masks.main_form)

print(masks.end)


# with Session() as session:




# Turn on debug mode.
import cgi
# import cgitb
# from moldes import *
cgitb.enable()



form = cgi.FieldStorage()
action = form.getvalue('action')
if action != None:
    print(action)
#     if action.startswith('consulta'): consulta(c,action[9]=='a',action[11]=='d')


# else:
#     with open('index.html', 'r') as f:
#         print(f.read())