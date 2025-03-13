# src/cli/menu.py

import sys
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

def exibir_submenu():
    """Exemplo de submenu para funcionalidades extras."""
    while True:
        print("\n----- SUBMENU DE OPÇÕES -----")
        print("1️⃣  Ver relatórios anteriores (TODO)")
        print("2️⃣  Configurações (TODO)")
        print("B) Voltar ao menu principal")
        escolha = input("👉 Escolha uma opção: ").strip().lower()

        if escolha == "b":
            print("\n↩️ Voltando ao menu principal...\n")
            break
        elif escolha == "1":
            print("Função de ver relatórios não implementada ainda.\n")
        elif escolha == "2":
            print("Função de configurações não implementada ainda.\n")
        else:
            print("❌ Opção inválida.\n")

def exibir_menu_principal(categorias):
    """Exibe o menu principal com opções estilizadas, validando inputs e oferecendo submenu."""

    # Validação: nome da empresa
    empresa = ""
    while not empresa.strip():
        empresa = input("Informe o nome da empresa: ").strip()
        if not empresa:
            print("❌ O nome da empresa não pode ficar em branco.\n")

    while True:
        exibir_header()
        print(f"\n🔹 Empresa atual: {empresa}")
        print("\n📌 Selecione uma opção:")
        print("1️⃣  Avaliar TODAS as categorias")
        print("2️⃣  Entrar no Submenu de Opções")
        print("3️⃣  Trocar nome da empresa (Reavaliar do zero)")

        i = 4
        for cat in categorias.keys():
            print(f"{i}️⃣  {cat}")
            i += 1

        print("\n❌ (Q) Sair")

        escolha = input("\n👉 Escolha uma opção: ").strip().lower()

        if escolha == "q":
            print("\n👋 Saindo... 🚀\n")
            sys.exit(0)

        elif escolha == "1":
            exibir_banner("Todas as Categorias")
            avaliar_todas(categorias, empresa)

        elif escolha == "2":
            exibir_submenu()

        elif escolha == "3":
            # Reiniciar nome da empresa
            empresa = ""
            while not empresa.strip():
                empresa = input("Informe o novo nome da empresa: ").strip()
                if not empresa:
                    print("❌ O nome da empresa não pode ficar em branco.\n")

        elif escolha.isdigit():
            indice = int(escolha)
            # Range para as categorias começa em 4
            if 4 <= indice <= len(categorias) + 3:
                cat_index = indice - 4
                categoria_selecionada = list(categorias.keys())[cat_index]
                exibir_banner(categoria_selecionada)
                avaliar_categoria(categorias[categoria_selecionada], empresa)
            else:
                print("\n❌ Escolha inválida! Tente novamente.\n")

        else:
            print("\n❌ Escolha inválida! Tente novamente.\n")
