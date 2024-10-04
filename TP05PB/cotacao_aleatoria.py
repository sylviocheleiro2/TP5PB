import sqlite3
import random
from datetime import datetime, timedelta
from consulta import inserir_cotacao


def criar_cotacoes_aleatorias(conn):
    # Dicionário de moedas com seus respectivos códigos
    moedas = {
        'USD': 1,  # Código 1 para USD
        'BRL': 2,  # Código 2 para BRL
        'EUR': 3,  # Código 3 para EUR
        'BTC': 4   # Código 4 para BTC
    }

    # Criando um intervalo de dias para inserir dados
    hoje = datetime.now()
    dias_para_criar = 10  # Por exemplo, os últimos 10 dias
    primeira_data = (hoje - timedelta(days=dias_para_criar - 1)
                     ).strftime('%Y-%m-%d')
    ultima_data = hoje.strftime('%Y-%m-%d')

    total_cotacoes = 0

    for i in range(dias_para_criar):
        # Calcula a data de hoje menos i dias
        data = (hoje - timedelta(days=i)).strftime('%Y-%m-%d')

        # Gerar valores aleatórios para as cotações
        valor_usd_brl = round(random.uniform(4.5, 5.5),
                              2)  # Valor entre 4.5 e 5.5
        valor_eur_brl = round(random.uniform(5.0, 6.0),
                              2)  # Valor entre 5.0 e 6.0
        # Valor entre 200,000 e 300,000
        valor_btc_brl = round(random.uniform(200000, 300000), 2)

        # Inserir cotações no banco de dados
        inserir_cotacao(conn, moedas['USD'],
                        moedas['BRL'], valor_usd_brl, data)
        inserir_cotacao(conn, moedas['EUR'],
                        moedas['BRL'], valor_eur_brl, data)
        inserir_cotacao(conn, moedas['BTC'],
                        moedas['BRL'], valor_btc_brl, data)

        total_cotacoes += 3  # 3 cotações por dia (USD, EUR, BTC)

    print(f"\nForam criadas {total_cotacoes} cotações.")
    print(f"Primeiro dia: {primeira_data}")
    print(f"Último dia: {ultima_data}\n")


def deletar_cotacoes_aleatorias(conn):
    cursor = conn.cursor()
    try:
        # Remover todas as cotações da tabela cotacao
        cursor.execute('DELETE FROM cotacao')
        conn.commit()
        print("Todas as cotações foram removidas com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao deletar cotações: {e}")
