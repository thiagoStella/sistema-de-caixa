# src/main.py
import sys
from .database import create_tables
from .repository import ProdutoRepository, VendaRepository
from .models import Produto, Venda, ItemVenda

venda_atual = None

def menu():
    """
    Exibe o menu principal do sistema e captura a opção do usuário.
    """
    menu_opcao = """
    ========== MENU ==========
    [R] Adicionar produto à venda
    [P] Parcial
    [F] Finalizar compra
    [G] Gerenciar produtos
    [S] Sair
    ==========================
    """
    return input(menu_opcao).lower()

def registrar_produto():
    """
    Refatora a função original para usar a classe Produto e o ProdutoRepository.
    Permite registrar um novo produto no banco de dados.
    """
    nome = input("Digite o nome do produto: ").strip()
    if not nome:
        print("Nome do produto não pode ser vazio.")
        return

    try:
        preco_input = input("Digite o valor do produto: ")
        # Substitui a vírgula por ponto para o float funcionar em pt-br
        preco = float(preco_input.replace(',', '.')) 
        if preco <= 0:
            print("O preço deve ser maior que zero.")
            return

        tipo_unidade_input = input("Tipo de unidade (UNIDADE/KG): ").upper()
        if tipo_unidade_input not in ["UNIDADE", "KG"]:
            print("Tipo de unidade inválido. Use 'UNIDADE' ou 'KG'.")
            return
            
        estoque = int(input("Digite a quantidade em estoque: "))
        if estoque < 0:
            print("Estoque não pode ser negativo.")
            return

    except ValueError:
        print("Entrada inválida. Certifique-se de digitar números para preço e estoque.")
        return
    
    produto_repo = ProdutoRepository()
    
    # 1. Cria um objeto Produto a partir das entradas do usuário
    novo_produto = Produto(nome=nome, preco=preco, tipo_unidade=tipo_unidade_input, estoque=estoque)

    # 2. Usa o Repositório para salvar o objeto no banco de dados
    produto_repo.save(novo_produto)
    
    print("Produto registrado com sucesso!")
    print(f"ID do produto: {novo_produto.id}")
    print("="*50)

def remover_produto():

    """
    Refatora a função original para remover um produto do banco de dados.
    """
    produto_repo = ProdutoRepository()
    
    # Busca e exibe todos os produtos para o usuário escolher
    produtos = produto_repo.get_all()
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print("="*50)
    print("LISTA DE PRODUTOS CADASTRADOS:")
    for p in produtos:
        print(f"- [ID: {p.id}] Nome: {p.nome} | Preço: R${p.preco:.2f} | Estoque: {p.estoque}")
    print("="*50)

    try:
        produto_id = int(input("Digite o ID do produto que deseja remover (0 para cancelar): "))
    except ValueError:
        print("Entrada inválida. Digite um número.")
        return

    if produto_id == 0:
        print("Operação cancelada.")
        return

    # Busca o produto no banco de dados para confirmar a existência
    produto_a_remover = produto_repo.get_by_id(produto_id)
    if not produto_a_remover:
        print("ID de produto não encontrado. Por favor, tente novamente.")
        return
        
    confirmacao = input(f"Tem certeza que deseja remover '{produto_a_remover.nome}'? (S/N): ").lower()
    if confirmacao == 's':
        if produto_repo.delete(produto_id):
            print(f"Produto '{produto_a_remover.nome}' removido com sucesso do banco de dados.")
        else:
            print(f"Erro ao remover produto '{produto_a_remover.nome}'.")
    else:
        print("Operação cancelada.")

def gerenciar_produtos():
    """
    Menu e lógica para o dono gerenciar os produtos.
    """
    senha = input("Digite a senha de acesso para o modo administrativo: ")
    SENHA_ADMIN = "admin"

    if senha != SENHA_ADMIN:
        print("Senha incorreta. Acesso negado.")
        return

    # Se a senha estiver correta, exibe o menu administrativo
    while True:
        menu_admin = """
        ==== MENU ADMINISTRATIVO ====
        [A] Adicionar novo produto
        [E] Editar produto
        [D] Deletar produto
        [V] Voltar ao menu principal
        =============================
        """
        opcao_admin = input(menu_admin).lower()

        if opcao_admin == 'a':
            registrar_produto() 
        elif opcao_admin == 'e':
            print("Funcionalidade 'Editar' ainda não implementada.")
            # Ainda para implementar
        elif opcao_admin == 'd':
            remover_produto()
        elif opcao_admin == 'v':
            break # Volta ao menu principal
        else:
            print("Opção inválida, tente novamente.")

