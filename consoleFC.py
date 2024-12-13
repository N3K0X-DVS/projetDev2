import random
from typing import List, Dict, Optional


# Mock Database Functions (since the original DB module is not provided)
class MockDB:
    _fiches = [
        (1, "Qu'est-ce que Python?", "Un langage de programmation interprété", "Programmation", False),
        (2, "Qu'est-ce qu'une variable?", "Un espace de stockage en mémoire pour une valeur", "Programmation", False),
        (3, "Définir un tuple", "Une collection ordonnée et immuable", "Python", False),
        (
        4, "Qu'est-ce que l'héritage?", "Un mécanisme de création de classe basé sur une autre classe", "Programmation",
        False),
        (5, "Définir une liste en Python", "Une collection ordonnée et modifiable", "Python", False)
    ]

    @classmethod
    def recuperer_all_info_fiches(cls):
        return cls._fiches

    @classmethod
    def recuperer_fiches_par_theme(cls, theme):
        return [fiche for fiche in cls._fiches if fiche[3] == theme]

    @classmethod
    def ajouter_fiche(cls, question, reponse, theme):
        new_id = len(cls._fiches) + 1
        cls._fiches.append((new_id, question, reponse, theme, False))


class FlashcardLogic:
    def __init__(self):
        # Initialize card collections
        self.all_flashcards: List[Dict[str, str]] = []
        self.current_flashcards: List[Dict[str, str]] = []
        self.current_card_index: int = 0

        # Test mode variables
        self.test_mode: bool = False
        self.test_questions: List[Dict[str, str]] = []
        self.current_question_index: int = 0
        self.correct_answers: int = 0

    def load_all_cards(self) -> None:
        """
        Load all flashcards into the manager.
        """
        fiches = MockDB.recuperer_all_info_fiches()

        # Convert database tuples to dictionary format
        self.all_flashcards = [
            {"question": fiche[1], "answer": fiche[2], "theme": fiche[3], "known": False}
            for fiche in fiches
        ]

        # Set initial current flashcards to unknown cards
        self.current_flashcards = [card for card in self.all_flashcards if not card["known"]]
        self.current_card_index = 0

    def load_theme(self, theme: str) -> None:
        """
        Load flashcards for a specific theme.

        :param theme: Theme to load
        """
        fiches = MockDB.recuperer_fiches_par_theme(theme)

        # Convert database tuples to dictionary format
        self.all_flashcards = [
            {"question": fiche[1], "answer": fiche[2], "theme": fiche[3], "known": False}
            for fiche in fiches
        ]

        # Set initial current flashcards to unknown cards
        self.current_flashcards = [card for card in self.all_flashcards if not card["known"]]
        self.current_card_index = 0

    def get_current_card(self) -> Optional[Dict[str, str]]:
        """
        Get the current flashcard.

        :return: Current flashcard dictionary or None if no cards exist
        """
        if not self.current_flashcards:
            return None
        return self.current_flashcards[self.current_card_index]

    def previous_card(self) -> None:
        """
        Move to the previous card, wrapping around to the end if at the start.
        """
        if not self.current_flashcards:
            return

        self.current_card_index = (self.current_card_index - 1) % len(self.current_flashcards)

    def mark_current_card_as_known(self) -> None:
        """
        Mark the current card as known.
        """
        if not self.current_flashcards:
            return

        # Mark the card as known
        self.current_flashcards[self.current_card_index]["known"] = "True"

        # Remove the card from current flashcards
        self.current_flashcards.pop(self.current_card_index)

        # Adjust index if it's now out of range
        if self.current_card_index >= len(self.current_flashcards):
            self.current_card_index = 0

    def mark_current_card_as_unknown(self) -> None:
        """
        Move the current card to the end of the list.
        """
        if not self.current_flashcards:
            return

        # Move current card to the end of the list
        card = self.current_flashcards[self.current_card_index]
        self.current_flashcards.append(self.current_flashcards.pop(self.current_card_index))

    def get_total_cards(self) -> int:
        """
        Get total number of cards.

        :return: Total number of cards
        """
        return len(self.all_flashcards)

    def get_known_cards_count(self) -> int:
        """
        Get the number of known cards.

        :return: Number of known cards
        """
        return len([card for card in self.all_flashcards if card["known"]])

    def get_unknown_cards_count(self) -> int:
        """
        Get the number of unknown cards.

        :return: Number of unknown cards
        """
        return len([card for card in self.all_flashcards if not card["known"]])

    def get_all_themes(self) -> List[str]:
        """
        Get all unique themes.

        :return: List of unique themes
        """
        return list(set(card["theme"] for card in self.all_flashcards))

    def prepare_test(self, num_questions: int = 10) -> List[Dict[str, str]]:
        """
        Prepare a test with a specified number of questions.

        :param num_questions: Number of questions in the test
        :return: List of test questions
        """
        # Get unknown cards
        unknown_cards = [card for card in self.all_flashcards if not card["known"]]

        if len(unknown_cards) < num_questions:
            raise ValueError("Not enough unknown cards to prepare test")

        self.test_mode = True
        self.test_questions = random.sample(unknown_cards, num_questions)
        self.current_question_index = 0
        self.correct_answers = 0

        return self.test_questions

    def check_test_answer(self, question_index: int, user_answer: str) -> bool:
        """
        Check if the user's answer matches the test question's answer.

        :param question_index: Index of the current question
        :param user_answer: User's submitted answer
        :return: True if answer is correct, False otherwise
        """
        if question_index >= len(self.test_questions):
            return False

        current_question = self.test_questions[question_index]
        is_correct = user_answer.strip().lower() == current_question['answer'].strip().lower()

        if is_correct:
            self.correct_answers += 1

        return is_correct

    def add_flashcard(self, question: str, answer: str, theme: str) -> bool:
        """
        Add a new flashcard to the collection.

        :param question: Question text
        :param answer: Answer text
        :param theme: Theme of the flashcard
        :return: True if successfully added, False otherwise
        """
        try:
            # Add to mock database
            MockDB.ajouter_fiche(question, answer, theme)

            # Reload flashcards to include the new one
            self.load_all_cards()

            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de la fiche : {e}")
            return False


