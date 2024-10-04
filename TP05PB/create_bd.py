import sqlite3


def criar_conexao():
    return sqlite3.connect('moedas.db')


def criar_tabelas(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('DROP TABLE IF EXISTS moeda')
        cursor.execute('DROP TABLE IF EXISTS cotacao')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS moeda (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT UNIQUE
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cotacao (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_moeda1 INTEGER,
            codigo_moeda2 INTEGER,
            valor FLOAT,
            data DATE,
            FOREIGN KEY(codigo_moeda1) REFERENCES moeda(codigo),
            FOREIGN KEY(codigo_moeda2) REFERENCES moeda(codigo)
        )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
