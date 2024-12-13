from FCApp import FlashcardApp  # Assurez-vous que c'est la classe FlashcardApp
from DB import creer_base_de_donnees
from consoleFC import *


def launch_gui():
    """
    Placeholder for GUI launch function.
    Replace this with actual GUI implementation when available.
    """
    try:
        import tkinter as tk
        from tkinter import messagebox

        def show_not_implemented():
            messagebox.showinfo("Information", "Interface graphique non encore implémentée.")

        root = tk.Tk()
        root.title("Flashcard App")
        root.geometry("400x300")

        label = tk.Label(root, text="Interface Graphique en Développement", font=("Arial", 14))
        label.pack(pady=20)

        btn = tk.Button(root, text="OK", command=root.destroy)
        btn.pack()

        root.mainloop()
    except ImportError:
        print("Tkinter n'est pas installé. Impossible de lancer l'interface graphique.")
        print("Installez tkinter ou utilisez le mode console.")


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