def main_menu():
    """
    Main menu for the flashcard application.
    """
    flashcard_manager = FlashcardLogic()
    flashcard_manager.load_all_cards()

    while True:
        print("\n--- APPLICATION FLASHCARDS ---")
        print("1. Réviser les cartes")
        print("2. Mode test")
        print("3. Statistiques")
        print("4. Ajouter une carte")
        print("5. Choisir un thème")
        print("6. Quitter")

        choix = input("Entrez votre choix (1-6) : ")

        if choix == '1':
            revise_cards(flashcard_manager)
        elif choix == '2':
            test_mode(flashcard_manager)
        elif choix == '3':
            show_statistics(flashcard_manager)
        elif choix == '4':
            add_flashcard(flashcard_manager)
        elif choix == '5':
            choose_theme(flashcard_manager)
        elif choix == '6':
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Réessayez.")


def revise_cards(flashcard_manager):
    """
    Card revision mode.
    """
    if not flashcard_manager.current_flashcards:
        print("Aucune carte à réviser.")
        return

    while flashcard_manager.current_flashcards:
        current_card = flashcard_manager.get_current_card()
        print(f"\nCarte {flashcard_manager.current_card_index + 1}/{len(flashcard_manager.current_flashcards)}")
        print(f"Question: {current_card['question']}")

        input("Appuyez sur Entrée pour voir la réponse...")
        print(f"Réponse: {current_card['answer']}")

        # Feedback and card management
        while True:
            choice = input("Connaissez-vous cette carte ? (O/N/P) : ").upper()
            if choice == 'O':
                flashcard_manager.mark_current_card_as_known()
                break
            elif choice == 'N':
                flashcard_manager.mark_current_card_as_unknown()
                break
            elif choice == 'P':
                flashcard_manager.previous_card()
                break
            else:
                print("Choix invalide. Utilisez O (Oui), N (Non), ou P (Précédent).")

        if not flashcard_manager.current_flashcards:
            print("Toutes les cartes ont été révisées !")
            break


def test_mode(flashcard_manager):
    """
    Test mode for flashcards.
    """
    try:
        num_questions = int(input("Nombre de questions pour le test (défaut 5) : ") or 5)
        test_questions = flashcard_manager.prepare_test(num_questions)

        for i, question in enumerate(test_questions, 1):
            print(f"\nQuestion {i}/{len(test_questions)}")
            print(f"Question: {question['question']}")

            user_answer = input("Votre réponse : ")
            is_correct = flashcard_manager.check_test_answer(i - 1, user_answer)

            if is_correct:
                print("Correct ✓")
            else:
                print(f"Incorrect ✗ - Réponse correcte : {question['answer']}")

        # Test results
        print(f"\nRésultat du test : {flashcard_manager.correct_answers}/{num_questions}")
        print(f"Pourcentage : {flashcard_manager.correct_answers / num_questions * 100:.1f}%")

    except ValueError as e:
        print(f"Erreur : {e}")


def show_statistics(flashcard_manager):
    """
    Display flashcard statistics.
    """
    print("\n--- STATISTIQUES ---")
    print(f"Nombre total de cartes : {flashcard_manager.get_total_cards()}")
    print(f"Cartes connues : {flashcard_manager.get_known_cards_count()}")
    print(f"Cartes à réviser : {flashcard_manager.get_unknown_cards_count()}")
    print("Thèmes disponibles :")
    for theme in flashcard_manager.get_all_themes():
        print(f"- {theme}")


def add_flashcard(flashcard_manager):
    """
    Add a new flashcard.
    """
    print("\n--- AJOUTER UNE CARTE ---")
    question = input("Entrez la question : ")
    answer = input("Entrez la réponse : ")
    theme = input("Entrez le thème : ")

    if flashcard_manager.add_flashcard(question, answer, theme):
        print("Carte ajoutée avec succès !")
    else:
        print("Échec de l'ajout de la carte.")


def choose_theme(flashcard_manager):
    """
    Choose a specific theme to load flashcards from.
    """
    themes = flashcard_manager.get_all_themes()
    if not themes:
        print("Aucun thème disponible.")
        return

    print("\n--- CHOISIR UN THÈME ---")
    for i, theme in enumerate(themes, 1):
        print(f"{i}. {theme}")

    try:
        choice = int(input("Entrez le numéro du thème : "))
        if 1 <= choice <= len(themes):
            selected_theme = themes[choice - 1]
            flashcard_manager.load_theme(selected_theme)
            print(f"Cartes du thème '{selected_theme}' chargées.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un numéro valide.")


if __name__ == "__main__":
    main_menu()
