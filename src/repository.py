
# src/repository.py
import sqlite3
from .database import get_db_connection
from .models import Produto, Venda, ItemVenda
import datetime

# ... o resto do seu código

# src/repository.py

# ... outros imports ...

class ProdutoRepository:
    """
    Repositório para operações de CRUD (Create, Read, Update, Delete)
    com a tabela 'produtos' no banco de dados SQLite.
    """
    def save(self, produto):
        """
        Salva um objeto Produto no banco de dados.
        Se o produto já tiver um ID, ele será atualizado. Caso contrário, será inserido.
        Retorna o objeto Produto com o ID atualizado.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if produto.id:
            cursor.execute("""
                UPDATE produtos SET nome = ?, preco = ?, tipo_unidade = ?, estoque = ?
                WHERE id = ?
            """, (produto.nome, produto.preco, produto.tipo_unidade, produto.estoque, produto.id))
        else:
            cursor.execute("""
                INSERT INTO produtos (nome, preco, tipo_unidade, estoque)
                VALUES (?, ?, ?, ?)
            """, (produto.nome, produto.preco, produto.tipo_unidade, produto.estoque))
            produto.id = cursor.lastrowid

        conn.commit()
        conn.close()
        return produto

    def get_by_id(self, produto_id):
        """
        Busca um produto pelo seu ID no banco de dados.
        Retorna um objeto Produto ou None se não encontrado.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, tipo_unidade, estoque FROM produtos WHERE id = ?", (produto_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Produto(id=row['id'], nome=row['nome'], preco=row['preco'], 
                            tipo_unidade=row['tipo_unidade'], estoque=row['estoque'])
        return None

    def get_by_name(self, produto_name):
        """
        Busca um produto pelo seu nome no banco de dados.
        Retorna um objeto Produto ou None se não encontrado.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, tipo_unidade, estoque FROM produtos WHERE LOWER(nome) LIKE ?", ('%' + produto_name.lower() + '%',))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Produto(id=row['id'], nome=row['nome'], preco=row['preco'], 
                            tipo_unidade=row['tipo_unidade'], estoque=row['estoque'])
        return None

    def get_all(self):
        """
        Busca todos os produtos no banco de dados.
        Retorna uma lista de objetos Produto.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, tipo_unidade, estoque FROM produtos ORDER BY nome")
        rows = cursor.fetchall()
        conn.close()
        
        produtos = []
        for row in rows:
            produtos.append(Produto(id=row['id'], nome=row['nome'], preco=row['preco'], 
                                    tipo_unidade=row['tipo_unidade'], estoque=row['estoque']))
        return produtos

    def delete(self, produto_id):
        """
        Remove um produto do banco de dados pelo seu ID.
        Retorna True se o produto foi removido, False caso contrário.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

# --------------------------------------------------------------------------------------

class VendaRepository:
    """
    Repositório para operações de CRUD com a tabela 'vendas' e 'itens_venda'.
    """
    def save(self, venda):
        """
        Salva uma venda e seus itens no banco de dados.
        Se a venda já tiver um ID, ela será atualizada. Caso contrário, será inserida.
        Retorna o objeto Venda com o ID atualizado.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        if venda.id: # Atualização de venda
            cursor.execute("""
                UPDATE vendas SET data_hora = ?, total = ?, status = ?, tipo_pagamento = ?
                WHERE id = ?
            """, (venda.data_hora, venda.total, venda.status, venda.tipo_pagamento, venda.id))
            
            # Para atualização de itens de venda, a lógica é mais complexa:
            # Geralmente, deletamos todos os itens antigos e inserimos os novos.
            # Ou, verificamos item por item (se existe, atualiza; se não, insere; se sumiu, deleta).
            # Para simplificar aqui, vamos focar na inserção de novos itens para novas vendas.
            # Em um cenário real, você teria um método ItemVendaRepository para isso.
            
            # Por enquanto, se a venda já existe, não vamos mexer nos itens diretamente por este método.
            pass # A gente vai tratar isso mais na frente, ou criar um ItemVendaRepository

        else: # Nova inserção de venda
            cursor.execute("""
                INSERT INTO vendas (data_hora, total, status, tipo_pagamento)
                VALUES (?, ?, ?, ?)
            """, (venda.data_hora, venda.total, venda.status, venda.tipo_pagamento))
            venda.id = cursor.lastrowid # Pega o ID da nova venda

            # Salva os itens da venda
            for item in venda.itens:
                # Garante que o item de venda sabe o ID da venda a que pertence
                item.venda_id = venda.id 
                # Chamar um ItemVendaRepository.save(item) seria o ideal aqui,
                # mas por simplicidade, faremos o insert direto por enquanto.
                cursor.execute("""
                    INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario_na_venda, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (item.venda_id, item.produto.id, item.quantidade, item.preco_unitario_na_venda, item.subtotal))

        conn.commit()
        conn.close()
        return venda

    def get_by_id(self, venda_id):
        """
        Busca uma venda e seus itens pelo ID.
        Retorna um objeto Venda ou None.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Busca a venda principal
        cursor.execute("SELECT id, data_hora, total, status, tipo_pagamento FROM vendas WHERE id = ?", (venda_id,))
        venda_row = cursor.fetchone()

        if not venda_row:
            conn.close()
            return None

        venda = Venda(id=venda_row['id'], data_hora=venda_row['data_hora'], 
                      total=venda_row['total'], status=venda_row['status'], 
                      tipo_pagamento=venda_row['tipo_pagamento'])

        # Busca os itens de venda associados
        cursor.execute("""
            SELECT iv.id, iv.venda_id, iv.produto_id, iv.quantidade, iv.preco_unitario_na_venda, iv.subtotal,
                   p.nome, p.preco, p.tipo_unidade, p.estoque
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = ?
        """, (venda_id,))
        item_rows = cursor.fetchall()
        
        for item_row in item_rows:
            # Recria o objeto Produto para o ItemVenda
            produto = Produto(id=item_row['produto_id'], nome=item_row['nome'], 
                              preco=item_row['preco'], tipo_unidade=item_row['tipo_unidade'], 
                              estoque=item_row['estoque'])
            
            item_venda = ItemVenda(id=item_row['id'], venda_id=item_row['venda_id'],
                                   produto=produto, quantidade=item_row['quantidade'],
                                   preco_unitario_na_venda=item_row['preco_unitario_na_venda'],
                                   subtotal=item_row['subtotal'])
            venda.adicionar_item(item_venda) # Adiciona à lista de itens do objeto Venda

        conn.close()
        return venda

    def get_all(self, status=None):
        """
        Busca todas as vendas no banco de dados, opcionalmente filtrando por status.
        Retorna uma lista de objetos Venda (sem os itens carregados por padrão para performance).
        Para carregar os itens, use get_by_id para cada venda.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, data_hora, total, status, tipo_pagamento FROM vendas"
        params = ()
        if status:
            query += " WHERE status = ?"
            params = (status,)
        query += " ORDER BY data_hora DESC" # Ordena da mais recente para a mais antiga

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        vendas = []
        for row in rows:
            vendas.append(Venda(id=row['id'], data_hora=row['data_hora'], 
                                total=row['total'], status=row['status'], 
                                tipo_pagamento=row['tipo_pagamento']))
        return vendas

    def delete(self, venda_id):
        """
        Remove uma venda e seus itens associados do banco de dados.
        Retorna True se a venda foi removida, False caso contrário.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Inicia uma transação para garantir que ambas as operações ocorram ou nenhuma ocorra
            conn.execute("BEGIN TRANSACTION")
            
            # Primeiro, remove os itens de venda associados
            cursor.execute("DELETE FROM itens_venda WHERE venda_id = ?", (venda_id,))
            
            # Em seguida, remove a venda principal
            cursor.execute("DELETE FROM vendas WHERE id = ?", (venda_id,))
            
            rows_affected = cursor.rowcount # Verifica se a venda principal foi removida
            
            conn.commit() # Confirma as operações
            return rows_affected > 0
        except sqlite3.Error as e:
            conn.rollback() # Desfaz todas as operações em caso de erro
            print(f"Erro ao deletar venda e itens: {e}")
            return False
        finally:
            conn.close()

# --------------------------------------------------------------------------------------

# NOTE para o futuro: Uma classe ItemVendaRepository seria ideal para gerenciar
# o CRUD de ItemVenda de forma mais granular, mas para este protótipo,
# as operações de ItemVenda serão tratadas principalmente dentro de VendaRepository.