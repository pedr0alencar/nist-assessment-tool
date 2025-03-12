import os
from datetime import datetime
from utils.chart_utils import (
    gerar_grafico_interativo_barras,
    gerar_grafico_interativo_pizza
)

def compilar_estatisticas(respostas):
    """
    Recebe as 'respostas' de uma categoria:
     [ {controle, descricao, status}, ... ]
    Retorna dict com contagem de cada status, total e % de conformidade (considerando 'Em Conformidade').
    """
    status_counts = {}
    for resp in respostas:
        st = resp["status"]
        status_counts[st] = status_counts.get(st, 0) + 1

    total_controles = sum(status_counts.values())
    conformes = status_counts.get("Em Conformidade", 0)
    perc_conf = (conformes / total_controles * 100) if total_controles else 0.0

    return {
        "status_counts": status_counts,
        "total_controles": total_controles,
        "percentual_conformidade": perc_conf
    }

def gerar_relatorio_html_single(categoria, respostas, destino):
    """
    Gera um relatório HTML interativo (Plotly) para UMA categoria,
    incluindo textos explicativos, tabelas e gráficos (barras + pizza).
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Estatísticas
    stats = compilar_estatisticas(respostas)
    status_counts = stats["status_counts"]
    total = stats["total_controles"]
    perc_conf = stats["percentual_conformidade"]

    # Gera HTML dos gráficos
    barras_html = gerar_grafico_interativo_barras(status_counts, titulo=f"{categoria} - Barras")
    pizza_html = gerar_grafico_interativo_pizza(status_counts, titulo=f"{categoria} - Pizza")

    # Texto explicativo
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    texto_introducao = f"""
    <p>
        Este relatório apresenta uma <strong>avaliação detalhada</strong> da categoria 
        <strong>{categoria}</strong> no contexto do Framework NIST, realizada em 
        <strong>{data_atual}</strong>. 
        No total, foram analisados <strong>{total}</strong> controles,
        resultando em cerca de <strong>{perc_conf:.1f}%</strong> em 
        conformidade total.
    </p>

    <p>
        A <strong>conformidade total</strong> indica que as medidas e processos 
        estabelecidos atendem satisfatoriamente aos requisitos do controle.
        Já os status de <em>“Não Implementado”</em>, <em>“Planejado”</em>, 
        <em>“Em Implementação”</em> ou <em>“Parcialmente em Conformidade”</em> 
        apontam a necessidade de aperfeiçoar determinados pontos 
        para minimizar riscos potenciais.
    </p>

    <p>
        Este panorama específico para a categoria <strong>{categoria}</strong> 
        permite <em>identificar prioridades</em> e alocar recursos de forma
        mais eficiente, fortalecendo a postura de segurança cibernética da 
        organização. Recomenda-se revisar individualmente cada controle
        que não esteja em conformidade para elaborar planos de ação imediatos
        ou de longo prazo.
    </p>
    """

    # Monta HTML final
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_{categoria}_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    # Script Plotly (CDN)
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
    <p style="text-align:center;">Data/Hora: {data_atual}</p>

    <div class="intro">
        {texto_introducao}
    </div>

    <div class="charts">
        <div class="chart-container">
            <h3>Gráfico de Barras Interativo</h3>
            {barras_html}
        </div>
        <div class="chart-container">
            <h3>Gráfico de Pizza Interativo</h3>
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

    # Tabela de Controles
    for resp in respostas:
        c = resp["controle"]
        d = resp["descricao"]
        s = resp["status"]
        html += f"""
            <tr>
                <td>{c}</td>
                <td>{d}</td>
                <td>{s}</td>
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

    # Salva em disco
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    return caminho_arquivo


def gerar_relatorio_html_all(dados_por_categoria, destino):
    """
    Gera um relatório consolidado de TODAS as categorias, 
    com texto abrangente e gráficos interativos (barras + pizza) no escopo global.
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Estatísticas GLOBAIS
    status_counts_globais = {}
    total_controles = 0
    for cat, respostas in dados_por_categoria.items():
        for r in respostas:
            st = r["status"]
            status_counts_globais[st] = status_counts_globais.get(st, 0) + 1
        total_controles += len(respostas)

    conformes = status_counts_globais.get("Em Conformidade", 0)
    perc_conf_global = (conformes / total_controles * 100) if total_controles else 0.0

    # Gráficos (Plotly)
    barras_html = gerar_grafico_interativo_barras(status_counts_globais, "Todas as Categorias - Barras")
    pizza_html = gerar_grafico_interativo_pizza(status_counts_globais, "Todas as Categorias - Pizza")

    # Texto explicativo global
    qtd_categorias = len(dados_por_categoria.keys())
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    texto_introducao = f"""
    <p>
        Este relatório consolida a <strong>avaliação de {qtd_categorias} categorias</strong>
        no âmbito do Framework NIST, totalizando <strong>{total_controles}</strong> controles analisados.
        A coleta de dados foi realizada em <strong>{data_atual}</strong>, resultando em 
        aproximadamente <strong>{perc_conf_global:.1f}%</strong> de conformidade total.
    </p>

    <p>
        O objetivo principal é oferecer um <em>panorama global</em> do estado atual 
        de segurança da informação, destacando tanto os pontos fortes quanto 
        as áreas que demandam maior atenção. As informações aqui presentes 
        servem de <strong>base para priorização</strong> de iniciativas, definição 
        de metas de curto e longo prazo e <em>alocação eficiente de recursos</em>, 
        visando reforçar a postura de segurança cibernética da organização.
    </p>

    <p>
        É recomendável, ainda, que as equipes responsáveis revisem cada 
        <strong>categoria individual</strong> para aprofundar o entendimento 
        sobre controles específicos. Assim, obtém-se uma visão mais granular 
        para atuar diretamente sobre eventuais lacunas e riscos identificados, 
        garantindo maior <strong>maturidade e resiliência</strong> diante de 
        ameaças cibernéticas.
    </p>
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_TodasCategorias_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    plotly_cdn_script = """<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório - TODAS as Categorias</title>
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
    <p style="text-align:center;">Data: {data_atual}</p>

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

    # Seção para cada categoria
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
