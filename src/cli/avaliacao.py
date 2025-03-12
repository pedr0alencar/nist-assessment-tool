import os
import json
from datetime import datetime
from utils.report_generator import gerar_relatorio_html

ASSESSMENTS_DIR = "src/assessments/"

STATUS_OPTIONS = [
    "Não Implementado",
    "Não Aplicável",
    "Planejado",
    "Em Implementação",
    "Parcialmente em Conformidade",
    "Em Conformidade"
]

def avaliar_categoria(categoria_data):
    """Permite avaliar os controles de uma única categoria e retorna ao menu principal."""
    print(f"\n📂 Avaliando Categoria: {categoria_data['categoria']}")

    respostas = []
    for subcat in categoria_data["subcategorias"]:
        print(f"\n🔹 Subcategoria: {subcat['subcategoria']}")
        for controle in subcat["controles"]:
            while True:
                print(f"\n➡️ {controle['controle']}: {controle['descricao']}")
                for i, status in enumerate(STATUS_OPTIONS, 1):
                    print(f"{i}. {status}")

                escolha = input("Escolha um status (ou 'b' para voltar ao menu): ").strip().lower()

                if escolha == "b":
                    return  # Volta ao menu principal imediatamente

                if escolha.isdigit() and 1 <= int(escolha) <= len(STATUS_OPTIONS):
                    respostas.append({
                        "controle": controle["controle"],
                        "descricao": controle["descricao"],
                        "status": STATUS_OPTIONS[int(escolha) - 1]
                    })
                    break
                else:
                    print("❌ Entrada inválida! Escolha um número válido.")

    salvar_avaliacao(categoria_data["categoria"], respostas)

def avaliar_todas(categorias):
    """Percorre todas as categorias e permite avaliá-las uma por uma."""
    for categoria_nome, categoria_data in categorias.items():
        print(f"\n📂 Iniciando avaliação da categoria: {categoria_nome}")
        avaliar_categoria(categoria_data)

def salvar_avaliacao(categoria, respostas):
    """Salva a avaliação em um arquivo JSON e gera o relatório HTML."""
    if not os.path.exists(ASSESSMENTS_DIR):
        os.makedirs(ASSESSMENTS_DIR)

    json_filename = f"avaliacao_{categoria}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    json_path = os.path.join(ASSESSMENTS_DIR, json_filename)

    # Salvar o JSON
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump({"categoria": categoria, "respostas": respostas}, file, indent=4, ensure_ascii=False)

    print(f"\n✅ Avaliação salva em: {json_path}")

    # Gerar relatório HTML
    html_path = gerar_relatorio_html(categoria, respostas, destino="src/reports")
    print(f"✅ Relatório HTML gerado em: {html_path}\n")