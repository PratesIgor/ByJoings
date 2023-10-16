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

def consulta_usuario_por_login(login):
    meubd, cursor = conectaBD()

    query = "SELECT * FROM USUARIOS WHERE login = %s"
    cursor.execute(query, (login,))

    usuario = cursor.fetchone()

    meubd.close()

    return usuario

def insere_usuario(id, email, login, senha, data, terminal_usuario):
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
        sql = "INSERT INTO usuarios (id, email, login, senha, data, terminal_usuario) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (id, email, login, senha, data, terminal_usuario)

        cursor.execute(sql, val)

        # Confirma a inserção no banco de dados
        meubd.commit()

        print("Usuário inserido com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    finally:
        # Fecha a conexão com o banco de dados
        meubd.close()

