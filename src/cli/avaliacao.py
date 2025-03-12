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

                if escolha.isdigit() and 1 <= int(escolha) <= len(STATUS_OPTIONS):
                    respostas.append({
                        "controle": controle["controle"],
                        "descricao": controle["descricao"],
                        "status": STATUS_OPTIONS[int(escolha) - 1]
                    })
                    break
                else:
                    print("\n❌ Entrada inválida! Escolha um número válido.\n")

    # Ao terminar, salvamos JSON + geramos Relatório (single)
    salvar_avaliacao_e_relatorio(empresa, categoria_data["categoria"], respostas)


def avaliar_todas(categorias, empresa):
    """
    Avalia TODAS as categorias. Salva JSON de cada uma,
    e no final gera 1 relatório HTML que engloba tudo.
    """
    dados_por_categoria = {}

    for cat_nome, cat_data in categories.items():
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
                        print("\n↩️ Pulando essa categoria...\n")
                        break  # Sai do laço dos controles, mas continua fluxo

                    if escolha.isdigit() and 1 <= int(escolha) <= len(STATUS_OPTIONS):
                        respostas.append({
                            "controle": controle["controle"],
                            "descricao": controle["descricao"],
                            "status": STATUS_OPTIONS[int(escolha) - 1]
                        })
                        break
                    else:
                        print("\n❌ Entrada inválida! Escolha um número válido.\n")

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

    # Salvar JSON
    json_filename = f"avaliacao_{categoria}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    json_path = os.path.join(assessments_dir, json_filename)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump({"categoria": categoria, "respostas": respostas}, file, indent=4, ensure_ascii=False)

    print(f"\n✅ Avaliação salva em: {json_path}")

    # Relatório single
    html_path = gerar_relatorio_html_single(categoria, respostas, destino=reports_dir)
    print(f"✅ Relatório HTML gerado em: {html_path}\n")


def salvar_json_unico(empresa, categoria, respostas):
    """
    Salva apenas o JSON de uma categoria, sem gerar relatório single.
    Usado em 'avaliar_todas'.
    """
    dirs = criar_pastas_empresa(empresa)
    assessments_dir = dirs["assessments"]

    json_filename = f"avaliacao_{categoria}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    json_path = os.path.join(assessments_dir, json_filename)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump({"categoria": categoria, "respostas": respostas}, file, indent=4, ensure_ascii=False)

    print(f"\n✅ [Categoria {categoria}] Avaliação salva em: {json_path}")


def criar_pastas_empresa(empresa):
    """
    Cria pasta para a empresa, com subpastas 'assessments' e 'reports' se não existirem,
    e retorna um dicionário com os caminhos.
    Ex: {
      "base": "src/clientes/EmpresaXYZ",
      "assessments": "src/clientes/EmpresaXYZ/assessments",
      "reports": "src/clientes/EmpresaXYZ/reports"
    }
    """
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
