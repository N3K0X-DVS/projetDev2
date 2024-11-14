class User:
    def __init__(self, name: str):
        self.name = name
        self.statistics = Statistics()
        self.badges: List[Badge] = []

    def create_card(self, text: str, image: str = "") -> Card:
        """
        Créer une instance de carte avec son texte et son image

        PRE: texte lié a la carte
             image liée à la carte 
        POST: une instance de carte est créée
        
        """
        return Card(text, image)

    def review_card(self, card: Card) -> bool:
        """
        Permet de vérifier la réponse de l'utilisateur en fonction de la question de la carte

        PRE: l'instance de carte
        POST: la réponse correcte a la carte

        """
        user_answer = input(f"Question : {card.text}\nVotre réponse : ")
        correct_answer = True  # Cela doit être vérifié avec la réponse correcte
        if correct_answer:
            self.statistics.update_statistics(True)
        else:
            self.statistics.update_statistics(False)
        return correct_answer

    def display_statistics(self):
        """
        Affiche les statistiques du joueur
        PRE: pas de parametres
        POST: ne renvoie rien mais affiche les données
        """
        self.statistics.display_stats()

class Statistics:
    def __init__(self):
        self.total_known_cards = 0
        self.total_unknown_cards = 0

    def update_statistics(self, known: bool):
        """
        Actualise les données en fonction de si l'utilisateur connait la carte ou non

        PRE: parametre known booléen introduit par l'utilisateur
        POST: ne renvoie rien mais actualise self.total_known_cards/self.total_unknown_cards

        """
        if known:
            self.total_known_cards += 1
        else:
            self.total_unknown_cards += 1

    def display_stats(self):
        """
        Affiche le nombre de cartes connues et pas connues

        PRE: pas de parametres
        POST: ne renvoie rien mais affiche les données
        """
        print(f"Cartes connues: {self.total_known_cards}")
        print(f"Cartes inconnues: {self.total_unknown_cards}")
