from utils.banners import HEADER_ASCII, BANNERS_CATEGORIAS
from cli.avaliacao import avaliar_categoria, avaliar_todas

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

    # Perguntar nome da empresa
    empresa = input("Informe o nome da empresa: ").strip()
    if not empresa:
        empresa = "EmpresaDefault"  # fallback se quiser

    while True:
        exibir_header()
        print(f"\n🔹 Empresa atual: {empresa}")
        print("\n📌 Selecione uma opção:")
        print("1️⃣  Avaliar TODAS as categorias")
        i = 2
        for cat in categorias.keys():
            print(f"{i}️⃣  {cat}")
            i += 1

        print("\n❌ (Q) Sair")
        escolha = input("\n👉 Escolha uma opção: ").strip().lower()

        if escolha == "q":
            print("\n👋 Saindo... 🚀\n")
            break

        if escolha == "1":
            exibir_banner("Todas as Categorias")
            avaliar_todas(categorias, empresa)  # <-- Passa empresa
        elif escolha.isdigit() and 2 <= int(escolha) <= len(categorias) + 1:
            cat_index = int(escolha) - 2
            categoria_selecionada = list(categorias.keys())[cat_index]
            exibir_banner(categoria_selecionada)
            avaliar_categoria(categorias[categoria_selecionada], empresa)  # <-- Passa empresa
        else:
            print("\n❌ Escolha inválida! Tente novamente.\n")