def mostrar_parcial():
    """
    Mostra os itens adicionados à venda em andamento e o total parcial.
    """
    global venda_atual
    
    if not venda_atual or not venda_atual.itens:
        print("A venda encontra-se vazia.")
        return

    print("=" * 50)
    print("RESUMO DA VENDA:")
    for i, item in enumerate(venda_atual.itens):
        print(f"{i + 1}. {item.produto.nome}: \tR$ {item.subtotal:.2f}")
    
    print("-" * 50)
    print(f"Sub-Total: R${venda_atual.total:.2f}")
    print("=" * 50)
    
def finalizar_compra():
    """
    Finaliza a venda em andamento, atualiza o estoque e salva no banco de dados.
    """
    global venda_atual
    venda_repo = VendaRepository()
    produto_repo = ProdutoRepository()
    
    if not venda_atual or not venda_atual.itens:
        print("Não há itens para finalizar a compra.")
        return

    print("=" * 50)
    print(f"Valor a ser cobrado: R${venda_atual.total:.2f}")
    
    tipo_pagamento = input("Tipo de pagamento (DINHEIRO/CARTAO/PIX): ").upper()
    if tipo_pagamento not in ["DINHEIRO", "CARTAO", "PIX"]:
        print("Tipo de pagamento inválido.")
        return
        
    venda_atual.status = "FINALIZADA"
    venda_atual.tipo_pagamento = tipo_pagamento

    # Atualiza o estoque no banco de dados para cada item da venda
    print("Atualizando estoque...")
    for item in venda_atual.itens:
        produto = produto_repo.get_by_id(item.produto.id)
        if produto:
            try:
                produto.atualizar_estoque(-item.quantidade)
                produto_repo.save(produto)
            except ValueError as e:
                print(f"Erro ao atualizar estoque do produto '{produto.nome}': {e}")
                # Em um sistema real, aqui você cancelaria a transação e informaria ao usuário.

    # Salva a venda e seus itens no banco de dados
    venda_repo.save(venda_atual)
    
    print("\nCompra finalizada com sucesso!")
    print("=" * 50)

    # Limpa a venda atual para uma nova transação
    venda_atual = Venda()

def adicionar_produto_a_venda():
    """
    Função para adicionar um produto existente no banco de dados à venda em andamento.
    """
    global venda_atual
    produto_repo = ProdutoRepository()
    
    # Exibe todos os produtos do banco para o usuário escolher
    produtos = produto_repo.get_all()
    if not produtos:
        print("Nenhum produto cadastrado para adicionar à venda.")
        return

    print("="*50)
    print("PRODUTOS DISPONÍVEIS:")
    for p in produtos:
        print(f"- [ID: {p.id}] Nome: {p.nome} | Preço: R${p.preco:.2f} | Estoque: {p.estoque}")
    print("="*50)
    
    try:
        produto_id = int(input("Digite o ID do produto para adicionar à venda: "))
        quantidade = float(input("Digite a quantidade: "))
    except ValueError:
        print("Entrada inválida. Digite números para ID e quantidade.")
        return
        
    produto_selecionado = produto_repo.get_by_id(produto_id)
    if not produto_selecionado:
        print("ID de produto não encontrado.")
        return

    try:
        # A validação de estoque está no método da classe Produto
        if quantidade <= 0 or quantidade > produto_selecionado.estoque:
            raise ValueError("Quantidade inválida ou insuficiente em estoque.")
            
        # Cria um objeto ItemVenda e o adiciona à Venda em andamento
        item_venda = ItemVenda(
            produto=produto_selecionado, 
            quantidade=quantidade,
            preco_unitario_na_venda=produto_selecionado.preco # Salva o preço atual
        )
        
        venda_atual.adicionar_item(item_venda)
        print(f"'{produto_selecionado.nome}' adicionado à venda. Subtotal: R${item_venda.subtotal:.2f}")
    except ValueError as e:
        print(f"Erro: {e}")





# O restante do seu main.py, agora completo.
def main():
    """
    Loop principal do sistema de caixa.
    """
    create_tables()
    
    global venda_atual
    venda_atual = Venda()

    while True:
        opcao = menu()
        
        if opcao == "r":
            adicionar_produto_a_venda() 
        elif opcao == "p":
            mostrar_parcial()
        elif opcao == "f":
            finalizar_compra()
        elif opcao == "g":
            gerenciar_produtos()
        elif opcao == "s":
            print("Encerrando o sistema...")
            sys.exit(0)
        else:
            print("Opção inválida, tente novamente!")

if __name__ == "__main__":
    main()