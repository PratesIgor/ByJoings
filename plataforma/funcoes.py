import json

def opcoes():
        resposta = int(input("----- O que deseja realizar? -----\n" +
                         "<1> - Para Inserir itens \n" +
                         "<2> - Para Pesquisar itens \n" +
                         "<3> - Para Excluir itens \n" +
                         "<4> - Para Listar itens \n" +
                         "<5> - Para Criar novo arquivo JSON \n" +
                         "<6> - Para Consultar usuarios \n" +
                         "<7> - Para Cadastrar novo usuário \n"+
                         "<8> - Para Sair \n"
                         "Digite aqui: "))
        return resposta

def preencherInventario():
    with open(input("Digite o nome do arquivo com o .json que você deseja salvar:"), "r") as bd_json:
        lista = json.load(bd_json)
    resp="S"
    while resp == "S":
        lista[str(input("Equipamento: ")).upper()] = [float(input("Valor: ")),
                                                    int(input("Número Serial: ")),
                                                    str(input("Departamento: ")).upper()]
        resp = input("Digite \"S\"para continuar: ").upper()
    salvaListaJSON(lista)

def exibirInventario():
    with open(str(input("Digite o nome do arquivo com o .json que você deseja salvar: ")), "r") as ar_json:
        inventario = json.load(ar_json)
        for chave, equipamento in inventario.items():
                print(chave + ": " + str(equipamento))

def localizarPorNome():
    busca=input("\nDigite o nome do equipamento que deseja buscar: ").upper()
    equipamentos = []
    with open("bd.txt", "r") as bd:
        for equipamento in bd.readlines():
            equipamentos.append(equipamento.split(str(busca)))
    print(equipamentos)

def depreciarPorNome(lista, porc):
    depreciacao=input("\nDigite o nome do equipamento que será depreciado: ")
    for elemento in lista:
        if depreciacao==elemento[0]:
            print("Valor antigo: ", elemento[1])
            elemento[1] = elemento[1] * (1-porc/100)
            print("Novo valor: ", elemento[1])
            print("")

def excluirPorSerial(lista):
    serial=int(input("\nDigite o serial do equipamento que será excluido: "))
    for elemento in lista:
        if elemento[2]==serial:
            lista.remove(elemento)
    return "Itens excluídos."

def resumirValores(lista):
    valores=[]
    for elemento in lista:
        valores.append(elemento[1])
        if len(valores)>0:
            print("O equipamento mais caro custa: ", max(valores))
            print("O equipamento mais barato custa: ", min(valores))
            print("O total de equipamentos é de: ", sum(valores))

def salvaListaJSON(lista):
    with open(input("Digite o nome do arquivo com o .json que você deseja salvar:"), "w") as bd_json:
       json.dump(lista, bd_json)

def criaNovoArquivoJSON(lista):
    with open(str(input("Digite o nome do arquivo com o .json no final:")), "w") as bd_json:
       json.dump(lista, bd_json)