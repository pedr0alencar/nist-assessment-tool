import os
from datetime import datetime

# Importa as funções para gerar gráficos base64
from utils.chart_utils import gerar_grafico_barras, gerar_grafico_pizza

def compilar_estatisticas(respostas):
    """
    Dado 'respostas' (lista de dicts com {controle, descricao, status}),
    retorna um dict com contagens de status, total e percentual de conformidade.
    """
    status_counts = {}
    for resp in respostas:
        st = resp["status"]
        status_counts[st] = status_counts.get(st, 0) + 1

    total_controles = sum(status_counts.values())

    # Exemplo de "Conformidade" = "Em Conformidade"
    # Você pode incluir "Parcialmente" também, se desejar
    em_conformidade = status_counts.get("Em Conformidade", 0)
    percentual_conformidade = 0.0
    if total_controles > 0:
        percentual_conformidade = (em_conformidade / total_controles) * 100

    return {
        "status_counts": status_counts,
        "total_controles": total_controles,
        "percentual_conformidade": percentual_conformidade
    }


def gerar_relatorio_html_single(categoria, respostas, destino):
    """
    Gera um relatório HTML para uma única categoria,
    com estatísticas, texto personalizado e gráficos (barras + pizza).
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Compilar estatísticas
    stats = compilar_estatisticas(respostas)
    status_counts = stats["status_counts"]
    total = stats["total_controles"]
    perc_conf = stats["percentual_conformidade"]

    # Gerar gráficos base64
    barras_base64 = gerar_grafico_barras(status_counts, titulo=f"{categoria} - Gráfico de Barras")
    pizza_base64 = gerar_grafico_pizza(status_counts, titulo=f"{categoria} - Gráfico de Pizza")

    # Nome do arquivo HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_{categoria}_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    # Texto de exemplo - ajustável
    texto_introducao = f"""
    <p>
        Este relatório apresenta os resultados da avaliação da categoria <strong>{categoria}</strong>.
        Foram analisados <strong>{total}</strong> controles, e 
        aproximadamente <strong>{perc_conf:.1f}%</strong> estão em conformidade completa.
    </p>
    <p>
        Com base nos dados coletados, é possível direcionar as iniciativas
        de segurança, priorizando os controles não implementados ou em
        implementação, visando aumentar a maturidade geral da organização
        na área de segurança cibernética.
    </p>
    """

    # Montagem do HTML
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
            padding: 12px;
            border: 1px solid #ccc;
            text-align: left;
        }}
        thead {{
            background-color: #eee;
        }}
        .status {{
            font-weight: bold;
        }}
        .charts {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .chart-container {{
            text-align: center;
            width: 45%;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 0.9em;
            color: #888;
        }}
        .intro {{
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>Relatório de Avaliação - {categoria}</h1>
    <p style="text-align:center;">Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>

    <div class="intro">
        {texto_introducao}
    </div>

    <div class="charts">
        <div class="chart-container">
            <h3>Gráfico de Barras</h3>
            <img src="data:image/png;base64,{barras_base64}" alt="Gráfico de Barras" />
        </div>
        <div class="chart-container">
            <h3>Gráfico de Pizza</h3>
            <img src="data:image/png;base64,{pizza_base64}" alt="Gráfico de Pizza" />
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

    # Acrescentar linhas da tabela de controles
    for resposta in respostas:
        controle = resposta["controle"]
        descricao = resposta["descricao"]
        status = resposta["status"]
        html_conteudo += f"""
            <tr>
                <td>{controle}</td>
                <td>{descricao}</td>
                <td class="status">{status}</td>
            </tr>
        """

    # Fechar tabela e corpo
    html_conteudo += """
        </tbody>
    </table>
    <div class="footer">
        <p>Gerado automaticamente pelo NIST Assessment Tool</p>
    </div>
</body>
</html>
"""

    # Salvar o arquivo HTML
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html_conteudo)

    return caminho_arquivo


def gerar_relatorio_html_all(dados_por_categoria, destino):
    """
    Gera um relatório HTML consolidado de TODAS as categorias,
    incluindo um texto introdutório e gráficos GLOBAIS, além de seções individuais.
    'dados_por_categoria' é um dict:
      {
        "Governar": [ {controle, descricao, status}, ... ],
        "Identificar": [ ... ],
        ...
      }
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Calcular estatísticas GLOBAIS
    status_counts_globais = {}
    total_controles = 0

    for cat, respostas in dados_por_categoria.items():
        for r in respostas:
            st = r["status"]
            status_counts_globais[st] = status_counts_globais.get(st, 0) + 1
        total_controles += len(respostas)

    # Porcentagem global de conformidade
    em_conformidade_global = status_counts_globais.get("Em Conformidade", 0)
    perc_conf_global = 0
    if total_controles > 0:
        perc_conf_global = (em_conformidade_global / total_controles) * 100

    # Gerar gráficos GLOBAIS
    barras_global = gerar_grafico_barras(status_counts_globais, titulo="Todas as Categorias - Barras")
    pizza_global = gerar_grafico_pizza(status_counts_globais, titulo="Todas as Categorias - Pizza")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_TodasCategorias_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    texto_introducao = f"""
    <p>
        Este relatório consolida as avaliações de <strong>{len(dados_por_categoria.keys())}</strong> categorias.
        Ao todo, foram avaliados <strong>{total_controles}</strong> controles,
        com aproximadamente <strong>{perc_conf_global:.1f}%</strong> em conformidade.
    </p>
    <p>
        Este panorama global ajuda a priorizar as áreas que mais necessitam
        de melhorias ou correções, bem como a registrar o progresso
        ao longo do tempo. Com base nessas informações, a organização
        pode direcionar esforços e recursos de maneira mais eficaz.
    </p>
    """

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório - TODAS as Categorias</title>
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
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
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
        .charts {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .chart-container {{
            text-align: center;
            width: 45%;
        }}
    </style>
</head>
<body>
    <h1>Relatório de Avaliação - TODAS AS CATEGORIAS</h1>
    <p style="text-align:center;">Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>

    <div class="intro">
        {texto_introducao}
    </div>

    <div class="charts">
        <div class="chart-container">
            <h3>Gráfico Global (Barras)</h3>
            <img src="data:image/png;base64,{barras_global}" alt="Gráfico Barras Global"/>
        </div>
        <div class="chart-container">
            <h3>Gráfico Global (Pizza)</h3>
            <img src="data:image/png;base64,{pizza_global}" alt="Gráfico Pizza Global"/>
        </div>
    </div>
"""

    # Seções para cada categoria
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
