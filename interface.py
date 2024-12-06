import tkinter as tk
import time
#Variables

unknown_flashcards = [
    {"question": "Quelle est la capitale de la Belgique ?", "answer": "Bruxelles"},
    {"question": "Quelle est la capitale de la France", "answer": "Paris"},
    {"question": "Quelle est la capitale des USA ?", "answer": "Washington DC"},
    {"question": "how are you ?", "answer": "good"},
    {"question": "what time is it", "answer": "10:00"}
]
known_flashcards = []
is_question_shown = True

# Création de la fenêtre principale
window = tk.Tk()
window.title("Application de Flashcards")
window.geometry("800x600")  # Taille de la fenêtre

# Création du cadre pour la flashcard
card_frame = tk.Frame(window, bg="lightblue", bd=5, relief="ridge")
card_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.6)

# Zone pour les boutons
button_frame = tk.Frame(window)
button_frame.pack(side="bottom", pady=10)

# Texte de la flashcard
card_text = tk.StringVar()
card_label = tk.Label(
    card_frame,
    textvariable=card_text,
    font=("Comic Sans MS", 21, "bold"),
    bg="white",
    fg="black",
    wraplength=700,
    justify="center",
    bd=5,
    relief="solid"
)
card_label.pack(expand=True, fill="both", padx=20, pady=20)


def show_card():
    if not unknown_flashcards:
        print('tout est connu !')
        return
    else: card_text.set(unknown_flashcards[0]["question"])

def known_card():
    animate_card("right")
    known_flashcards.append(unknown_flashcards.pop(0))
    show_card()

def show_answer():
    global is_question_shown
    if is_question_shown:
        card_text.set(unknown_flashcards[0]["answer"])
    else:
        card_text.set(unknown_flashcards[0]["question"])
    is_question_shown = not is_question_shown

def unknown_card():
    animate_card("left")
    unknown_flashcards.append(unknown_flashcards.pop(0))
    show_card()

#animation
def animate_card(direction):
    move = 20 if direction == "right" else -20  # Glissement de la carte
    x_pos = 10
    for step in range(50):
        card_frame.place_configure(x= x_pos)
        x_pos += move
        window.update()
        time.sleep(0.01)
    card_frame.place_configure(x=0)

# Boutons de navigation

btn_known = tk.Button(button_frame, text="Connu", command=known_card, font=("Arial", 14), bg="green", fg="white")
btn_known.pack(side="left", padx=5)

btn_show_answer = tk.Button(button_frame, text="Montrer La réponse", command=show_answer, font=("Arial", 14), bg="orange", fg="white")
btn_show_answer.pack(side="left", padx=5)

btn_unknown = tk.Button(button_frame, text="Inconnu", command=unknown_card, font=("Arial", 14), bg="red", fg="white")
btn_unknown.pack(side="left", padx=5)

menu_bar = tk.Menu(window)

# Menu Principale
menu_bar.add_cascade(label="Quitter", command=window.quit)
menu_bar.add_cascade(label="Charger de Thème", command=lambda: print("Chargement..."))

# Menu Statistiques
stats_menu = tk.Menu(menu_bar, tearoff=0)
stats_menu.add_command(label="Afficher les statistiques", command=lambda: print("Statistiques"))
menu_bar.add_cascade(label="Statistiques", menu=stats_menu)

window.config(menu=menu_bar)




# Afficher la première carte
card_text.set(unknown_flashcards[0]["question"])

window.mainloop()

