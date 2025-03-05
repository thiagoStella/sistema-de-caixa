def menu():
    menu_opcao = """
    ========== MENU ==========
    [R] Registrar produto
    [X] Remover produto
    [P] Parcial
    [F] Finalizar compra
    [Q] Sair
    ==========================
    """
    return input(menu_opcao).lower()

def registrar_produto():
    global listagem, cesta, quantidade
    produto = input("Digite o nome do produto: ")
    if produto:
        preco = int(input("Digite o valor: "))
        listagem.append({'nome': produto, 'valor': preco})
        cesta += preco
        quantidade += 1
        print("Produto cadastrado com sucesso!")
        print("="*50)
    else:
        print("Por favor, digite o nome do produto!")

def remover_produto():
    global listagem, cesta, quantidade
    if not listagem:
        print("A LISTA ENCONTRA-SE VAZIA")
        return
    print("Listagem dos produtos:")
    for i, item in enumerate(listagem):
        print(f"{i + 1}. {item['nome']}: R$ {item['preco']}")
    
    opcao = int(input("Digite o item que deseja remover da lista de compras: (0 para cancelar)"))
    if opcao == 0:
        return
    if 1 <= opcao <= len(listagem):
        item_removido = listagem.pop(opcao - 1)
        cesta -= item_removido['valor']
        quantidade -= 1
        print(f"O Produto '{item_removido['nome']}' foi removido.")


def mostrar_parcial():
    print("="*50)
    for i, item in enumerate(listagem):
        print(f"{i + 1}.{item['nome']}: \tR$ {item['valor']}")
    print(f"\nSub-Total: {cesta}")
    print("="*50)

def finalizar_compra():
    print(f"Valor a ser cobrado: R${cesta}")
    input("dinheiro ou cartão?")

def main():
    global cesta, quantidade, listagem
    cesta = 0
    quantidade = 0
    listagem = []
    while True:
        opcao = menu()
        if opcao == "r":
            registrar_produto()
        if opcao == "x":
            remover_produto()
        elif opcao == "p":
            mostrar_parcial()
        elif opcao == "f":
            finalizar_compra()
            break
        elif opcao == "q":
            break
        else:
            print("Opção inválida, tente novamente!")

if __name__ == "__main__":
    main()