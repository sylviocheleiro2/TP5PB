import sqlite3
from datetime import datetime
from create_bd import *
from consulta import *


def atualizar_cotacoes(conn):
    dados_moeda = obter_dados_api()

    if dados_moeda:
        cursor = conn.cursor()
        data_atual = datetime.now().strftime('%Y-%m-%d')

        # Remover todas as cotações para a data atual antes de inserir novas
        cursor.execute('DELETE FROM cotacao WHERE data = ?', (data_atual,))
        conn.commit()

        for par_moeda, valores in dados_moeda.items():
            try:
                # Usar a função que insere a moeda e retorna o código
                codigo_moeda1 = inserir_moeda(conn, valores['code'])
                codigo_moeda2 = inserir_moeda(conn, valores['codein'])
                valor = float(valores['bid'])

                # Verificar se as moedas são diferentes
                if codigo_moeda1 != codigo_moeda2:
                    # Inserir nova cotação, se não existir
                    cursor.execute('''SELECT COUNT(*) FROM cotacao WHERE codigo_moeda1 = ? AND codigo_moeda2 = ? AND data = ?''',
                                   (codigo_moeda1, codigo_moeda2, data_atual))
                    existe_cotacao = cursor.fetchone()[0]

                    if existe_cotacao == 0:
                        inserir_cotacao(conn, codigo_moeda1,
                                        codigo_moeda2, valor, data_atual)
                    else:
                        print(f"Cotação já existe para o par {valores['code']} e {
                              valores['codein']} no dia {data_atual}.")
                else:
                    print(f"Ignorando a inserção da cotação {valores['code']} para {
                          valores['codein']} (pares iguais).")

            except Exception as e:
                print(f"Erro ao processar a cotação de {
                      valores['code']} para {valores['codein']}: {e}")

        print("Cotações atualizadas com sucesso!")
    else:
        print("Erro ao obter dados da API.")


def listar_moedas(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT codigo, descricao FROM moeda")
        moedas = cursor.fetchall()
        print("\n=== Moedas disponíveis ===")
        for moeda in moedas:
            print(f"Descrição: {moeda[1]}")

    except sqlite3.Error as e:
        print(f"Erro ao listar moedas: {e}")


def consultar_cotacoes(conn):
    listar_moedas(conn)

    data = input("Digite a data (AAAA-MM-DD): ")
    codigo_moeda1 = input(
        "Digite o código da primeira moeda: ").upper()
    codigo_moeda2 = input(
        "Digite o código da segunda moeda: ").upper()

    cursor = conn.cursor()

    # Obter os códigos das moedas
    cursor.execute(
        "SELECT codigo FROM moeda WHERE descricao = ?", (codigo_moeda1,))
    resultado1 = cursor.fetchone()

    cursor.execute(
        "SELECT codigo FROM moeda WHERE descricao = ?", (codigo_moeda2,))
    resultado2 = cursor.fetchone()

    if resultado1 and resultado2:
        # Consulta a cotação diretamente
        cursor.execute('''SELECT valor FROM cotacao 
                          WHERE data = ? AND codigo_moeda1 = ? AND codigo_moeda2 = ?''',
                       (data, resultado1[0], resultado2[0]))
        cotacao = cursor.fetchone()

        if cotacao:
            print(f"Cotação do par {
                  codigo_moeda1}/{codigo_moeda2} em {data}: {cotacao[0]}")
        else:
            print("Cotação não encontrada para a data e moedas fornecidas.")
    else:
        print("Uma ou ambas as moedas não foram encontradas.")
