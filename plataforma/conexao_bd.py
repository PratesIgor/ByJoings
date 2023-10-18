import mysql.connector

usuarios = {}

def conectaBD ():
    meubd = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'equipamentos'
        )

    cursor = meubd.cursor()
    return meubd, cursor

def consulta_usuario_por_login(usuario):
    meubd, cursor = conectaBD()

    query = "SELECT usuario, email, senha FROM USUARIOS WHERE usuario = %s"
    cursor.execute(query, (usuario,))

    login = cursor.fetchone()

    meubd.close()

    if login is not None:
        print("Resultado da consulta:", login)
        return login
    else:
        print("Nenhum usuário encontrado com o usuario fornecido.")
        return None  # Retorna None em vez de uma mensagem de aviso


def insere_usuario(id, email, usuario, senha, data, terminal_usuario):
    try:
        # Conecta ao banco de dados
        meubd = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='equipamentos'
        )
        
        cursor = meubd.cursor()

        # Instrução SQL para inserir um novo usuário
        sql = "INSERT INTO usuarios (id, email, usuario, senha, data, terminal_usuario) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (id, email, usuario, senha, data, terminal_usuario)

        cursor.execute(sql, val)

        # Confirma a inserção no banco de dados
        meubd.commit()

        print("Usuário inserido com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    finally:
        # Fecha a conexão com o banco de dados
        meubd.close()

