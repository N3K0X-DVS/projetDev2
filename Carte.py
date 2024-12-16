from Theme import Theme  # Assurez-vous que Theme est importé

class Carte:
    def __init__(self, question: str, answer: str, theme: Theme, known: bool = False):
        self.question = question
        self.answer = answer
        self.theme = theme
        self.known = known

    def __repr__(self):
        return f"Carte(question={self.question}, answer={self.answer}, theme={self.theme.name}, known={self.known})"

    def mark_known(self):
        self.known = True

    def mark_unknown(self):
        self.known = False
