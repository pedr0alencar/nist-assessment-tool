# src/main.py

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

def main():
    print("\nNIST Cybersecurity Assessment Tool\n")
    respostas = coletar_respostas()
    exibir_resumo(respostas)

if __name__ == "__main__":
    main()
