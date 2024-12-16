# flashcard_logic.py
import random
from typing import List, Dict, Optional
from DB import recuperer_all_info_fiches, recuperer_fiches_par_theme, ajouter_fiche
from Carte import Carte
from Theme import Theme

class FlashcardLogic:
    def __init__(self):
        self.all_flashcards: List[Carte] = []
        self.current_flashcards: List[Carte] = []
        self.current_card_index: int = 0
        self.test_mode: bool = False
        self.test_questions: List[Carte] = []
        self.current_question_index: int = 0
        self.correct_answers: int = 0

    def load_all_cards(self) -> None:
        fiches = recuperer_all_info_fiches()
        self.all_flashcards = [Carte(fiche[1], fiche[2], Theme(fiche[4])) for fiche in fiches]
        self.current_flashcards = [card for card in self.all_flashcards if not card.known]
        self.current_card_index = 0

    def load_theme(self, theme_name: str) -> None:
        fiches = recuperer_fiches_par_theme(theme_name)
        self.all_flashcards = [Carte(fiche[1], fiche[2], Theme(fiche[3])) for fiche in fiches]
        self.current_flashcards = [card for card in self.all_flashcards if not card.known]
        self.current_card_index = 0

    def get_all_themes(self) -> List[str]:
        return list(set(card.theme.name for card in self.all_flashcards))

    def get_current_card(self) -> Optional[Carte]:
        if not self.current_flashcards:
            return None
        return self.current_flashcards[self.current_card_index]

    def previous_card(self) -> None:
        if not self.current_flashcards:
            return
        self.current_card_index = (self.current_card_index - 1) % len(self.current_flashcards)

    def mark_current_card_as_known(self) -> None:
        if not self.current_flashcards:
            return
        self.current_flashcards[self.current_card_index].mark_known()
        self.current_flashcards.pop(self.current_card_index)
        if self.current_card_index >= len(self.current_flashcards):
            self.current_card_index = 0

    def mark_current_card_as_unknown(self) -> None:
        if not self.current_flashcards:
            return
        card = self.current_flashcards[self.current_card_index]
        self.current_flashcards.append(self.current_flashcards.pop(self.current_card_index))

    def get_total_cards(self) -> int:
        return len(self.all_flashcards)

    def get_known_cards_count(self) -> int:
        return len([card for card in self.all_flashcards if card.known])

    def get_unknown_cards_count(self) -> int:
        return len([card for card in self.all_flashcards if not card.known])

    def prepare_test(self, num_questions: int = 10) -> List[Carte]:
        unknown_cards = [card for card in self.all_flashcards if not card.known]
        if len(unknown_cards) < num_questions:
            raise ValueError("Not enough unknown cards to prepare test")
        self.test_mode = True
        self.test_questions = random.sample(unknown_cards, num_questions)
        self.current_question_index = 0
        self.correct_answers = 0
        return self.test_questions

    def check_test_answer(self, question_index: int, user_answer: str) -> bool:
        if question_index >= len(self.test_questions):
            return False
        current_question = self.test_questions[question_index]
        return user_answer.strip().lower() == current_question.answer.strip().lower()

    def add_flashcard(self, question: str, answer: str, theme_name: str) -> bool:
        try:
            theme = Theme(theme_name)
            ajouter_fiche(question, answer, theme.name)
            self.load_all_cards()
            return True
        except Exception as e:
            print(f"Error adding flashcard: {e}")
            return False
