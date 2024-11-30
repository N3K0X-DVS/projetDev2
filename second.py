import sqlite3


def creer_base_de_donnees():
    """
    Crée une base de données SQLite avec deux tables : theme et fiche
    Les tables sont liées par theme_id avec une contrainte de clé étrangère
    """
    # Connexion à la base de données (la créera si elle n'existe pas)
    conn = sqlite3.connect('fiches_thematiques.db')
    curseur = conn.cursor()

    # Création de la table theme
    curseur.execute('''
    CREATE TABLE IF NOT EXISTS theme (
        theme_id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme_nom TEXT NOT NULL UNIQUE
    )
    ''')

    # Création de la table fiche
    curseur.execute('''
    CREATE TABLE IF NOT EXISTS fiche (
        id_question INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        reponse TEXT NOT NULL,
        theme_id INTEGER,
        FOREIGN KEY(theme_id) REFERENCES theme(theme_id)
    )
    ''')

    # Commit des changements et fermeture de la connexion
    conn.commit()
    conn.close()


def ajouter_theme(theme_nom):
    """
    Ajoute un nouveau thème à la base de données

    :param theme_nom: Nom du thème à ajouter
    :return: L'ID du thème ajouté
    """
    conn = sqlite3.connect('fiches_thematiques.db')
    curseur = conn.cursor()

    try:
        curseur.execute('INSERT INTO theme (theme_nom) VALUES (?)', (theme_nom,))
        theme_id = curseur.lastrowid
        conn.commit()
        return theme_id
    except sqlite3.IntegrityError:
        # Si le thème existe déjà, récupérer son ID existant
        curseur.execute('SELECT theme_id FROM theme WHERE theme_nom = ?', (theme_nom,))
        theme_id = curseur.fetchone()[0]
        return theme_id
    finally:
        conn.close()


def ajouter_fiche(question, reponse, theme_nom):
    """
    Ajoute une nouvelle fiche à la base de données

    :param question: La question de la fiche
    :param reponse: La réponse à la question
    :param theme_nom: Le nom du thème associé
    """
    # Récupérer ou créer l'ID du thème
    theme_id = ajouter_theme(theme_nom)

    conn = sqlite3.connect('fiches_thematiques.db')
    curseur = conn.cursor()

    curseur.execute('''
    INSERT INTO fiche (question, reponse, theme_id) 
    VALUES (?, ?, ?)
    ''', (question, reponse, theme_id))

    conn.commit()
    conn.close()


def recuperer_fiches_par_theme(theme_nom):
    """
    Récupère toutes les fiches d'un thème donné

    :param theme_nom: Nom du thème
    :return: Liste de tuples (id_question, question, reponse)
    """
    conn = sqlite3.connect('fiches_thematiques.db')
    curseur = conn.cursor()

    curseur.execute('''
    SELECT fiche.id_question, fiche.question, fiche.reponse, theme.theme_nom
    FROM fiche 
    JOIN theme ON fiche.theme_id = theme.theme_id 
    WHERE theme.theme_nom = ?
    ''', (theme_nom,))

    fiches = curseur.fetchall()
    conn.close()

    return fiches


def main():
    # Création de la base de données
    creer_base_de_donnees()

    # Exemple d'utilisation
    # Ajout de thèmes et fiches
    ajouter_fiche(
        "Quelle est la capitale de la France ?",
        "Paris",
        "Géographie"
    )

    ajouter_fiche(
        "Qui a peint la Joconde ?",
        "Léonard de Vinci",
        "Art"
    )

    # Récupération des fiches par thème
    print("Fiches du thème 'Géographie':")
    for fiche in recuperer_fiches_par_theme("Géographie"):
        print(f"ID: {fiche[0]}, Question: {fiche[1]}, Réponse: {fiche[2]}, theme:{fiche[3]}")


if __name__ == "__main__":
    main()