# src/main.py

from .models import Produto, Venda, ItemVenda
from .repository import ProdutoRepository, VendaRepository
from .database import create_tables # Precisamos disso para garantir que as tabelas existem!

def main():
    print("Iniciando o sistema de caixa...")
    
    # 1. Garante que as tabelas existem
    create_tables()

    # Instanciando nossos repositórios
    produto_repo = ProdutoRepository()
    venda_repo = VendaRepository()

    print("\n--- Testando CRUD de Produto ---")

    # C (Create): Inserindo novos produtos
    arroz = Produto(nome="Arroz Agulha 5kg", preco=25.00, tipo_unidade="UNIDADE", estoque=100)
    feijao = Produto(nome="Feijao Preto 1kg", preco=8.50, tipo_unidade="UNIDADE", estoque=150)
    banana = Produto(nome="Banana Nanica KG", preco=7.90, tipo_unidade="KG", estoque=50)

    # O método save() vai atribuir o ID do banco ao objeto!
    arroz = produto_repo.save(arroz)
    feijao = produto_repo.save(feijao)
    banana = produto_repo.save(banana)
    print(f"Produtos salvos com ID: {arroz.id}, {feijao.id}, {banana.id}")

    # R (Read): Buscando produtos
    produto_buscado_por_id = produto_repo.get_by_id(arroz.id)
    print(f"\nProduto buscado por ID ({arroz.id}): {produto_buscado_por_id}")

    produto_buscado_por_nome = produto_repo.get_by_name("Arroz") # Testando busca por nome parcial/case-insensitive
    print(f"Produto buscado por nome ('Arroz'): {produto_buscado_por_nome}")
    
    # U (Update): Atualizando um produto (estoque do arroz)
    if produto_buscado_por_id:
        print(f"\nEstoque do Arroz antes da venda: {produto_buscado_por_id.estoque}")
        produto_buscado_por_id.atualizar_estoque(-5) # Vende 5 unidades
        produto_repo.save(produto_buscado_por_id) # Salva a alteração no banco
        print(f"Estoque do Arroz depois da venda (atualizado no banco): {produto_buscado_por_id.estoque}")

    # R (Read All): Listando todos os produtos
    todos_produtos = produto_repo.get_all()
    print("\nTodos os produtos no banco:")
    for p in todos_produtos:
        print(f"  - {p}")

    # D (Delete): Removendo um produto (cuidado com IDs usados em vendas!)
    # Vamos criar um produto temporário para deletar
    lixo = Produto(nome="Produto Lixo", preco=1.00, tipo_unidade="UNIDADE", estoque=1)
    lixo = produto_repo.save(lixo)
    print(f"\nProduto Lixo criado com ID: {lixo.id}")
    if produto_repo.delete(lixo.id):
        print(f"Produto com ID {lixo.id} (Produto Lixo) deletado com sucesso.")
    else:
        print(f"Falha ao deletar Produto com ID {lixo.id}.")
    
    # Verifica se realmente foi deletado
    if not produto_repo.get_by_id(lixo.id):
        print(f"Confirmação: Produto com ID {lixo.id} não encontrado após exclusão.")


    print("\n--- Testando CRUD de Venda ---")

    # C (Create): Criando uma nova venda
    venda_nova = Venda()
    # Adicionando itens à venda em memória (usando os produtos que já têm ID do banco)
    item_venda1 = ItemVenda(produto=arroz, quantidade=2, preco_unitario_na_venda=arroz.preco)
    item_venda2 = ItemVenda(produto=feijao, quantidade=1, preco_unitario_na_venda=feijao.preco)
    venda_nova.adicionar_item(item_venda1)
    venda_nova.adicionar_item(item_venda2)
    venda_nova.status = "FINALIZADA"
    venda_nova.tipo_pagamento = "DINHEIRO"
    
    venda_nova = venda_repo.save(venda_nova) # Salva a venda e seus itens no banco
    print(f"\nVenda criada e salva com ID: {venda_nova.id}, Total: R${venda_nova.total:.2f}")


    # R (Read): Buscando uma venda por ID (com seus itens)
    venda_buscada = venda_repo.get_by_id(venda_nova.id)
    if venda_buscada:
        print(f"\nVenda buscada por ID ({venda_nova.id}): {venda_buscada}")
        print("Itens da venda buscada:")
        for item in venda_buscada.itens:
            print(f"  - {item.produto.nome} (Qtd: {item.quantidade}) - Subtotal: R${item.subtotal:.2f}")
    else:
        print(f"Venda com ID {venda_nova.id} não encontrada.")

    # Criando outra venda para ter mais dados para 'get_all'
    outra_venda = Venda()
    item_venda3 = ItemVenda(produto=banana, quantidade=0.5, preco_unitario_na_venda=banana.preco)
    outra_venda.adicionar_item(item_venda3)
    outra_venda.status = "FINALIZADA"
    outra_venda.tipo_pagamento = "CARTAO"
    outra_venda = venda_repo.save(outra_venda)
    print(f"Outra venda criada e salva com ID: {outra_venda.id}")

    # R (Read All): Listando todas as vendas
    todas_vendas = venda_repo.get_all()
    print("\nTodas as vendas no banco:")
    for v in todas_vendas:
        print(f"  - {v}")

    # D (Delete): Removendo uma venda
    if venda_repo.delete(outra_venda.id):
        print(f"\nVenda com ID {outra_venda.id} e seus itens deletados com sucesso.")
    else:
        print(f"\nFalha ao deletar Venda com ID {outra_venda.id}.")
    
    # Verifica se realmente foi deletada
    if not venda_repo.get_by_id(outra_venda.id):
        print(f"Confirmação: Venda com ID {outra_venda.id} não encontrada após exclusão.")


if __name__ == "__main__":
    main()