"""
Titre : PROJET 2, Escape game python des neiges
Objectif : Le joueur parcours un plan, reçoit des indices, ouvre des portes s'il répond
            correctement à la question posée par la porte pour atteindre la sortie et gagner.

Nom : Secundar
Prénom : Ismael
Matricule : 504107
Date : 12/11/2020

"""

import turtle                                   # Importe le module Turtle

from CONFIGS import *


def lire_matrice(fichier):
    """
    Lit un fichier et retourne chaque ligne de ce fichier en une matrice.
    :param fichier: fichier texte
    :return: matrice du plan
    """
    matrice = []                                # On définie une matrice vide

    for l in open(fichier):                     # Lit les lignes du fichier
        matrice_1 = []                          # Correspond à une ligne de la matrice
        matrice.append(matrice_1)
        for elem in l:                          # Correspond aux colonnes de la matrice
            if elem.isnumeric():                # Permet d'avoir que des valeurs numériques
                matrice_1.append(int(elem))

    return matrice


def calculer_pas(matrice):
    """
    Calcule le pas, cette valeur est la longueur minimale d'une case par rapport au plan donné
    :param matrice:
    :return: donne un entier
    """

    hauteur_max_plan = abs(ZONE_PLAN_MINI[0])+abs(ZONE_PLAN_MAXI[0])    # calcul la hauteur du plan
    largeur_max_plan = abs(ZONE_PLAN_MINI[1])+abs(ZONE_PLAN_MAXI[1])    # calcul la largeur du plan

    hauteur_matrice = len(matrice)                                      # nombre de lignes de la matrice
    largeur_matrice = len(matrice[0])                                   # nombre de colonnes de la matrice

    pas_a = hauteur_max_plan//hauteur_matrice                           # la hauteur diviser par le nombre de ligne
    pas_b = largeur_max_plan//largeur_matrice                           # la largeur diviser par le nombre de colonne
    pas_f = min(pas_a, pas_b)                                           # Prend la valeur minimale entre les deux

    return pas_f


def coordonnees(case, pas):
    """
    :param case: tuple de coordonées (ligne,colonne) d'une case du plan
    :param pas: le pas qui a été mentionné dans le fonction calculer_pas
    :return: donne les coordonnées sur turtle du coin inférieur gauche d'une case de la matrice
    """

    return (ZONE_PLAN_MINI[0] + (case[1] * pas)), ((ZONE_PLAN_MINI[1] + pas * (len(matrice_p) - (case[0] + 1))))


def coordonne_milieu_case(position_depart, pas):
    """
    Cette fonction nous permet d'être exactement au milieu de la case
    :param position_depart: on donne la position de départ
    :param pas: on donne le pas qu'on a effectué
    :return: les coordonnées de turtle au milieu d'une case du plan
    """
    res = coordonnees(position_depart, pas)
    res_x = res[0] + (pas // 2)
    res_y = res[1] + (pas // 2)
    return res_x, res_y


def tracer_carre(dimension):
    """
    Fonction qui nous permet de tracer un carré sur turtle
    :param dimension: la dimension du carré
    :return: Rien
    """

    turtle.begin_fill()            # Turtle commence à remplir
    turtle.setheading(0)           # Turtle met sa tête dans la direction qu'il faut
    for carre in range(4):         # boucle for pour ne pas avoir de répétition, elle permet de tracer un carré
        turtle.forward(dimension)
        turtle.left(90)
    turtle.end_fill()              # Turtle arrête le remplissage


def tracer_case(case, couleur, pas):

    """
    Prend les coordonnées d'une case sur turtle, sa couleur et sa taille, ensuite fait appel à la fonction tracer_carre
    pour tracer un carré
    :param case: Tuple de coordonnées sur turtle
    :param couleur: Permet d'afficher une case dans une certaine couleur
    :param pas: Dimension de la case
    :return: Rien
    """

    turtle.tracer(0)                                           # Enlève l'annimation de turtle, trace directement
    turtle.up()                                                # Turtle lève sa plume avant d'aller à l'endroit
    turtle.goto(coordonnees(case, pas))                        # Turtle va à l'endroit demandé
    turtle.color(COULEUR_CASES)
    turtle.fillcolor(couleur)                                  # Définie la couleur qui va être tracé
    turtle.down()                                              # Turtle dépose sa plume pour écrire
    tracer_carre(pas)                                          # Turtle trace un carré de la dimension d'un pas
    turtle.up()


def afficher_plan(matrice):
    """
    Affiche le plan en fonction de la matrice et en fonction des nombres affiche une case dans une certaine couleur.
    Affiche aussi 'Inventaire'
    :param matrice:
    :return: Rien
    """

    for ligne in range(len(matrice)):
        for colonne in range(len(matrice[ligne])):
            tracer_case((ligne, colonne), COULEURS[matrice[ligne][colonne]], pas)  #appelle la fonction tracer_case.
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
    turtle.color('black')
    turtle.write('Inventaire :', font=('Calibri', 12, "bold"))
    turtle.up()

#----------------------------------------------------------------------------------------------------------------------#


def deplacer(matrice, position, mouvement):
    """
    Fonction qui permet de limiter les déplacement du personnage dans le plan. Elle permet aussi d'afficher une annonce
    si le joueur gagne
    :param matrice:
    :param position:coordonnées du joueur dans la matrice
    :param mouvement:déplacement du joueur dans le jeu
    :return:True ou False
    """
    condition = False
    if matrice[mouvement[0]][mouvement[1]] == 0:              # si la case lu sur la matrice équivaut à un couloir
        condition = True                                      # le joueur peut se déplacer sur cette case
    elif matrice[mouvement[0]][mouvement[1]] == 4:            # si la case lu sur la matrice équivaut à un indice/objet
        condition = True
        ramasser_objet(dico_objet, pas, mouvement, position, matrice_p)
    elif matrice[mouvement[0]][mouvement[1]] == 3:            # si la case lu sur la matrice équivaut à une porte
        poser_question(matrice, position, mouvement)
    elif matrice[mouvement[0]][mouvement[1]] == 2:            # si la case lu sur la matrice équivaut à la sortie
        condition = True
        changer_texte()
        turtle.goto(POINT_AFFICHAGE_ANNONCES)
        turtle.color('black')
        turtle.write('Vous avez gagné ', font=('Calibri', 12, "bold"))
        turtle.goto(coordonne_milieu_case(position, pas))
    return condition


def deplacer_gauche():
    """
    Fonction qui permet au joueur de se déplacer d'une case à gauche
    :return: Rien
    """
    global matrice_p, position_dans_jeu  # mets les variables globales dans la fonction afin de modifier la position
                                         # courante dans le jeu à chaque déplacement
    turtle.onkeypress(None, "Left")      # Désactive la touche Left
    mouv_joueur = (position_dans_jeu[0], position_dans_jeu[1] - 1)  # donne les coordonnées après le déplacement
                                                                    # selon le mouvement
    turtle.onkeypress(deplacer_gauche, "Left")  # Réassocie la touche Left à la fonction deplacer_gauche
    if deplacer(matrice_p, position_dans_jeu, mouv_joueur):  # Cas où le déplacement est possible
        tracer_case(position_dans_jeu, COULEUR_VUE, pas)     # Trace la case précédente en une couleur définie
        turtle.goto(coordonne_milieu_case(position_dans_jeu, pas))  # Dit à Turtle d'aller au milieu de la case courante
        turtle.setheading(180)
        turtle.forward(pas)
        turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)     # Place le joueur sur la case suivant le mouvement
        position_dans_jeu[:] = mouv_joueur                         # Change la variable en fonction de la nouvelle position


def deplacer_droite():
    """
    Fonction qui permet au joueur de se déplacer d'une case à droite
    :return: Rien
    """
    global matrice_p, position_dans_jeu
    turtle.onkeypress(None, "Right")
    mouv_joueur = (position_dans_jeu[0], position_dans_jeu[1] + 1)
    turtle.onkeypress(deplacer_droite, "Right")
    if deplacer(matrice_p, position_dans_jeu, mouv_joueur):
        tracer_case(position_dans_jeu, COULEUR_VUE, pas)
        turtle.goto(coordonne_milieu_case(position_dans_jeu, pas))
        turtle.setheading(0)
        turtle.forward(pas)
        turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
        position_dans_jeu[:] = mouv_joueur


def deplacer_haut():
    """
    Fonction qui permet au joueur de se déplacer d'une case en haut
    :return: Rien
    """
    global matrice_p, position_dans_jeu
    turtle.onkeypress(None, "Up")
    mouv_joueur = (position_dans_jeu[0] - 1, position_dans_jeu[1])
    turtle.onkeypress(deplacer_haut, "Up")
    if deplacer(matrice_p, position_dans_jeu, mouv_joueur):
        tracer_case(position_dans_jeu, COULEUR_VUE, pas)
        turtle.goto(coordonne_milieu_case(position_dans_jeu, pas))
        turtle.setheading(90)
        turtle.forward(pas)
        turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
        position_dans_jeu[:] = mouv_joueur


def deplacer_bas():
    """
    Fonction qui permet au joueur de se déplacer d'une case en bas
    :return: Rien
    """

    global matrice_p, position_dans_jeu
    turtle.onkeypress(None, "Down")
    mouv_joueur = (position_dans_jeu[0] + 1, position_dans_jeu[1])
    turtle.onkeypress(deplacer_bas, "Down")
    if deplacer(matrice_p, position_dans_jeu, mouv_joueur):
        tracer_case(position_dans_jeu, COULEUR_VUE, pas)
        turtle.goto(coordonne_milieu_case(position_dans_jeu, pas))
        turtle.setheading(270)
        turtle.forward(pas)
        turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
        position_dans_jeu[:] = mouv_joueur


#---------------------------------------------------------------------------------------------------------------------#
def creer_dictionnaire_des_objets(fichier_des_objets):
    """
    Cette fonction permet de créer un dictionnaire à partir d'un fichier
    :param fichier_des_objets:
    :return: Donne un dictionnaire
    """
    dictionnaire = {}
    with open(fichier_des_objets, encoding="utf-8") as object:
        for i in object:
            x, y = eval(i)       # Sépare le tuple du string de chaque ligne
            dictionnaire[x] = y  # Initialise un dictionnaire dont les clées sont des tuples correspondant à des
                                 # coordonnées et les valeurs des strings correspondant à des indices
    return dictionnaire


def changer_texte():
    """
    Pour afficher le texte suivant l'on dessine un rectangle blanc sur le texte présent
    :return: Rien
    """
    turtle.goto(POINT_AFFICHAGE_ANNONCES[0]-10, POINT_AFFICHAGE_ANNONCES[1])
    turtle.color(COULEUR_CASES)
    turtle.down()
    turtle.begin_fill()
    turtle.setheading(0)
    for i in range(2):
        turtle.forward(500)
        turtle.left(90)
        turtle.forward(30)
        turtle.left(90)
    turtle.end_fill()
    turtle.up()


def ramasser_objet(dico_objet, pas, mouvement, position, matrice_p):
    """
    Fonction qui permet de changer la case sur laquelle le joueur va prendre l'indice par une case couloir. Affiche et
    annonce l'indice récupéré dans l'inventaire. Replace turtle à la position courante du joueur
    :param dico_objet: dictionnaire
    :param pas: entier
    :param mouvement: coordonnée suivant le déplacement
    :param position: position du joueur
    :param matrice_p: matrice
    :return: Rien
    """
    matrice_p[mouvement[0]][mouvement[1]] = 0          # Change la case de l'indice par une case couloir dans la matrice
    changer_texte()
    turtle.goto(coordonnees(mouvement, pas))
    tracer_case(mouvement, COULEUR_COULOIR, pas)       # Remplace la case par une case couloir sur le plan
    index_dictionnaire = dico_objet[mouvement]
    inventaire(index_dictionnaire)
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.color('black')
    turtle.write('Vous avez trouvé : ' + dico_objet[mouvement], font=('Calibri', 12, "bold"))
    turtle.goto(coordonne_milieu_case(position, pas))


def inventaire(index):
    """
    La fonction permet d'afficher chaque objet ramassé. De façon à ce que le joueur puisse voir les indices.
    :param index:
    :return: Rien
    """
    global incrementation                  # variable qui sert à changer le numéro de l'indice et à afficher les indices
                                           # l'un en dessous de l'autre
    incrementation += 1                    # incrémente la valeur globale
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - incrementation*2*pas)
    turtle.color('black')
    turtle.write("n° " + str(incrementation) + " : " + index, font=('Calibri', 12, "bold"))

