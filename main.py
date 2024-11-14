import json
import random
from typing import List

class Card:
    def __init__(self, text: str, image: str = ""):
        self.text = text
        self.image = image

    def modify_text(self, new_text: str):
        self.text = new_text

    def modify_image(self, new_image: str):
        self.image = new_image


class Theme:
    def __init__(self, name: str):
        self.name = name
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)
            print(f"Carte supprimée du thème {self.name} avec succès!")
        else:
            print("La carte n'est pas dans ce thème.")

    def get_cards(self) -> List[Card]:
        return self.cards


class Statistics:
    def __init__(self):
        self.total_known_cards = 0
        self.total_unknown_cards = 0

    def update_statistics(self, known: bool):
        if known:
            self.total_known_cards += 1
        else:
            self.total_unknown_cards += 1

    def display_stats(self):
        print(f"Cartes connues: {self.total_known_cards}")
        print(f"Cartes inconnues: {self.total_unknown_cards}")


class Badge:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def unlock(self):
        print(f"Badge débloqué: {self.name} - {self.description}")


class User:
    def __init__(self, name: str):
        self.name = name
        self.statistics = Statistics()
        self.badges: List[Badge] = []

    def create_card(self, text: str, image: str = "") -> Card:
        return Card(text, image)

    def review_card(self, card: Card) -> bool:
        user_answer = input(f"Question : {card.text}\nVotre réponse : ")
        correct_answer = True  # Cela doit être vérifié avec la réponse correcte
        if correct_answer:
            self.statistics.update_statistics(True)
        else:
            self.statistics.update_statistics(False)
        return correct_answer

    def display_statistics(self):
        self.statistics.display_stats()


class ReviewSystem:
    def __init__(self):
        self.known_cards: List[Card] = []
        self.unknown_cards: List[Card] = []
        self.themes: List[Theme] = []

    def add_known_card(self, card: Card):
        self.known_cards.append(card)

    def add_unknown_card(self, card: Card):
        self.unknown_cards.append(card)

    def propose_challenge(self):
        print("Proposer un défi basé sur les cartes")

    def review_by_theme(self, theme: Theme) -> List[Card]:
        return theme.get_cards()


# Fonctions de gestion des fiches avec JSON
def load_cards(file='cards.json'):
    try:
        with open(file, 'r', encoding="utf-8") as f:
            cards = json.load(f)
    except FileNotFoundError:
        cards = {}
    return cards


def save_cards(cards, file='cards.json'):
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(cards, f, indent=4)


def add_card(question, answer, file='cards.json'):
    cards = load_cards(file)
    cards[question] = answer
    save_cards(cards, file)
    print("Fiche ajoutée avec succès!")


def remove_card(file='cards.json'):
    cards = load_cards(file)
    if not cards:
        print("Aucune fiche disponible pour suppression.")
        return

    print("\n--- Fiches disponibles ---")
    questions = list(cards.keys())
    for i, question in enumerate(questions, start=1):
        print(f"{i}. {question}")

    choice = input("\nEntrez le numéro de la question à supprimer (ou 'all' pour tout supprimer) : ")
    
    if choice.strip().lower() == 'all':
        cards.clear()
        save_cards(cards, file)
        print("Toutes les fiches ont été supprimées.")
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(questions):
                question_to_delete = questions[index]
                del cards[question_to_delete]
                save_cards(cards, file)
                print(f"La fiche '{question_to_delete}' a été supprimée.")
            else:
                print("Numéro invalide.")
        except ValueError:
            print("Entrée non valide, veuillez entrer un numéro.")


def ask_question(file='cards.json'):
    cards = load_cards(file)
    if not cards:
        print("Aucune fiche disponible.")
        return

    question = random.choice(list(cards.keys()))
    correct_answer = cards[question]
    user_answer = input(f"Question: {question}\nVotre réponse : ")

    if user_answer.strip().lower() == correct_answer.strip().lower():
        print("Bonne réponse!")
    else:
        print(f"Incorrect. La bonne réponse est : {correct_answer}")


def display_cards(file='cards.json'):
    cards = load_cards(file)
    if not cards:
        print("Aucune fiche enregistrée")
    else:
        print("\n--- Liste de toutes les fiches ---\n")
        for i, (question, answer) in enumerate(cards.items(), start=1):
            print("-" * 50)
            print(f"{i}. Question: {question}")
            print(f"Réponse: {answer}")
            print("-" * 50)
        print(f"Il y a {len(cards)} fiches")


def menu():
    user = User(name="Nom d'utilisateur")
    review_system = ReviewSystem()

    while True:
        print("\n--- Système de Fiches de Révision ---")
        print("1. Ajouter une fiche")
        print("2. Réviser une fiche")
        print("3. Afficher les fiches")
        print("4. Supprimer une fiche")
        print("5. Quitter")
        choice = input("Choisissez une option : ")

        if choice == '1':
            question = input("Entrez la question : ")
            answer = input("Entrez la réponse : ")
            add_card(question, answer)
        elif choice == '2':
            ask_question()
        elif choice == '3':
            display_cards()
        elif choice == '4':
            remove_card()
        elif choice == '5':
            print("Au revoir!")
            break
        else:
            print("Option non valide, veuillez réessayer.")


menu()
