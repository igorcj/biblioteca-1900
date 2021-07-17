#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src/utils
import masks

engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)
print("Content-Type: text/html\n\n")


print(masks.test)


# with Session() as session:


