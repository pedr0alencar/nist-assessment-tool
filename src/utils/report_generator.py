import os
from datetime import datetime
from utils.chart_utils import (
    gerar_grafico_interativo_barras,
    gerar_grafico_interativo_pizza
)

def compilar_estatisticas(respostas):
    status_counts = {}
    for resp in respostas:
        st = resp["status"]
        status_counts[st] = status_counts.get(st, 0) + 1

    total = sum(status_counts.values())
    conformes = status_counts.get("Em Conformidade", 0)
    perc_conf = (conformes / total * 100) if total else 0.0

    return {
        "status_counts": status_counts,
        "total_controles": total,
        "percentual_conformidade": perc_conf
    }

def gerar_relatorio_html_single(categoria, respostas, destino):
    """
    Gera relatório interativo usando Plotly (barras + pizza).
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    stats = compilar_estatisticas(respostas)
    status_counts = stats["status_counts"]
    total = stats["total_controles"]
    perc_conf = stats["percentual_conformidade"]

    # Gerar HTML dos gráficos interativos (sem <html>)
    barras_html = gerar_grafico_interativo_barras(status_counts, titulo=f"{categoria} - Barras")
    pizza_html = gerar_grafico_interativo_pizza(status_counts, titulo=f"{categoria} - Pizza")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_{categoria}_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    # Texto de exemplo
    texto_introducao = f"""
    <p>
        Esta é uma avaliação da categoria <strong>{categoria}</strong>.
        No total, analisamos <strong>{total}</strong> controles, e 
        <strong>{perc_conf:.1f}%</strong> estão totalmente em conformidade.
    </p>
    """

    # Incluir script Plotly (CDN) APENAS uma vez
    plotly_cdn_script = """<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório - {categoria}</title>
    {plotly_cdn_script}
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f9f9f9;
        }}
        h1 {{
            text-align: center;
        }}
        .intro {{
            margin-top: 20px;
        }}
        .charts {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .chart-container {{
            width: 45%;
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
        .footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 0.85em;
            color: #888;
        }}
    </style>
</head>
<body>
    <h1>Relatório - {categoria}</h1>
    <p style="text-align:center;">Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>

    <div class="intro">
        {texto_introducao}
    </div>

    <div class="charts">
        <div class="chart-container">
            <h3>Gráfico de Barras (Interativo)</h3>
            {barras_html}
        </div>
        <div class="chart-container">
            <h3>Gráfico de Pizza (Interativo)</h3>
            {pizza_html}
        </div>
    </div>

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

    html += """
      </tbody>
    </table>

    <div class="footer">
        <p>Gerado automaticamente pelo NIST Assessment Tool - Plotly Edition</p>
    </div>
</body>
</html>
"""

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    return caminho_arquivo


def gerar_relatorio_html_all(dados_por_categoria, destino):
    """
    Relatório com TODOS os gráficos interativos. 
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Calcular estatísticas globais
    status_counts_globais = {}
    total_controles = 0
    for cat, respostas in dados_por_categoria.items():
        for r in respostas:
            st = r["status"]
            status_counts_globais[st] = status_counts_globais.get(st, 0) + 1
        total_controles += len(respostas)

    conformes_global = status_counts_globais.get("Em Conformidade", 0)
    perc_conf_global = (conformes_global / total_controles * 100) if total_controles else 0.0

    # Plotly HTML
    barras_html = gerar_grafico_interativo_barras(status_counts_globais, "Todas as Categorias - Barras")
    pizza_html = gerar_grafico_interativo_pizza(status_counts_globais, "Todas as Categorias - Pizza")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_TodasCategorias_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    texto_introducao = f"""
    <p>
        Este relatório consolida as avaliações de <strong>{len(dados_por_categoria.keys())}</strong> categorias.
        Ao todo, foram avaliados <strong>{total_controles}</strong> controles,
        com aproximadamente <strong>{perc_conf_global:.1f}%</strong> em conformidade total.
    </p>
    """

    plotly_cdn_script = """<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório - Todas as Categorias</title>
    {plotly_cdn_script}
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f9f9f9;
        }}
        h1 {{
            text-align: center;
        }}
        .intro {{
            margin-top: 20px;
        }}
        .charts {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .chart-container {{
            width: 45%;
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
        .footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 0.85em;
            color: #888;
        }}
        .categoria-title {{
            margin-top: 40px;
            font-weight: bold;
            font-size: 1.2em;
        }}
    </style>
</head>
<body>
    <h1>Relatório de Avaliação - TODAS AS CATEGORIAS</h1>
    <p style="text-align:center;">Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>

    <div class="intro">
        {texto_introducao}
    </div>

    <div class="charts">
        <div class="chart-container">
            <h3>Gráfico Global (Barras) Interativo</h3>
            {barras_html}
        </div>
        <div class="chart-container">
            <h3>Gráfico Global (Pizza) Interativo</h3>
            {pizza_html}
        </div>
    </div>
"""

    # Seções de cada categoria
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
        <p>Gerado automaticamente pelo NIST Assessment Tool - Plotly Edition</p>
    </div>
</body>
</html>
"""

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    return caminho_arquivo
