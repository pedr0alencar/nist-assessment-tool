# src/utils/report_generator.py
import os
from datetime import datetime
from utils.chart_utils import gerar_grafico_barras, gerar_grafico_pizza

def gerar_relatorio_html_single(categoria, respostas, destino="src/reports"):
    """
    Gera um relatório HTML para uma única categoria,
    contendo tabela de controles e gráficos (barra e pizza).
    """

    if not os.path.exists(destino):
        os.makedirs(destino)

    # Montar contagens de status
    status_counts = {}
    for resp in respostas:
        st = resp["status"]
        status_counts[st] = status_counts.get(st, 0) + 1

    # Gerar gráficos em base64
    barras_base64 = gerar_grafico_barras(status_counts, titulo=f"{categoria} - Barras")
    pizza_base64 = gerar_grafico_pizza(status_counts, titulo=f"{categoria} - Pizza")

    # Montar corpo HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_{categoria}_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    html_conteudo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório - {categoria}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f9f9f9;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid #ccc;
            text-align: left;
        }}
        thead {{
            background-color: #eee;
        }}
        .charts {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .chart-container {{
            text-align: center;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 0.85em;
            color: #888;
        }}
    </style>
</head>
<body>
    <h1>Relatório de Avaliação - {categoria}</h1>
    <p>Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
    <table>
        <thead>
            <tr>
                <th>Controle</th>
                <th>Descrição</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
    """

    for resp in respostas:
        controle = resp["controle"]
        descricao = resp["descricao"]
        status = resp["status"]
        html_conteudo += f"""
            <tr>
                <td>{controle}</td>
                <td>{descricao}</td>
                <td>{status}</td>
            </tr>
        """

    html_conteudo += """
        </tbody>
    </table>

    <div class="charts">
        <div class="chart-container">
            <h3>Gráfico de Barras</h3>
            <img src="data:image/png;base64,""" + barras_base64 + """">
        </div>
        <div class="chart-container">
            <h3>Gráfico de Pizza</h3>
            <img src="data:image/png;base64,""" + pizza_base64 + """">
        </div>
    </div>

    <div class="footer">
        <p>Gerado automaticamente pelo NIST Assessment Tool</p>
    </div>
</body>
</html>
"""

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html_conteudo)

    return caminho_arquivo


def gerar_relatorio_html_all(dados_por_categoria, destino="src/reports"):
    """
    Gera um relatório HTML englobando todas as categorias.
    'dados_por_categoria' deve ser um dict:
      {
        "Governar": [ {controle, descricao, status}, ... ],
        "Identificar": [ ... ],
        ...
      }
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Vamos fazer uma contagem global de status
    status_counts_globais = {}

    for cat, respostas in dados_por_categoria.items():
        for resp in respostas:
            st = resp["status"]
            status_counts_globais[st] = status_counts_globais.get(st, 0) + 1

    # Gerar gráficos globais
    barras_global = gerar_grafico_barras(status_counts_globais, titulo="Todas as Categorias - Barras")
    pizza_global = gerar_grafico_pizza(status_counts_globais, titulo="Todas as Categorias - Pizza")

    # Montar HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_TodasCategorias_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório - Todas as Categorias</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f9f9f9;
        }}
        h1 {{
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid #ccc;
            text-align: left;
        }}
        thead {{
            background-color: #eee;
        }}
        .charts {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .chart-container {{
            text-align: center;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 0.85em;
            color: #888;
        }}
        .categoria-title {{
            margin-top: 40px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>Relatório de Avaliação - TODAS AS CATEGORIAS</h1>
    <p>Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
    <div class="charts">
        <div class="chart-container">
            <h3>Gráfico de Barras (Global)</h3>
            <img src="data:image/png;base64,{barras_global}">
        </div>
        <div class="chart-container">
            <h3>Gráfico de Pizza (Global)</h3>
            <img src="data:image/png;base64,{pizza_global}">
        </div>
    </div>
"""

    # Agora adicionamos tabelas para cada categoria, se quiser
    for cat, respostas in dados_por_categoria.items():
        html += f"""
        <h2 class="categoria-title">{cat}</h2>
        <table>
        <thead>
          <tr>
            <th>Controle</th>
            <th>Descrição</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
        """
        for r in respostas:
            html += f"""
            <tr>
                <td>{r["controle"]}</td>
                <td>{r["descricao"]}</td>
                <td>{r["status"]}</td>
            </tr>
            """
        html += "</tbody></table>"

    html += """
    <div class="footer">
        <p>Gerado automaticamente pelo NIST Assessment Tool</p>
    </div>
</body>
</html>
"""

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    return caminho_arquivo
