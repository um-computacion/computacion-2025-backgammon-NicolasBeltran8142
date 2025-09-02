from core.dados import Dados

def main():
    dados = Dados()
    valores = dados.tirar()
    print(f"Tirada: {valores}")

if __name__ == "__main__":
    main()
