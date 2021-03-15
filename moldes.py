abre_tabela = '''\
<!DOCTYPE html>
<html>
<head>
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

literarios_header = "<h2>Livros Literários</h2>"

academicos_header = "<h2>Livros Acadêmicos</h2>"

tabela_header = '''\
<table>
  <tr>
    <th>Código</th>
    <th>Título</th>
    <th>Autor</th>
    <th>Editora</th>
    <th>Ano</th>
    <th>Dono</th>
    <th>Status</th>
  </tr>
'''

tabela_item = '''\
<tr>
    <td>{codigo}</td>
    <td>{titulo}</td>
    <td>{autor}</td>
    <td>{editora}</td>
    <td>{ano}</td>
    <td>{dono}</td>
    <td>{status}</td>
</tr>
'''

fecha_tabela = '''\
</table>
<p></p>
<form action="/index.py">
      <input type="submit" value="Página Inicial">
</form>
</body>
</html>
'''
