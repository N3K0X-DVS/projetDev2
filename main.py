from interface import FlashcardApp  # Assurez-vous que c'est la classe FlashcardApp
from DB import creer_base_de_donnees

def run_app():
    app = FlashcardApp()
    app.run()  # Lance l'application

if __name__ == "__main__":
    creer_base_de_donnees()
    run_app()
