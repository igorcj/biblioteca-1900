#!/usr/bin/python3

import cgi
import sys
sys.path.append('/var/www/src')

import utils
import masks
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)

print("Content-Type: text/html;charset=UTF-8\n\n")

print(masks.begin)
print(masks.home_page)
print(masks.end)

# form = cgi.FieldStorage()
# searchterm =  form.getvalue('action')

# print(searchterm)

# with Session() as session: