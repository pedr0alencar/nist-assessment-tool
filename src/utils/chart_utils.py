import base64
import io
import matplotlib.pyplot as plt

def gerar_grafico_barras(status_counts, titulo="Distribuição de Status"):
    """
    Gera um gráfico de barras usando matplotlib e retorna a imagem em base64.
    status_counts: dict {status: quantidade}
    titulo: título do gráfico
    """
    labels = list(status_counts.keys())
    values = list(status_counts.values())

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values, color="#4C8EFA")
    ax.set_title(titulo)
    ax.set_ylabel("Quantidade")
    ax.set_xlabel("Status")
    plt.xticks(rotation=45, ha="right")

    # Ajustar layout e salvar em buffer
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    # Converter em base64
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return img_base64


def gerar_grafico_pizza(status_counts, titulo="Distribuição de Status"):
    """
    Gera um gráfico de pizza (pie chart) usando matplotlib e retorna a imagem em base64.
    status_counts: dict {status: quantidade}
    titulo: título do gráfico
    """
    labels = list(status_counts.keys())
    values = list(status_counts.values())

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(titulo)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return img_base64
