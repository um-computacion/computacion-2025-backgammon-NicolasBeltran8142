from cli.cli import ejecutar_cli

def main():
    """
    Main function to run the Backgammon game.
    Allows the user to choose between the CLI and Pygame UI.
    """
    while True:
        print("\nSelect the game mode:")
        print("1. Command Line Interface (CLI)")
        print("2. Pygame User Interface (GUI)")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            ejecutar_cli()
            break
        elif choice == '2':
            try:
                from pygame_ui.ui import ejecutar_pygame
                ejecutar_pygame()
            except ImportError:
                print("\nError: Pygame is not installed. The graphical interface cannot be run.")
                print("Please install it by running: pip install pygame")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
