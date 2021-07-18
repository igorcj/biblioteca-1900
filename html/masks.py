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


home_page = '''
<h1>Biblioteca 1900</h1>

<div style="position: absolute; top: 10; right: 10;">
<button type="button" onclick="window.location.href='devolucao.py';">
Realizar uma devolução</button>
</div>

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

home_open_table = '''
<table>
  <tr>
    <th>Código</th>
    <th>Título</th>
    <th>Editora</th>
    <th>Edição</th>
    <th>Ano</th>
    <th>Autor</th>
    <th>Disponível</th>
    <th>Dono</th>
  </tr>
'''

home_table_item = '''
<tr id="myBtn" onclick="window.location.href='index.py?modal={}';" style="cursor: pointer;">
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
</tr>
'''

home_close_table = '''</table>'''


home_modal = '''
<style>
body {font-family: Arial, Helvetica, sans-serif;}

/* The Modal (background) */
.modal {
  display: block; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

/* The Close Button */
.close {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
</style>


<div id="myModal" class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span class="close">&times;</span>
    {}
  </div>

</div>

<script>
// Get the modal
var modal = document.getElementById("myModal");


// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
</script>'''


home_end = '''
</body>
</html>
'''