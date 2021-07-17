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


print('''
<!DOCTYPE html>
<html>
<body>

<h1>The button Element</h1>

<button type="button" onclick="alert('Hello world!')">Click Me!</button>
 
</body>
</html>
''')


# with Session() as session:


