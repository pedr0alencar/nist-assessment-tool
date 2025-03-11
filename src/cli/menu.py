from cli.avaliacao import avaliar_categoria, avaliar_todas
from utils.banners import HEADER_ASCII, BANNERS_CATEGORIAS


def exibir_header():
    """Exibe o cabeçalho ASCII do sistema"""
    print(HEADER_ASCII)

def exibir_banner(categoria):
    """Exibe o ASCII correspondente à categoria escolhida"""
    if categoria in BANNERS_CATEGORIAS:
        print(BANNERS_CATEGORIAS[categoria])
    print(f"\n📂 Iniciando avaliação: {categoria}\n")

def exibir_menu_principal(categorias):
    """Exibe o menu principal com opções estilizadas"""
    while True:
        exibir_header()
        print("\n📌 Selecione uma opção:")
        print("1️⃣  Avaliar TODAS as categorias")
        for i, categoria in enumerate(categorias.keys(), 2):
            print(f"{i}️⃣  {categoria}")

        print("\n❌ (Q) Sair")
        escolha = input("\n👉 Escolha uma opção: ").strip().lower()

        if escolha == "q":
            print("\n👋 Saindo... 🚀\n")
            break

        if escolha == "1":
            print("\n🌎 Iniciando avaliação de TODAS as categorias...\n")
            avaliar_todas(categorias)

        elif escolha.isdigit() and 2 <= int(escolha) <= len(categorias) + 1:
            categoria_selecionada = list(categorias.keys())[int(escolha) - 2]
            print(f"\n{BANNERS_CATEGORIAS[categoria_selecionada]}")
            print(f"\n📂 Iniciando avaliação: {categoria_selecionada}\n")
            avaliar_categoria(categorias[categoria_selecionada])

        else:
            print("\n❌ Escolha inválida! Tente novamente.\n")