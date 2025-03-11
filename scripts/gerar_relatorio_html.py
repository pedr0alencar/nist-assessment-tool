import json
import os
from datetime import datetime

RESPOSTAS_DIR = "../respostas/"
RELATORIOS_DIR = "../relatorios/"

def listar_arquivos_respostas():
    """Lista os arquivos JSON disponíveis na pasta respostas/"""
    arquivos = [f for f in os.listdir(RESPOSTAS_DIR) if f.endswith(".json")]
    if not arquivos:
        print("❌ Nenhum arquivo de resposta encontrado. Execute primeiro 'gerar_relatorio.py'.")
        exit()

    print("\n📂 Arquivos disponíveis:")
    for i, arquivo in enumerate(arquivos, start=1):
        print(f"{i}. {arquivo}")

    escolha = input("\nSelecione um número para gerar o relatório: ")
    while not escolha.isdigit() or int(escolha) not in range(1, len(arquivos) + 1):
        escolha = input("Entrada inválida. Digite um número válido: ")

    return arquivos[int(escolha) - 1]

def gerar_html(arquivo_respostas):
    """Gera o relatório HTML a partir do arquivo de respostas selecionado"""
    nome_empresa = arquivo_respostas.replace("_respostas.json", "").replace("_", " ").title()
    caminho_respostas = os.path.join(RESPOSTAS_DIR, arquivo_respostas)

    # Carrega os dados da avaliação
    with open(caminho_respostas, 'r', encoding='utf-8') as file:
        dados = json.load(file)

    total_controles = sum(len(cat) for cat in dados["categorias"].values())
    resultados = {}

    for categoria, controles in dados["categorias"].items():
        for controle in controles:
            avaliacao = controle["avaliacao"]
            resultados[avaliacao] = resultados.get(avaliacao, 0) + 1

    # Estrutura base do HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Avaliação - {nome_empresa}</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Relatório de Avaliação - {nome_empresa}</h1>
        <p><strong>Data:</strong> {datetime.now().strftime("%d/%m/%Y")}</p>

        <h2>Sumário Executivo</h2>
        <p>Total de controles avaliados: {total_controles}</p>

        <canvas id="graficoPizza" width="400" height="200"></canvas>

        <h2>Detalhamento da Avaliação</h2>
    """

    for categoria, controles in dados['categorias'].items():
        html_categoria = f"<h3>{categoria.capitalize()}</h3><ul>"
        for controle in controles:
            html_categoria += f"""
                <li>
                    <strong>{controle['controle']}</strong>: {controle['descricao']} 
                    <em>({controle['avaliacao']})</em>
                </li>
            """
        html_categoria += "</ul>"
        html_content += html_categoria

    # Scripts para Gráficos
    html_content += f"""
    <script>
        var ctx = document.getElementById('graficoPizza').getContext('2d');
        var graficoPizza = new Chart(ctx, {{
            type: 'pie',
            data: {{
                labels: {list(resultados.keys())},
                datasets: [{{
                    data: {list(resultados.values())},
                    backgroundColor: [
                        '#4CAF50', '#FFEB3B', '#FF9800', '#2196F3', '#F44336', '#9E9E9E'
                    ]
                }}]
            }}
        }});
    </script>

    </body>
    </html>
    """

    # Salvar o relatório
    os.makedirs(RELATORIOS_DIR, exist_ok=True)
    caminho_relatorio = os.path.join(RELATORIOS_DIR, arquivo_respostas.replace("_respostas.json", "_relatorio.html"))
    
    with open(caminho_relatorio, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    print(f"\n✅ Relatório HTML gerado em {caminho_relatorio}")

if __name__ == "__main__":
    arquivo_escolhido = listar_arquivos_respostas()
    gerar_html(arquivo_escolhido)
