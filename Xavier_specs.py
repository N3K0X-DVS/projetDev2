def modify_text(self, new_text: str):
    ''' modifie l'attribut self.text pour lui assigner une nouvelle valeur.
    PRE: new_text est une chaine de charactère
    POST: remplace self.text par new_text

    '''
    self.text = new_text


def modify_image(self, new_image: str):
    ''' modifie l'attribut self.image pour lui assigner une nouvelle valeur.
    PRE: new_text est une chaine de charactère(lien)
    POST: remplace self.image par new_image

    '''
    self.image = new_image


def add_card(self, card: Card):
    ''' ajoute une card a la collection de card
    PRE: card est une instance de Card
    POST: card est ajouter a la collection de card

    '''
    self.cards.append(card)


def remove_card(self, card: Card):
    ''' enlève une card a la collection de card
    PRE: card est une instance de Card
    POST: card est enlevé a la collection de card

    '''
    if card in self.cards:
        self.cards.remove(card)
        print(f"Carte supprimée du thème {self.name} avec succès!")
    else:
        print("La carte n'est pas dans ce thème.")


def get_cards(self) -> List[Card]:
    ''' getter pour la liste de card
    PRE: None
    POST: renvoie la liste des cards enregistré

    '''
    return self.cards
