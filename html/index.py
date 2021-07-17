#!/usr/bin/python3

import sys
sys.path.append('/var/www/src')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import utils
import masks

engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)
print("Content-Type: text/html\n\n")


print(masks.test)


# with Session() as session:


