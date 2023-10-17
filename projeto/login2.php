<?php
define('HOST','127.0.0.1:8090');
define('USUARIO', 'root');
define('SENHA', 'projetinho');
define('DB', 'projeto');

$conexao = mysql_connect(HOST, USUARIO, SENHA, DB) or die('Não foi possível realizar o login.');


?>
