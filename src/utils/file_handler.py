import json
import os

DATA_DIR = "src/data/"

def carregar_categorias():
    """Carrega todos os arquivos JSON das categorias e retorna um dicionário."""
    categorias = {}
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            path = os.path.join(DATA_DIR, filename)
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                categorias[data["categoria"]] = data
    return categorias
