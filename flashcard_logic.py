import random
from typing import List, Dict, Optional
from DB import recuperer_all_info_fiches, recuperer_fiches_par_theme, ajouter_fiche


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
        fiches = recuperer_all_info_fiches()

        # Convert database tuples to dictionary format
        self.all_flashcards = [
            {"question": fiche[1], "answer": fiche[2], "theme": fiche[4], "known": False}
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
        fiches = recuperer_fiches_par_theme(theme)

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
            # Add to database
            ajouter_fiche(question, answer, theme)

            # Reload flashcards to include the new one
            self.load_all_cards()

            return True
        except Exception as e:
            print(f"Error adding flashcard: {e}")
            return False
