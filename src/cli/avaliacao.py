import os
import json
from datetime import datetime

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
