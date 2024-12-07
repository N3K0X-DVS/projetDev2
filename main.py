from DB import recuperer_all_info_fiches, ajouter_fiche
import random


class FlashcardManager:
    def __init__(self):
        self.unknown_flashcards = []
        self.known_flashcards = []
        self.current_card_index = 0
        self.test_mode = False
        self.test_questions = []
        self.current_question_index = 0
        self.correct_answers = 0

    def charger_fiches(self, fiches=None):
        if fiches is None:
            fiches = recuperer_all_info_fiches()

        self.unknown_flashcards = [
            {"question": fiche[1], "answer": fiche[2], "theme": fiche[4]} 
            for fiche in fiches
        ]
        self.known_flashcards = []
        self.current_card_index = 0

    def get_current_card(self):
        if self.unknown_flashcards:
            return self.unknown_flashcards[self.current_card_index]
        return None

    def toggle_answer(self, is_answer_shown):
        card = self.get_current_card()
        if not card:
            return None
        return card["answer"] if is_answer_shown else card["question"]

    def mark_known(self):
        if not self.unknown_flashcards:
            return

        card = self.unknown_flashcards.pop(self.current_card_index)
        self.known_flashcards.append(card)

        if self.current_card_index >= len(self.unknown_flashcards):
            self.current_card_index = 0

    def mark_unknown(self):
        if not self.unknown_flashcards:
            return

        card = self.unknown_flashcards[self.current_card_index]
        self.unknown_flashcards.append(self.unknown_flashcards.pop(self.current_card_index))

    def get_statistics(self):
        total = len(self.known_flashcards) + len(self.unknown_flashcards)
        known = len(self.known_flashcards)
        return total, known

    def start_test(self):
        if len(self.unknown_flashcards) < 10:
            return False, "Il y a moins de 10 cartes disponibles pour passer le test."

        self.test_mode = True
        self.test_questions = random.sample(self.unknown_flashcards, 10)
        self.current_question_index = 0
        self.correct_answers = 0
        return True, None

    def ask_next_question(self):
        if self.current_question_index < len(self.test_questions):
            card = self.test_questions[self.current_question_index]
            self.current_question_index += 1
            return card["question"]
        return None

    def check_answer(self, user_answer):
        card = self.test_questions[self.current_question_index - 1]
        if user_answer.strip().lower() == card["answer"].lower():
            self.correct_answers += 1

    def get_test_results(self):
        return self.correct_answers

    def add_flashcard(self, question, answer, theme):
        ajouter_fiche(question, answer, theme)
