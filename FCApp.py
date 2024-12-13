import tkinter as tk
from tkinter import messagebox, ttk

from flashcard_logic import FlashcardLogic


class FlashcardApp:
    def __init__(self):
        # Create the logic instance
        self.logic = FlashcardLogic()

        # Create the main window
        self.window = tk.Tk()
        self.window.title("FlashLearn")
        self.window.geometry("1000x700")
        self.window.configure(bg="#f0f4f8")

        # UI-specific state variables
        self.is_answer_shown = False
        self.test_mode = False
        self.test_questions = []
        self.current_question_index = 0
        self.correct_answers = 0

        # Create the UI
        self.create_ui()

    def create_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.window, bg="#f0f4f8")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Titre de l'application
        title_label = tk.Label(main_frame, text="FlashLearn",
                               font=("Arial", 24, "bold"),
                               bg="#f0f4f8",
                               fg="#2c3e50")
        title_label.pack(pady=10)

        # Statistiques en haut
        stats_frame = tk.Frame(main_frame, bg="#f0f4f8")
        stats_frame.pack(fill="x", pady=10)

        self.stats_label = tk.Label(stats_frame,
                                    text="0/0 cartes",
                                    font=("Arial", 12),
                                    bg="#f0f4f8")
        self.stats_label.pack()

        # Carte de flashcard
        self.card_frame = tk.Frame(main_frame,
                                   bg="white",
                                   highlightbackground="#a0a0a0",
                                   highlightthickness=1,
                                   bd=0)
        self.card_frame.pack(expand=True, fill="both", pady=20)

        self.card_text = tk.Label(self.card_frame,
                                  text="Commencez à étudier",
                                  font=("Arial", 24, "bold"),
                                  bg="white",
                                  wraplength=800)
        self.card_text.pack(expand=True, fill="both", padx=20, pady=20)

        # Boutons de contrôle
        control_frame = tk.Frame(main_frame, bg="#f0f4f8")
        control_frame.pack(fill="x", pady=10)

        buttons = [
            ("Précédent", self.previous_card, "gray"),
            ("Inconnu", self.mark_unknown, "red"),
            ("Montrer Réponse", self.toggle_answer, "orange"),
            ("Connu", self.mark_known, "green"),
            ("Ajouter une carte", self.add_flashcard, "blue")
        ]

        for text, command, color in buttons:
            btn = tk.Button(control_frame,
                            text=text,
                            command=command,
                            bg=color,
                            fg="white",
                            font=("Arial", 14))
            btn.pack(side="left", expand=True, padx=5)

        # Menus
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # Menu Thèmes
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Thèmes", menu=theme_menu)
        theme_menu.add_command(label="Charger Thème", command=self.load_theme_dialog)
        theme_menu.add_command(label="Statistiques", command=self.show_statistics)

        # Menu Test
        test_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Test", menu=test_menu)
        test_menu.add_command(label="Passer le Test", command=self.start_test)

    def show_current_card(self):
        # Retrieve current flashcard from logic class
        card = self.logic.get_current_card()
        if card:
            self.card_text.config(text=card["question"], fg="black")
            self.is_answer_shown = False
            self.update_stats()
        else:
            self.show_end_screen()

    def toggle_answer(self):
        card = self.logic.get_current_card()
        if not card:
            return

        if self.is_answer_shown:
            self.card_text.config(text=card["question"], fg="black")
            self.is_answer_shown = False
        else:
            self.card_text.config(text=card["answer"], fg="blue")
            self.is_answer_shown = True

    def mark_known(self):
        # Delegate to logic class
        self.logic.mark_current_card_as_known()
        self.show_current_card()

    def mark_unknown(self):
        # Delegate to logic class
        self.logic.mark_current_card_as_unknown()
        self.show_current_card()

    def previous_card(self):
        # Delegate to logic class
        self.logic.previous_card()
        self.show_current_card()

    def update_stats(self):
        total = self.logic.get_total_cards()
        known = self.logic.get_known_cards_count()
        stats_text = f"Cartes connues : {known}/{total}"
        self.stats_label.config(text=stats_text)

    def show_end_screen(self):
        end_window = tk.Toplevel(self.window)
        end_window.title("Étude terminée")
        end_window.geometry("400x300")

        tk.Label(end_window, text="Félicitations !", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(end_window, text="Vous avez terminé toutes les cartes.", font=("Arial", 14)).pack(pady=10)

        tk.Button(end_window, text="Recommencer", command=lambda: [self.load_cards(), end_window.destroy()]).pack(
            pady=10)
        tk.Button(end_window, text="Fermer", command=end_window.destroy).pack(pady=10)

    def load_theme_dialog(self):
        theme_window = tk.Toplevel(self.window)
        theme_window.title("Charger un Thème")
        theme_window.geometry("400x200")

        tk.Label(theme_window, text="Sélectionnez un thème :").pack(pady=10)

        themes = self.logic.get_all_themes()
        theme_var = tk.StringVar()

        theme_dropdown = ttk.Combobox(theme_window, textvariable=theme_var, values=list(themes))
        theme_dropdown.pack(pady=10)

        def load_theme():
            selected_theme = theme_var.get()
            self.logic.load_theme(selected_theme)
            self.show_current_card()
            theme_window.destroy()

        tk.Button(theme_window, text="Charger", command=load_theme).pack(pady=10)

    def show_statistics(self):
        stats_window = tk.Toplevel(self.window)
        stats_window.title("Statistiques détaillées")
        stats_window.geometry("500x400")

        total = self.logic.get_total_cards()
        known_count = self.logic.get_known_cards_count()
        known_percent = (known_count / total * 100) if total > 0 else 0

        stats = [
            f"Total de cartes : {total}",
            f"Cartes connues : {known_count} ({known_percent:.1f}%)",
            f"Cartes restantes : {self.logic.get_unknown_cards_count()}"
        ]

        for stat in stats:
            tk.Label(stats_window, text=stat, font=("Arial", 14)).pack(pady=5)

    def start_test(self):
        if self.logic.get_total_cards() < 10:
            messagebox.showinfo("Test", "Il y a moins de 10 cartes disponibles pour passer le test.")
            return

        self.test_mode = True
        self.test_questions = self.logic.prepare_test()
        self.current_question_index = 0
        self.correct_answers = 0
        self.ask_next_question()

    def ask_next_question(self):
        if self.current_question_index < len(self.test_questions):
            card = self.test_questions[self.current_question_index]
            question = card["question"]

            # Créer une fenêtre de question
            self.test_window = tk.Toplevel(self.window)
            self.test_window.title(f"Question {self.current_question_index + 1}/10")
            self.test_window.geometry("500x300")

            tk.Label(self.test_window, text=question, font=("Arial", 18, "bold")).pack(pady=20)

            answer_entry = tk.Entry(self.test_window, font=("Arial", 14), width=40)
            answer_entry.pack(pady=10)

            def check_answer():
                answer = answer_entry.get().strip()
                if self.logic.check_test_answer(self.current_question_index, answer):
                    self.correct_answers += 1

                self.current_question_index += 1
                self.test_window.destroy()
                self.ask_next_question()

            tk.Button(self.test_window, text="Soumettre", command=check_answer).pack(pady=20)
        else:
            self.show_test_results()

    def show_test_results(self):
        result_window = tk.Toplevel(self.window)
        result_window.title("Résultats du Test")
        result_window.geometry("400x300")

        score = self.correct_answers
        tk.Label(result_window, text=f"Vous avez {score} / 10 bonnes réponses.", font=("Arial", 18)).pack(pady=20)
        tk.Button(result_window, text="Fermer", command=result_window.destroy).pack(pady=20)

    def add_flashcard(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Ajouter une carte")
        add_window.geometry("400x350")

        tk.Label(add_window, text="Entrez la question :").pack(pady=10)
        question_entry = tk.Entry(add_window, font=("Arial", 14), width=40)
        question_entry.pack(pady=10)

        tk.Label(add_window, text="Entrez la réponse :").pack(pady=10)
        answer_entry = tk.Entry(add_window, font=("Arial", 14), width=40)
        answer_entry.pack(pady=10)

        tk.Label(add_window, text="Sélectionnez un thème :").pack(pady=10)
        themes = self.logic.get_all_themes()
        theme_var = tk.StringVar()
        theme_dropdown = ttk.Combobox(add_window, textvariable=theme_var, values=list(themes))
        theme_dropdown.pack(pady=10)

        def save_flashcard():
            question = question_entry.get()
            answer = answer_entry.get()
            theme = theme_var.get()

            if question and answer and theme:
                if self.logic.add_flashcard(question, answer, theme):
                    messagebox.showinfo("Succès", "Carte ajoutée avec succès")
                    add_window.destroy()
                    self.load_cards()  # Recharge les cartes
                else:
                    messagebox.showwarning("Erreur", "Impossible d'ajouter la carte.")
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

        tk.Button(add_window, text="Ajouter", command=save_flashcard).pack(pady=10)

    def load_cards(self):
        # Delegate to logic class to load all cards
        self.logic.load_all_cards()
        self.show_current_card()

    def run(self):
        # Initial card load
        self.load_cards()
        self.window.mainloop()


def run_app():
    app = FlashcardApp()
    app.run()
