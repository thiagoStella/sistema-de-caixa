menu = """
[R] Registrar produto
[P] Parcial
[F] Finalizar compra

"""
cesta = 0
quantidade = 0
listagem = ""

while True:
    opcao = input(menu)
    if opcao == "r":
        lista = input("Digite o nome do produto: ")
        listagem += f"{lista} ;\n"
        preço = int(input("Digite o valor: "))
        cesta += preço
        quantidade += 1
    
    elif opcao == "p":        
        print(15*"=")
        print(f"{listagem}\nTotal de itens: {quantidade}\nValor total: {cesta}")
        print(15*"=")
        
    elif opcao == "f":
        print(f"Valor a ser cobrado: R${cesta}")
        input("dinehiro ou cartao?")
        break