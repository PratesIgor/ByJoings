<?php
session_start();
include('conexao.php');

$id = mysqli_real_escape_string($conexao, $_POST['id']);
$login = mysqli_real_escape_string($conexao, $_POST['login']);
$email = mysqli_real_escape_string($conexao, $_POST['email']);
$senha = mysqli_real_escape_string($conexao, $_POST['senha']);
$telefone = mysqli_real_escape_string($conexao, $_POST['telefone']);

$sql = "SELECT COUNT(*) AS total FROM usuarios WHERE login = '$usuario'";
$result = mysqli_query($conexao, $sql);
$row = mysqli_fetch_assoc($result);

if($row ['total'] == 1) {
    $_SESSION['usuario_existe'] = true;
    header('Location: cadastro.php');
    exit;
}

$sql = "INSERT INTO usuarios (id, login, email, senha, telefone, data) VALUES ('$id', '$login', '$email', '$senha', '$telefone', NOW())";

if($conexao->query($sql) === TRUE) {
    $_SESSION['status_cadastro'] = true;
}

$conexao->close();

header('Location: cadastro.php');
exit;
?>