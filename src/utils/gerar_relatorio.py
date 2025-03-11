import json
import os

# Caminhos
DATA_DIR = '../data/'
RESPOSTAS_DIR = '../respostas/'

# Carrega categorias disponíveis
categorias = [
    'governar',
    'identificar',
    'proteger',
    'detectar',
    'responder',
    'recuperar'
]

# Função para carregar arquivos JSON
def carregar_json(categoria):
    with open(f"{DATA_DIR}/controles_{categoria}.json", 'r', encoding='utf-8') as file:
        return json.load(file)

# Pergunta ao usuário sobre a conformidade
def perguntar_conformidade(controle, descricao):
    opcoes = {
        '1': 'Não Implementado',
        '2': 'Não Aplicável',
        '3': 'Planejado',
        '4': 'Em Implementação',
        '5': 'Parcialmente em Conformidade',
        '6': 'Em Conformidade'
    }
    print(f"\nControle: {controle}")
    print(f"Descrição: {descricao}\n")
    for chave, valor in opcoes.items():
        print(f"{chave}. {valor}")

    resposta = input("\nSelecione uma opção (1-6): ")
    while resposta not in opcoes:
        resposta = input("Opção inválida. Escolha novamente (1-6): ")

    return opcoes[resposta]

# Iniciar Avaliação
def iniciar_avaliacao(empresa_nome):
    resultado = {"empresa": empresa_nome, "categorias": {}}

    for categoria in categorias:
        dados_categoria = carregar_json(categoria)
        resultado["categorias"][categoria] = []

        print(f"\n--- Avaliando Categoria: {dados_categoria['categoria']} ---")

        for subcategoria in dados_categoria['subcategorias']:
            for controle in subcategoria['controles']:
                resposta = perguntar_conformidade(controle['controle'], controle['descricao'])
                resultado["categorias"][categoria].append({
                    "controle": controle['controle'],
                    "descricao": controle['descricao'],
                    "avaliacao": resposta
                })

    # Salvar respostas
    os.makedirs(RESPOSTAS_DIR, exist_ok=True)
    with open(f"{RESPOSTAS_DIR}/{empresa_nome.lower()}_respostas.json", 'w', encoding='utf-8') as file:
        json.dump(resultado, file, ensure_ascii=False, indent=4)

    print(f"\n✅ Avaliação salva com sucesso em '{RESPOSTAS_DIR}/{empresa_nome.lower()}_respostas.json'!")

# Executa script
if __name__ == "__main__":
    empresa = input("Digite o nome da empresa: ")
    iniciar_avaliacao(empresa)
