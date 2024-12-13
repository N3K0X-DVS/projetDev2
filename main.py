from FCApp import FlashcardApp  # Assurez-vous que c'est la classe FlashcardApp
from DB import creer_base_de_donnees
from consoleFC import *

def main():
    import argparse

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Flashcard Learning Application")
    parser.add_argument('--mode',
                        choices=['console', 'gui'],
                        default='gui',
                        help='Mode de lancement de l\'application (console par défaut)')

    # Parse arguments
    args = parser.parse_args()

    # Launch the appropriate mode
    if args.mode == 'console':
        main_menu()
    elif args.mode == 'gui':
        run_app()

def run_app():
    app = FlashcardApp()
    app.run()  # Lance l'application

if __name__ == "__main__":
    creer_base_de_donnees()
    main()
