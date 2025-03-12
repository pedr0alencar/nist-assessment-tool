import plotly.graph_objects as go

def gerar_grafico_interativo_barras(status_counts, titulo="Distribuição de Status"):
    """
    Gera um gráfico de barras interativo usando Plotly e retorna o HTML (sem <html> e <body>).
    """
    labels = list(status_counts.keys())
    values = list(status_counts.values())

    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=values, marker_color="#4C8EFA"))
    fig.update_layout(
        title=titulo,
        xaxis_title="Status",
        yaxis_title="Quantidade",
        template="plotly_white"
    )

    # Gera HTML do gráfico, sem <html> e <body>, mas contendo <div> + scripts
    chart_html = fig.to_html(full_html=False, include_plotlyjs=False)
    return chart_html

def gerar_grafico_interativo_pizza(status_counts, titulo="Distribuição de Status"):
    """
    Gera um gráfico de pizza (pie) interativo usando Plotly e retorna o HTML (sem <html> e <body>).
    """
    labels = list(status_counts.keys())
    values = list(status_counts.values())

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=labels, values=values, hole=0, hoverinfo='label+percent+value'))
    fig.update_layout(
        title=titulo,
        template="plotly_white"
    )

    chart_html = fig.to_html(full_html=False, include_plotlyjs=False)
    return chart_html
