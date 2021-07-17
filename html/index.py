from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import utils
import masks

engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)


print(masks.test)


# with Session() as session:


