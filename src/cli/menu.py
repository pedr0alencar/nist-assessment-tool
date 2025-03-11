from cli.avaliacao import avaliar_categoria, avaliar_todas

def exibir_menu_principal(categorias):
    """Exibe o menu principal para seleção de categoria ou todas de uma vez."""
    while True:
        print("\n📌 Selecione uma opção:")
        print("1. Avaliar todas as categorias")
        for i, categoria in enumerate(categorias.keys(), 2):
            print(f"{i}. {categoria}")

        print("\n(Q) Sair")
        escolha = input("Escolha uma opção: ").strip().lower()

        if escolha == "q":
            print("Saindo... 🚀")
            break

        if escolha == "1":
            avaliar_todas(categorias)
        elif escolha.isdigit() and 2 <= int(escolha) <= len(categorias) + 1:
            categoria_selecionada = list(categorias.keys())[int(escolha) - 2]
            avaliar_categoria(categorias[categoria_selecionada])
        else:
            print("❌ Escolha inválida! Tente novamente.")
