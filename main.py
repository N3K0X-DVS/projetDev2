import json
import random


def charger_fiches(fichier='fiches.json'):
    try:
        with open(fichier, 'r', encoding="utf-8") as f:
            fiches = json.load(f)
    except FileNotFoundError:
        fiches = {}
    return fiches


def sauvegarder_fiches(fiches, fichier='fiches.json'):
    with open(fichier, 'w', encoding="utf-8") as f:
        json.dump(fiches, f, indent=4)


def ajouter_fiche(question, reponse, fichier='fiches.json'):
    fiches = charger_fiches(fichier)
    fiches[question] = reponse
    sauvegarder_fiches(fiches, fichier)
    print("Fiche ajoutée avec succès!")


def poser_question(fichier='fiches.json'):
    fiches = charger_fiches(fichier)
    if not fiches:
        print("Aucune fiche disponible.")
        return

    question = random.choice(list(fiches.keys()))
    reponse_correcte = fiches[question]
    reponse_utilisateur = input(f"Question : {question}\nVotre réponse : ")

    if reponse_utilisateur.strip().lower() == reponse_correcte.strip().lower():
        print("Bonne réponse!")
    else:
        print(f"Incorrect. La bonne réponse est : {reponse_correcte}")


def afficher_fiches(fichier ='fiches.json'):
    fiches = charger_fiches(fichier)
    if not fiches:
        print("aucune fiche enregistrée")
    else:
        print("\n ---liste de toutes les fiches---\n")
        i = 0
        for question, reponse in fiches.items():
            i += 1
            print("-"*50)
            print(f"{i}. Question: {question}")
            print(f"Réponse: {reponse}")
            print("-" * 50)
        print(f"Il y a {len(fiches)} fiches")


def supprimer_fiches(fichier = 'fiches.json'):
    fiches = charger_fiches(fichier)
    if not fiches:
        print("aucune fiche enregistrée")
    print("\n ---fiches disponible ---\n")
    for i, question in enumerate(fiches.keys(), 1):
        print('_' * 50)
        print(f"{i}.{question}")
        print('_' * 50)
    choix = input("\n  ---Entrez les numéros des questions que vous souhaitez supprimer, separez par une virgule ou ecrivez 'all' pour tout supprimer. ex(1,7,14): ")
    if choix.strip().lower() == 'all':
        fiches.clear()
        sauvegarder_fiches(fiches, fichier)
        print("toutes les fiches ont été supprimer")
        return

    else:
        indices_a_supprimer = [int(num.strip()) for num in choix.split(',') if num.strip().isdigit()]

        questions_a_supprimer = [list(fiches.keys())[i - 1] for i in indices_a_supprimer if 1 <= i <= len(fiches)]

        if not questions_a_supprimer:
            print("Aucune question valide sélectionnée.")
            return

        for question in questions_a_supprimer:
            del fiches[question]

        sauvegarder_fiches(fiches, fichier)
        print("Fiches supprimées avec succès.")


def menu():
    while True:
        print("\n--- Système de Fiches de Révision ---")
        print("1. Ajouter une fiche")
        print("2. Réviser une fiche")
        print("3. afficher les fiches")
        print("4. supprimer une fiche")
        print("5. Quitter")
        choix = input("Choisissez une option : ")

        if choix == '1':
            question = input("Entrez la question : ")
            reponse = input("Entrez la réponse : ")
            ajouter_fiche(question, reponse)
        elif choix == '2':
            poser_question()
        elif choix == '3':
            afficher_fiches()
        elif choix == '4':
            supprimer_fiches()
        elif choix == '5':
            print("Au revoir!")
            break
        else:
            print("Option non valide, veuillez réessayer.")

if __name__ == '__main__':

    menu()