#!/usr/bin/python3


home_begin = '''
<html>
<head>
<title>Biblioteca 1900</title>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>
'''




home_end = '''
</table>
</body>
</html>
'''

home_table_item = '''
<tr>
    <td>{}/td>
    <td>{}/td>
    <td>{}/td>
    <td>{}/td>
    <td>{}/td>
    <td>{}/td>
    <td>{}/td>
</tr>
'''



home_page = '''
<h1>Biblioteca 1900</h1>

<div style="position: absolute; top: 10; right: 10;">
<button type="button" onclick="window.location.href='devolucao.py';">
Realizar uma devolução</button>
</div>

<table>
  <tr>
    <th>Título</th>
    <th>Editora</th>
    <th>Edição</th>
    <th>Ano</th>
    <th>Autor</th>
    <th>Disponível</th>
    <th>Dono</th>
  </tr>
'''

# pesquisa_form = '''
# <form action="/index.py">
#   <input type="radio" id="consulta-academico" name="action" value="consulta-a-t">
#   <label for="male">Consultar todos os livros acadêmicos</label><br>
#   <input type="radio" id="consulta-literario" name="action" value="consulta-l-t">
#   <label for="male">Consultar todos os livros literários</label><br>
#   <p></p>
#   <input type="radio" id="consulta-academico" name="action" value="consulta-a-d">
#   <label for="male">Consultar livros acadêmicos disponíveis</label><br>
#   <input type="radio" id="consulta-literario" name="action" value="consulta-l-d">
#   <label for="male">Consultar livros literários disponíveis</label><br>


#   <p></p>

#   <input type="submit" value="Pesquisar">
# </form>
# '''