#----------------------------------------------------------------------------------------------------------------------#


def verif_rep(entree_joueur, case, matrice, solution, mouvement):
    """
    Fonction qui vérifie si la réponse du joueur est correcte. Si la réponse est correcte, la porte s'ouvre et
    l'affiche dans l'encadré des annonces
    :param entree_joueur: réponse du joueur sous forme de string
    :param case: position du joueur sous forme de tuple
    :param matrice: matrice
    :param solution: la réponse attendu
    :param mouvement: tuple du déplacement
    :return: Rien
    """
    turtle.up()
    if entree_joueur == solution:                                 # Cas où le joueur trouve la bonne réponse
        matrice[mouvement[0]][mouvement[1]] = 0                   # Change dans la matrice la case porte en case couloir
        changer_texte()
        turtle.goto(POINT_AFFICHAGE_ANNONCES)
        turtle.color('black')
        turtle.down()
        turtle.write("La porte s'ouvre ", font=('Calibri', 12, "bold"))
        turtle.up()
        turtle.goto(coordonnees(mouvement, pas))
        tracer_case(mouvement, COULEUR_COULOIR, pas)
        turtle.goto(coordonne_milieu_case(position_dans_jeu, pas))  # Replace turtle dans la position du joueur

    else:                                                           # Cas où le joueur ne trouve pas la bonne réponse
        changer_texte()
        turtle.goto(POINT_AFFICHAGE_ANNONCES)
        turtle.color('black')
        turtle.write('Mauvaise réponse ', font=('Calibri', 12, "bold"))
        turtle.goto(coordonne_milieu_case(case, pas))               # Replace turtle dans la position du joueur


