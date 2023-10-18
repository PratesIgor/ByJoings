import sys
sys.path.append("C:/Users/Jones/Documents/github/ByJoings")
from plataforma.conexao_bd import *
from plataforma.funcoes import *
import platform
import getpass
from datetime import datetime

equipamentos = {}
lista = {}

opcao = opcoes()

while opcao >=1 and opcao <= 8:
    if opcao == 1:
        preencherInventario()
    elif opcao == 2:
        localizarPorNome()
    elif opcao == 3:
        excluirPorSerial(lista)
    elif opcao == 4:
        exibirInventario()
    elif opcao == 5:
        criaNovoArquivoJSON(lista)
    elif opcao == 6:
        usuario = str(input("Digite o login do usuário que deseja consultar: "))
        consulta_usuario_por_login(usuario)
    elif opcao == 7:
        id = input('Digite o ID: ')
        email = input('Digite o e-mail: ')
        usuario = input('Digite o usuario: ')
        senha = input('Digite a senha: ')
        data = datetime.now().isoformat()
        terminal_usuario = (getpass.getuser() + platform.node())
        insere_usuario(id, email, usuario, senha, data, terminal_usuario)
    elif opcao == 8:
        exit()
    opcao = opcoes()


