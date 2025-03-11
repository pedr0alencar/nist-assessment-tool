import json
import os
from datetime import datetime

# Diretório onde os arquivos JSON das categorias estão armazenados
DATA_DIR = "src/data/"
ASSESSMENTS_DIR = "src/assessments/"

# Status possíveis para cada controle
STATUS_OPTIONS = [
    "Não Implementado",
    "Não Aplicável",
    "Planejado",
    "Em Implementação",
    "Parcialmente em Conformidade",
    "Em Conformidade"
]

def carregar_categorias():
    """Carrega todos os arquivos JSON das categorias e retorna um dicionário."""
    categorias = {}
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            path = os.path.join(DATA_DIR, filename)
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                categorias[data["categoria"]] = data
    return categorias

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

def avaliar_categoria(categoria_data):
    """Permite avaliar os controles de uma categoria."""
    print(f"\n📂 Categoria: {categoria_data['categoria']}")

    respostas = []
    for subcat in categoria_data["subcategorias"]:
        print(f"\n🔹 Subcategoria: {subcat['subcategoria']}")
        for controle in subcat["controles"]:
            while True:
                print(f"\n➡️ {controle['controle']}: {controle['descricao']}")
                for i, status in enumerate(STATUS_OPTIONS, 1):
                    print(f"{i}. {status}")

                escolha = input("Escolha um status (ou 'b' para voltar): ").strip().lower()

                if escolha == "b":
                    return  # Volta para o menu principal

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

def salvar_avaliacao(categoria, respostas):
    """Salva a avaliação em um arquivo JSON."""
    if not os.path.exists(ASSESSMENTS_DIR):
        os.makedirs(ASSESSMENTS_DIR)

    filename = f"{ASSESSMENTS_DIR}avaliacao_{categoria}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump({"categoria": categoria, "respostas": respostas}, file, indent=4, ensure_ascii=False)

    print(f"\n✅ Avaliação salva com sucesso em: {filename}")

if __name__ == "__main__":
    categorias = carregar_categorias()
    exibir_menu_principal(categorias)
