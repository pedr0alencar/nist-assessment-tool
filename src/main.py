# src/main.py
import matplotlib.pyplot as plt
import pandas as pd

categorias = {
    "Governar": [
        "Política de Segurança da Informação",
        "Conscientização e Treinamento",
        "Responsabilidade Organizacional"
    ],
    "Identificar": [
        "Inventário de Ativos",
        "Gestão de Riscos"
    ],
    "Proteger": [
        "Gerenciamento de Senhas",
        "Autenticação Multifator"
    ],
    "Detectar": [
        "Monitoramento Contínuo",
        "Sistemas Antivírus"
    ],
    "Responder": [
        "Plano de Resposta a Incidentes",
        "Comunicação"
    ],
    "Recuperar": [
        "Backup e Recuperação",
        "Plano de Continuidade de Negócios"
    ]
}

estados = [
    "Não implementado",
    "Não aplicável",
    "Planejado",
    "Em implementação",
    "Parcialmente em conformidade",
    "Em conformidade"
]

def coletar_respostas():
    respostas = {}

    for categoria, controles in categorias.items():
        print(f"\nCategoria: {categoria}")
        respostas[categoria] = {}

        for controle in controles:
            print(f"\nControle: {controle}\nSelecione o estado atual desse controle:")

            for idx, estado in enumerate(estados, 1):
                print(f"[{idx}] {estado}")

            while True:
                try:
                    selecao = int(input("Seleção: "))
                    if 1 <= selecao <= len(estados):
                        respostas[categoria][controle] = estados[selecao - 1]
                        break
                    else:
                        print(f"Selecione um valor entre 1 e {len(estados)}.")
                except ValueError:
                    print("Por favor, insira um número válido.")

    return respostas

def exibir_resumo(respostas):
    print("\nResumo da Avaliação NIST:\n")

    for categoria, controles in respostas.items():
        print(f"{categoria}:")
        for controle, estado in controles.items():
            print(f"  - {controle}: {estado}")
        print()


def gerar_graficos(respostas):
    dados = []

    for categoria, controles in respostas.items():
        for controle, estado in controles.items():
            dados.append([categoria, controle, estado])

    df = pd.DataFrame(dados, columns=['Categoria', 'Controle', 'Estado'])

    # Gráfico 1: Contagem geral de estados
    plt.figure(figsize=(8, 6))
    df['Estado'].value_counts().plot(kind='barh')
    plt.title('Quantidade de Controles por Estado')
    plt.xlabel('Quantidade')
    plt.ylabel('Estado')
    plt.grid(axis='x')
    plt.tight_layout()
    plt.savefig('grafico_estados.png')
    plt.show()

    # Gráfico 2: Estados por Categoria
    estados_categoria = df.groupby(['Categoria', 'Estado']).size().unstack(fill_value=0)
    estados_categoria.plot(kind='bar', stacked=True, figsize=(10, 7))
    plt.title('Estados dos Controles por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Quantidade de Controles')
    plt.xticks(rotation=30)
    plt.legend(title='Estado')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig('grafico_estados_categoria.png')
    plt.show()

def main():
    print("\nNIST Cybersecurity Assessment Tool\n")
    respostas = coletar_respostas()
    exibir_resumo(respostas)
    gerar_graficos(respostas)

if __name__ == "__main__":
    main()
