import os
from datetime import datetime

def gerar_relatorio_html(categoria, respostas, destino="src/reports"):
    """
    Gera um relatório HTML simples contendo os controles avaliados.
    :param categoria: Nome da categoria avaliada
    :param respostas: Lista de dicionários com {controle, descricao, status}
    :param destino: Diretório onde salvar o arquivo HTML
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Nome do arquivo (ex.: relatorio_Governar_20230315_1234.html)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"relatorio_{categoria}_{timestamp}.html"
    caminho_arquivo = os.path.join(destino, nome_arquivo)

    # Aqui criamos um HTML básico
    # Adicionei CSS inline para deixar mais apresentável
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
            background-color: #ddd;
        }}
        .status {{
            font-weight: bold;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 0.9em;
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

    # Acrescentar linhas da tabela
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
