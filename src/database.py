import sqlite3
import os

# Define o nome do arquivo do banco de dados
DB_NAME = 'caixa.db'
# Define o caminho completo para o banco de dados dentro da pasta 'data'
# Se a pasta 'data' não existir, ela será criada.
DB_PATH = os.path.join('data', DB_NAME)

def get_db_connection():
    """
    Função para obter uma conexão com o banco de dados SQLite.
    Se o diretório 'data' não existir, ele será criado.
    """
    # Garante que o diretório 'data' exista
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Permite acessar colunas como dicionário (ex: row['nome'])
    return conn

def create_tables():
    """
    Cria as tabelas necessárias no banco de dados se elas não existirem.
    Usamos IF NOT EXISTS para evitar erros caso as tabelas já existam.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela: Produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            preco REAL NOT NULL,
            tipo_unidade TEXT NOT NULL, -- 'UNIDADE' ou 'KG'
            estoque INTEGER NOT NULL DEFAULT 0
        );
    """)

    # Tabela: Vendas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL, -- Formato YYYY-MM-DD HH:MM:SS
            total REAL NOT NULL,
            status TEXT NOT NULL, -- 'FINALIZADA', 'CANCELADA'
            tipo_pagamento TEXT -- 'DINHEIRO', 'CARTAO', 'PIX'
        );
    """)

    # Tabela: Itens_Venda
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade REAL NOT NULL,
            preco_unitario_na_venda REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
    """)

    conn.commit() # Salva as mudanças no banco de dados
    conn.close() # Fecha a conexão

    print(f"Tabelas criadas ou já existentes no banco de dados '{DB_NAME}'.")

if __name__ == "__main__":
    # Este bloco só será executado se você rodar 'python src/database.py' diretamente
    create_tables()
    print(f"Banco de dados '{DB_NAME}' configurado na pasta 'data'.")