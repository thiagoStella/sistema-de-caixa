import datetime

class Produto:
    """
    Representa um produto no sistema de caixa.
    Cada produto tem um ID (no banco de dados), nome, preço,
    tipo de unidade (UNIDADE/KG) e estoque.
    """
    def __init__(self, id=None, nome=None, preco=None, tipo_unidade=None, estoque=0):
        """
        Construtor da classe Produto.
        Inicializa um novo objeto Produto.

        Args:
            id (int, optional): ID do produto, usado quando carregado do banco de dados. Defaults to None.
            nome (str): Nome do produto.
            preco (float): Preço do produto.
            tipo_unidade (str): Tipo de unidade do produto ('UNIDADE' ou 'KG').
            estoque (int): Quantidade em estoque. Defaults to 0.
        """
        # Atributos (características) do nosso Produto
        self.id = id # Será preenchido pelo banco de dados após a primeira inserção
        self.nome = nome
        self.preco = preco
        self.tipo_unidade = tipo_unidade # 'UNIDADE' ou 'KG'
        self.estoque = estoque

    def __str__(self):
        """
        Retorna uma representação em string do objeto Produto, útil para impressão.
        """
        return f"Produto(ID: {self.id}, Nome: {self.nome}, Preço: R${self.preco:.2f}, Tipo: {self.tipo_unidade}, Estoque: {self.estoque})"

    def __repr__(self):
        """
        Retorna uma representação "oficial" do objeto, útil para depuração.
        """
        return self.__str__() # Por enquanto, a mesma que __str__

    def calcular_subtotal(self, quantidade_vendida):
        """
        Calcula o subtotal para uma dada quantidade deste produto.
        """
        if not isinstance(quantidade_vendida, (int, float)) or quantidade_vendida <= 0:
            raise ValueError("Quantidade vendida deve ser um número positivo.")
        return self.preco * quantidade_vendida

    def atualizar_estoque(self, quantidade_movimentada):
        """
        Atualiza o estoque do produto.
        Pode ser para decremento (venda) ou incremento (reposição).
        """
        novo_estoque = self.estoque + quantidade_movimentada
        if novo_estoque < 0:
            raise ValueError("Estoque não pode ser negativo.")
        self.estoque = novo_estoque
        return self.estoque

# --------------------------------------------------------------------------------------

class Venda:
    """
    Representa uma venda completa no sistema de caixa.
    Uma venda agrupa múltiplos itens de venda e contém informações
    como data/hora, total, status e tipo de pagamento.
    """
    def __init__(self, id=None, data_hora=None, total=0.0, status="ABERTA", tipo_pagamento=None):
        """
        Construtor da classe Venda.
        Inicializa um novo objeto Venda.

        Args:
            id (int, optional): ID da venda, usado quando carregada do banco de dados. Defaults to None.
            data_hora (str, optional): Data e hora da venda (YYYY-MM-DD HH:MM:SS). Defaults to None (set to now if not provided).
            total (float): Valor total da venda. Defaults to 0.0.
            status (str): Status da venda ('ABERTA', 'FINALIZADA', 'CANCELADA'). Defaults to "ABERTA".
            tipo_pagamento (str, optional): Forma de pagamento ('DINHEIRO', 'CARTAO', 'PIX'). Defaults to None.
        """
        self.id = id
        self.data_hora = data_hora if data_hora else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total = total
        self.status = status
        self.tipo_pagamento = tipo_pagamento
        self.itens = [] # Lista de objetos ItemVenda associados a esta venda

    def __str__(self):
        return f"Venda(ID: {self.id}, Data: {self.data_hora}, Total: R${self.total:.2f}, Status: {self.status})"

    def __repr__(self):
        return self.__str__()

    def adicionar_item(self, item_venda):
        """
        Adiciona um objeto ItemVenda à lista de itens desta venda
        e atualiza o total da venda.
        """
        if not isinstance(item_venda, ItemVenda):
            raise TypeError("O item adicionado deve ser uma instância de ItemVenda.")
        self.itens.append(item_venda)
        self.total += item_venda.subtotal # Acumula o subtotal do item ao total da venda

    def remover_item(self, item_venda_id):
        """
        Remove um item da venda pelo seu ID (temporário para a lista em memória).
        NOTA: Para persistência, a remoção deve ocorrer também no banco de dados.
        """
        original_len = len(self.itens)
        self.itens = [item for item in self.itens if item.id != item_venda_id]
        if len(self.itens) < original_len:
            # Recalcula o total se um item foi removido
            self.total = sum(item.subtotal for item in self.itens)
            return True # Item removido com sucesso
        return False # Item não encontrado

# --------------------------------------------------------------------------------------

class ItemVenda:
    """
    Representa um único item dentro de uma venda.
    Cada ItemVenda está ligado a um Produto e a uma Venda.
    """
    def __init__(self, id=None, venda_id=None, produto=None, quantidade=None, preco_unitario_na_venda=None, subtotal=None):
        """
        Construtor da classe ItemVenda.
        Inicializa um novo objeto ItemVenda.

        Args:
            id (int, optional): ID do item de venda, usado quando carregado do banco de dados. Defaults to None.
            venda_id (int, optional): ID da venda à qual este item pertence. Defaults to None.
            produto (Produto): Objeto Produto associado a este item.
            quantidade (float): Quantidade do produto vendida.
            preco_unitario_na_venda (float): Preço do produto no momento da venda (para histórico).
            subtotal (float, optional): Subtotal do item (calculado se não fornecido). Defaults to None.
        """
        self.id = id
        self.venda_id = venda_id
        self.produto = produto # Aqui, o objeto Produto é armazenado!
        self.quantidade = quantidade
        self.preco_unitario_na_venda = preco_unitario_na_venda if preco_unitario_na_venda is not None else produto.preco
        self.subtotal = subtotal if subtotal is not None else \
                        self.preco_unitario_na_venda * self.quantidade

    def __str__(self):
        return (f"ItemVenda(ID: {self.id}, Venda ID: {self.venda_id}, "
                f"Produto: {self.produto.nome}, Qtd: {self.quantidade}, "
                f"Preço Unit.: R${self.preco_unitario_na_venda:.2f}, Subtotal: R${self.subtotal:.2f})")

    def __repr__(self):
        return self.__str__()