# src/main.py

from .models import Produto, Venda, ItemVenda

def main():
    print("Iniciando o sistema de caixa...")
    # Futuramente, chamaremos as funções do banco de dados e da GUI aqui.

    print("\n--- Testando a Classe Produto ---")
    # Criando objetos Produto
    arroz = Produto(nome="Arroz 5kg", preco=25.00, tipo_unidade="UNIDADE", estoque=100)
    feijao = Produto(nome="Feijao 1kg", preco=8.50, tipo_unidade="UNIDADE", estoque=150)
    banana = Produto(nome="Banana Prata", preco=7.90, tipo_unidade="KG", estoque=50)
    print("-------------------------------------------------------------")
    print("Produtos!!!")
    print(arroz)
    print(feijao)
    print(banana)
    print("-------------------------------------------------------------")

    print(f"Subtotal para 2 Arroz: R${arroz.calcular_subtotal(2):.2f}")
    print(f"\nEstoque do Arroz antes: {arroz.estoque}")
    arroz.atualizar_estoque(-5) # Vendendo 5 unidades
    print(f"\nEstoque do Arroz depois de vender 5: {arroz.estoque}")
    arroz.atualizar_estoque(10) # Repondo 10 unidades
    print(f"\nEstoque do Arroz depois de repor 10: {arroz.estoque}")


    print("\n\t--- Testando a Classe Venda e ItemVenda ---")
    venda_atual = Venda(status="ABERTA")
    print(f"\n\tVenda criada: {venda_atual}")

    
    item1 = ItemVenda(produto=arroz, quantidade=2, preco_unitario_na_venda=arroz.preco)
    item2 = ItemVenda(produto=feijao, quantidade=3, preco_unitario_na_venda=feijao.preco)
    item3 = ItemVenda(produto=banana, quantidade=0.75, preco_unitario_na_venda=banana.preco) # Exemplo com KG

    print(item1)
    print(item2)
    print(item3)

    venda_atual.adicionar_item(item1)
    venda_atual.adicionar_item(item2)
    venda_atual.adicionar_item(item3)

    print(f"\nVenda após adicionar itens: {venda_atual}")
    print("Itens na venda:")
    for item in venda_atual.itens:
        print(f"  - {item.produto.nome} ({item.quantidade} {item.produto.tipo_unidade}) - R${item.subtotal:.2f}")

    
    print(f"\nRemovendo item com ID {item1.id} (ainda None, então usaremos o objeto) do carrinho (apenas para teste de logica)")


if __name__ == "__main__":
    main()