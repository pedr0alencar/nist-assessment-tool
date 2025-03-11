from cli.avaliacao import avaliar_categoria

def exibir_menu_principal(categorias):
    """Exibe o menu principal para seleção de categoria."""
    while True:
        print("\n📌 Selecione uma categoria para avaliar:")
        for i, categoria in enumerate(categorias.keys(), 1):
            print(f"{i}. {categoria}")

        print("\n(Q) Sair")
        escolha = input("Escolha uma opção: ").strip().lower()

        if escolha == "q":
            print("Saindo... 🚀")
            break

        if escolha.isdigit() and 1 <= int(escolha) <= len(categorias):
            categoria_selecionada = list(categorias.keys())[int(escolha) - 1]
            avaliar_categoria(categorias[categoria_selecionada])
        else:
            print("❌ Escolha inválida! Tente novamente.")
