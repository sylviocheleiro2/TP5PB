from crud import *
from create_bd import *
from cotacao_aleatoria import *
from consulta import *


def exibir_menu():
    print("\n==== Menu de Opções ====")
    print("1. Atualizar cotações da API")
    print("2. Consultar cotações de um dia especifico (gerado aleatoriamente na opção 3)")
    print("3. Criar cotações aleatorias")
    print("4. Deletar cotações")
    print("5. Sair...")
    return input("\nEscolha uma opção: ")


def opcao():
    conn = criar_conexao()
    criar_tabelas(conn)

    while True:
        opcao = exibir_menu()
        if opcao == '1':
            atualizar_cotacoes(conn)
        elif opcao == '2':
            consultar_cotacoes(conn)
        elif opcao == '3':
            criar_cotacoes_aleatorias(conn)
        elif opcao == '4':
            deletar_cotacoes_aleatorias(conn)
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

    conn.close()


opcao()
