#!/usr/bin/python3


begin = '''
<html>
<head>
  <title>Biblioteca 1900</title>
</head>
<body>
'''

end = '''
</body>
</html>
'''

# main_page = '''
# <h1>Biblioteca 1900</h1>
# <h2>Escolha a operação:</h2>
# <button type="button" onclick="window.location.href='pesquisa.py';">Pesquisa</button>
# '''

main_form = '''
<form action="/index.py">
  <input type="radio" id="consulta-academico" name="action" value="consulta-a-t">
  <label for="male">Consultar todos os livros acadêmicos</label><br>
  <input type="radio" id="consulta-literario" name="action" value="consulta-l-t">
  <label for="male">Consultar todos os livros literários</label><br>
  <p></p>
  <input type="radio" id="consulta-academico" name="action" value="consulta-a-d">
  <label for="male">Consultar livros acadêmicos disponíveis</label><br>
  <input type="radio" id="consulta-literario" name="action" value="consulta-l-d">
  <label for="male">Consultar livros literários disponíveis</label><br>


  <p></p>

  <input type="submit" value="Pesquisar">
</form>
'''