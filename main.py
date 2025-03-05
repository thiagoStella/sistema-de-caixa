def menu():
    menu_opcao = """
    ========== MENU ==========
    [R] Registrar produto
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
        listagem += f"{produto} ;\n"
        preco = int(input("Digite o valor: "))
        cesta += preco
        quantidade += 1
        print("Produto cadastrado com sucesso!")
        print("="*50)
    else:
        print("Por favor, digite o nome do produto!")

def mostrar_parcial():
    print("="*10)
    print(listagem)
    print("="*10)

def finalizar_compra():
    print(f"Valor a ser cobrado: R${cesta}")
    input("dinheiro ou cartão?")

def main():
    global cesta, quantidade, listagem
    cesta = 0
    quantidade = 0
    listagem = ""
    while True:
        opcao = menu()
        if opcao == "r":
            registrar_produto()
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