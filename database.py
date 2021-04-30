import sqlalchemy as sa
import os
import utils

from core import Livro, Aluno, Emprestimo, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///new.db")
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":

    if os.path.exists("new.db"):
        os.remove("new.db")
    Base.metadata.create_all(engine)

"""
python -i database.py

# Criando objetos Aluno
a1 = Aluno(nome="João", telefone=41984203944, quarto=60, matricula="B41309")
a2 = Aluno(nome="Igor", quarto=74, matricula="B39000")
a3 = Aluno(nome="Biblioteca", quarto=0, matricula="B00000")

# Criando objetos Livro
b1 = Livro(categoria=0, letra="F", indice=1, titulo="Foo", dono=a1) # Quem é o dono do livro? O Aluno a1
b2 = Livro(categoria=0, letra="B", indice=1, titulo="Bar", dono=a1)
b3 = Livro(categoria=0, letra="F", indice=2, titulo="FooBarr", dono=a2)

session.add_all([a1, a2, b1, b2, b3])
# session.rollback() Cancela tudo até o último commit
session.commit() # Realiza as operações. Aqui, os dados já estão no banco de dados

alunos = session.query(Aluno)
print(alunos[0])
livros_a1 = alunos[0].livros # Objetos da classe Livro! São os objetos mesmo, como definidos em core.py
print(livros_a1[0].titulo)

b_foo = session.query(Livro).filter(Livro.titulo == "Foo").all() # O método filter exige que façamos um "fetch"
print(b_foo[0].dono) # Dono do livro foo
print(b_foo[0].dono.livros[0].dono.livros[0].dono)




"""
