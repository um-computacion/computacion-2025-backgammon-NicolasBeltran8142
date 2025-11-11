from cli.cli import iniciar_juego_cli
from pygame_ui.ui import ejecutar_pygame

def main():
    """
    Main function to run the Backgammon game.
    Allows the user to choose between the CLI and Pygame UI.
    """
    while True:
        print("\nSelect the game mode:")
        print("1. Command Line Interface (CLI)")
        print("2. Pygame User Interface (UI)")
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            iniciar_juego_cli()
            break
        elif choice == "2":
            try:
                ejecutar_pygame()
            except ImportError:
                print(
                    "\nError: Pygame is not installed. The graphical interface cannot be run."
                )
                print("Please install it by running: pip install pygame")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
