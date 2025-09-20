# src/main.py
import sys
from .database import create_tables
from .repository import ProdutoRepository, VendaRepository
from .models import Produto, Venda, ItemVenda

def menu():
    """
    Exibe o menu principal do sistema e captura a opção do usuário.
    """
    menu_opcao = """
    ========== MENU ==========
    [R] Registrar produto
    [X] Remover produto
    [P] Parcial
    [F] Finalizar compra
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
        
def main():
    """
    Loop principal do sistema de caixa.
    """
    create_tables()
    
    while True:
        opcao = menu()
        
        if opcao == "r":
            registrar_produto()
        elif opcao == "x":  # Adicionando a nova opção para remover
            remover_produto()
        elif opcao == "s":
            print("Encerrando o sistema...")
            sys.exit(0)
        else:
            print("Opção inválida, tente novamente!")

if __name__ == "__main__":
    main()