# src/cli/avaliacao.py

import os
import json
from datetime import datetime
from utils.report_generator import gerar_relatorio_html_single, gerar_relatorio_html_all

STATUS_OPTIONS = [
    "Não Implementado",
    "Não Aplicável",
    "Planejado",
    "Em Implementação",
    "Parcialmente em Conformidade",
    "Em Conformidade"
]

def avaliar_categoria(categoria_data, empresa):
    """
    Avalia uma única categoria, salva JSON e gera relatório HTML SINGLE.
    """
    print(f"\n📂 Avaliando Categoria: {categoria_data['categoria']}")
    print("=" * 50)

    respostas = []
    for subcat in categoria_data["subcategorias"]:
        print(f"\n🔹 {subcat['subcategoria']}")
        print("-" * 50)
        for controle in subcat["controles"]:
            while True:
                print(f"\n➡️ {controle['controle']}: {controle['descricao']}")
                for i, status in enumerate(STATUS_OPTIONS, 1):
                    print(f"{i}. {status}")

                escolha = input("\n👉 Escolha um status (ou 'b' para voltar ao menu): ").strip().lower()

                if escolha == "b":
                    print("\n↩️ Voltando ao menu...\n")
                    return

                # Validação do input
                if not escolha.isdigit():
                    print("\n❌ Entrada inválida! Digite um número.\n")
                    continue

                idx = int(escolha)
                if 1 <= idx <= len(STATUS_OPTIONS):
                    respostas.append({
                        "controle": controle["controle"],
                        "descricao": controle["descricao"],
                        "status": STATUS_OPTIONS[idx - 1]
                    })
                    break
                else:
                    print(f"\n❌ Escolha um número entre 1 e {len(STATUS_OPTIONS)}.\n")

    salvar_avaliacao_e_relatorio(empresa, categoria_data["categoria"], respostas)


def avaliar_todas(categorias, empresa):
    """
    Avalia TODAS as categorias. Salva JSON de cada uma,
    e no final gera 1 relatório HTML que engloba tudo.
    """
    dados_por_categoria = {}

    # Corrigido: usar 'categorias.items()' em vez de 'categories.items()'
    for cat_nome, cat_data in categorias.items():
        print(f"\n📂 Iniciando avaliação da categoria: {cat_nome}\n")
        print("=" * 50)

        respostas = []
        for subcat in cat_data["subcategorias"]:
            print(f"\n🔹 {subcat['subcategoria']}")
            print("-" * 50)
            for controle in subcat["controles"]:
                while True:
                    print(f"\n➡️ {controle['controle']}: {controle['descricao']}")
                    for i, status in enumerate(STATUS_OPTIONS, 1):
                        print(f"{i}. {status}")

                    escolha = input("\n👉 Escolha um status (ou 'b' para pular esta categoria): ").strip().lower()

                    if escolha == "b":
                        print("\n↩️ Pulando essa subcategoria...\n")
                        break

                    if not escolha.isdigit():
                        print("\n❌ Entrada inválida! Digite um número.\n")
                        continue

                    idx = int(escolha)
                    if 1 <= idx <= len(STATUS_OPTIONS):
                        respostas.append({
                            "controle": controle["controle"],
                            "descricao": controle["descricao"],
                            "status": STATUS_OPTIONS[idx - 1]
                        })
                        break
                    else:
                        print(f"\n❌ Escolha um número entre 1 e {len(STATUS_OPTIONS)}.\n")

        # Salvamos JSON para essa categoria
        salvar_json_unico(empresa, cat_nome, respostas)
        dados_por_categoria[cat_nome] = respostas

    # Ao final, gera relatório ALL
    gerar_relatorio_html_all(dados_por_categoria, destino=criar_pastas_empresa(empresa)["reports"])
    print("\n✅ Relatório HTML GLOBAL gerado com sucesso!\n")


def salvar_avaliacao_e_relatorio(empresa, categoria, respostas):
    """
    Salva JSON e gera relatório HTML para UMA categoria.
    """
    dirs = criar_pastas_empresa(empresa)
    assessments_dir = dirs["assessments"]
    reports_dir = dirs["reports"]

    json_filename = f"avaliacao_{categoria}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    json_path = os.path.join(assessments_dir, json_filename)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump({"categoria": categoria, "respostas": respostas}, file, indent=4, ensure_ascii=False)

    print(f"\n✅ Avaliação salva em: {json_path}")

    html_path = gerar_relatorio_html_single(categoria, respostas, destino=reports_dir)
    print(f"✅ Relatório HTML gerado em: {html_path}\n")


def salvar_json_unico(empresa, categoria, respostas):
    dirs = criar_pastas_empresa(empresa)
    assessments_dir = dirs["assessments"]

    json_filename = f"avaliacao_{categoria}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    json_path = os.path.join(assessments_dir, json_filename)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump({"categoria": categoria, "respostas": respostas}, file, indent=4, ensure_ascii=False)

    print(f"\n✅ [Categoria {categoria}] Avaliação salva em: {json_path}")


def criar_pastas_empresa(empresa):
    base_empresa = os.path.join("src", "clientes", empresa)
    assessments_dir = os.path.join(base_empresa, "assessments")
    reports_dir = os.path.join(base_empresa, "reports")

    if not os.path.exists(base_empresa):
        os.makedirs(base_empresa)
    if not os.path.exists(assessments_dir):
        os.makedirs(assessments_dir)
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    return {
        "base": base_empresa,
        "assessments": assessments_dir,
        "reports": reports_dir
    }