def poser_question(matrice, case, mouvement):
    """
    Cette fonction permet au joueur de répondre à une question posée
    :param matrice: matrice
    :param case: position du joueur sous forme de tuple
    :param mouvement: tuple du déplacement
    :return: Rien
    """
    changer_texte()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.color('black')
    turtle.write('Cette porte est fermée ', font=('Calibri', 12, "bold"))
    entree_joueur = turtle.textinput("Question : ", dico_question[mouvement][0])   # Affiche une fenêtre dans laquelle
                                                                                   # le joueur répond à une question
    turtle.listen()
    verif_rep(entree_joueur, case, matrice, dico_question[mouvement][1], mouvement)


# variables globales :

fichier_objet = 'dico_objets.txt'
dico_objet = creer_dictionnaire_des_objets(fichier_objet)
fichier_plan = 'plan_chateau.txt'
incrementation = 0
matrice_p = lire_matrice(fichier_plan)
pas = calculer_pas(matrice_p)
afficher_plan(matrice_p)
position_dans_jeu = list(POSITION_DEPART)
dico_question = creer_dictionnaire_des_objets('dico_portes.txt')

turtle.goto(coordonne_milieu_case(position_dans_jeu, pas))
turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
turtle.listen()                                         # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_droite, "Right")             # Associe à la touche Right une fonction appelée deplacer_droite
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_gauche, "Left")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()                                       # Permet de faire une boucle
turtle.hideturtle()