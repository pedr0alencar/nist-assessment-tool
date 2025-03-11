from cli.menu import exibir_menu_principal
from utils.file_handler import carregar_categorias

def main():
    """Inicia o programa carregando os dados e chamando o menu."""
    categorias = carregar_categorias()
    exibir_menu_principal(categorias)

if __name__ == "__main__":
    main()
