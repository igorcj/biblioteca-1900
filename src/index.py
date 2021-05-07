#!/usr/bin/python

# Turn on debug mode.
import cgi
import cgitb
from moldes import *
cgitb.enable()


# Print necessary headers.
print("Content-Type: text/html; charset=utf-8")
print()

# Connect to the database.
import pymysql
conn = pymysql.connect(
    db='biblioteca',
    user='root',
    passwd='#IGt361320',
    host='localhost')
c = conn.cursor()

# # Insert some example data.
# c.execute("INSERT INTO numbers VALUES (1, 'One!')")
# c.execute("INSERT INTO numbers VALUES (2, 'Two!')")
# c.execute("INSERT INTO numbers VALUES (3, 'Three!')")
# conn.commit()

# # Print the contents of the database.
# c.execute("SELECT * FROM numbers")
# print([(r[0], r[1]) for r in c.fetchall()])

def consulta(c,acad,status):
    filt = ''
    if status: filt = 'where status = "Disponível"'
    query = 'select * from (select letra,indice,titulo,autor,editora,ano,nome,\
        IF((concat(academico,letra,indice) not in (select concat(livros_academico,livros_letra,livros_indice)\
            from emprestimos where data_dev is NULL)), "Disponível", "Emprestado")\
        as status from livros inner join alunos on livros.alunos_ID = alunos.ID where academico = {}) as consult {};'.format(acad,filt)
    c.execute(query)
    print(abre_tabela)
    if acad: print(academicos_header)
    else: print(literarios_header)
    print(tabela_header)
    for e in c.fetchall():
        print(tabela_item.format(codigo = e[0]+str(e[1]), titulo = e[2], autor = e[3], editora = e[4], ano = e[5], dono = e[6], status = e[7]))
    print(fecha_tabela)



form = cgi.FieldStorage()
action = form.getvalue('action')
if action != None:
    if action.startswith('consulta'): consulta(c,action[9]=='a',action[11]=='d')


else:
    with open('index.html', 'r') as f:
        print(f.read())


#IF((concat(academico,letra,indice) not in (select concat(livros_academico,livros_letra,livros_indice) from emprestimos where data_dev is NULL)), "Disponível", "Emprestado") as status