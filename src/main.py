def main():
    print("\nNIST Cybersecurity Assessment Tool\n")
    print("Categorias Disponíveis:")
    categorias = [
        "Governar",
        "Identificar",
        "Proteger",
        "Detectar",
        "Responder",
        "Recuperar"
    ]

    for categoria in categorias:
        print(f"- {categoria}")

if __name__ == "__main__":
    main()
