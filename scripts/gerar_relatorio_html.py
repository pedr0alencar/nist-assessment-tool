import json
import os
from datetime import datetime

RELATORIO_DIR = '../relatorios/'

def gerar_html(empresa):
    nome_arquivo = empresa.lower().replace(' ', '_')
    caminho_respostas = f"../respostas/{nome_arquivo}_respostas.json"

    # Carrega os dados da avaliação
    with open(caminho_respostas, 'r', encoding='utf-8') as file:
        dados = json.load(file)

    total_controles = 0
    resultados = {}
    for cat, controles in dados["categorias"].items():
        for controle in controles:
            resposta = controle["avaliacao"]
            resultados[resposta] = resultados.get(resposta, 0) + 1
            total_controles += 1

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Avaliação - {empresa}</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Relatório de Avaliação - {empresa}</h1>
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

    diretorio = "../relatorios/"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    caminho_relatorio = f"{diretorio}/{nome_arquivo}_relatorio.html"
    with open(caminho_relatorio, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    print(f"\n✅ Relatório HTML gerado em {caminho_relatorio}")

if __name__ == "__main__":
    empresa = input("Nome da Empresa: ")
    gerar_html(empresa)
