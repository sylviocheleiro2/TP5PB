import sqlite3
import requests
from create_bd import *


def obter_dados_api():
    # Função para obter dados da API
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None


def inserir_moeda(conn, descricao):
    # Insere a moeda na tabela moeda
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT codigo FROM moeda WHERE descricao = ?", (descricao,))
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0]
        else:
            cursor.execute(
                "INSERT INTO moeda (descricao) VALUES (?)", (descricao,))
            conn.commit()

            print(f"A moeda '{descricao}' foi inserida com sucesso.")
            return cursor.lastrowid  # Retorna o ID da nova moeda
    except sqlite3.Error as e:
        print(f"Erro ao inserir moeda: {e}")


def inserir_cotacao(conn, codigo_moeda1, codigo_moeda2, valor, data):
    # Insere a cotação na tabela cotacao
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO cotacao (codigo_moeda1, codigo_moeda2, valor, data)
            VALUES (?, ?, ?, ?)
        ''', (codigo_moeda1, codigo_moeda2, valor, data))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir cotação: {e}")
