import pygame
import random

# Initialisation de pygame
pygame.init()

# Constantes
LARGEUR = 640
HAUTEUR = 480
TAILLE_CELLULE = 20
VITESSE = 10

# Couleurs
BLANC = (155, 188, 15)
COULEUR_SCORE = (0, 0, 0)
COULEUR_FOND = (181, 193, 134)
COULEUR_SERPENT = (96, 96, 96)
COULEUR_POMME = (184, 111, 13)
COULEUR_QUADRILLAGE = (200, 209, 161)

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Snake")
horloge = pygame.time.Clock()
lcd_font = pygame.font.Font("digital_font.ttf", 32)

def afficher_score(score):
    score_texte = lcd_font.render(f"Score : {score}", True, COULEUR_SCORE)
    fenetre.blit(score_texte, [10, 10])

def afficher_serpent(serpent):
    for position in serpent:
        pygame.draw.rect(fenetre, COULEUR_SERPENT, (*position, TAILLE_CELLULE, TAILLE_CELLULE))

def afficher_pomme(pomme):
    pygame.draw.rect(fenetre, COULEUR_POMME, (*pomme, TAILLE_CELLULE, TAILLE_CELLULE))
    
def nouvelle_pomme(selection_murs):
    while True:
        pomme_temp = [random.randrange(0, LARGEUR, TAILLE_CELLULE), random.randrange(0, HAUTEUR, TAILLE_CELLULE)]
        if selection_murs == "Murs autour":
            if pomme_temp[0] <= 0 or pomme_temp[0] >= LARGEUR - 1 or pomme_temp[1] <= 0 or pomme_temp[1] >= HAUTEUR - 1:
                continue
        elif selection_murs == "Murs en croix":
            # Collision avec le mur vertical
            if (LARGEUR/2 - TAILLE_CELLULE <= pomme_temp[0] < LARGEUR/2 and 0 <= pomme_temp[1] < HAUTEUR):
                continue
            # Collision avec le mur horizontal supérieur
            elif (0 <= pomme_temp[0] < LARGEUR/2 - 3*TAILLE_CELLULE and HAUTEUR/2 - TAILLE_CELLULE <= pomme_temp[1] < HAUTEUR/2):
                continue
            # Collision avec le mur horizontal inférieur
            elif (LARGEUR/2 + 3*TAILLE_CELLULE <= pomme_temp[0] < LARGEUR and HAUTEUR/2 - TAILLE_CELLULE <= pomme_temp[1] < HAUTEUR/2):
                continue
        return pomme_temp

def afficher_quadrillage():
    for x in range(0, LARGEUR, TAILLE_CELLULE):
        pygame.draw.line(fenetre, COULEUR_QUADRILLAGE, (x, 0), (x, HAUTEUR))
    for y in range(0, HAUTEUR, TAILLE_CELLULE):
        pygame.draw.line(fenetre, COULEUR_QUADRILLAGE, (0, y), (LARGEUR, y))

def enregistrer_score(score, nom, mode):
    with open("scores.txt", "a") as fichier_scores:
        fichier_scores.write(f"{nom} : {score} : {mode}\n")

def obtenir_meilleurs_scores(mode):
    with open("scores.txt", "r") as fichier_scores:
        scores = fichier_scores.readlines()

    # Filtrer les scores en fonction du mode
    scores_mode = [s for s in scores if len(s.strip().split(":")) > 2 and s.strip().split(":")[2].strip() == mode]
    
    # Trier les scores
    scores_tries = sorted(scores_mode, key=lambda s: int(s.split(" : ")[1]), reverse=True)

    # Renvoyer les 10 meilleurs scores pour ce mode
    return scores_tries[:10]

def afficher_meilleurs_scores():
    lcd_title_font = pygame.font.Font("digital_font.ttf", 50)
    title = lcd_title_font.render("High Scores", True, COULEUR_SCORE)
    fenetre.blit(title, (LARGEUR/2 - title.get_width()/2, 30))  # Remontez le titre en haut

    modes = ["Sans mur", "Murs autour", "Murs en croix"]
    
    lcd_font_score = pygame.font.Font("digital_font.ttf", 25)
    
    for idx, mode in enumerate(modes):
        meilleurs_scores = obtenir_meilleurs_scores(mode)
        
        # Positionnement des titres des modes
        offset_y = 100
        mode_title = lcd_font_score.render(mode, True, COULEUR_SCORE)
        fenetre.blit(mode_title, (LARGEUR/3 * idx, offset_y))
        
        # Affichage des 10 premiers scores pour chaque mode
        for i, score in enumerate(meilleurs_scores):
            y_position = offset_y + (i + 1) * 30
            score_texte = lcd_font_score.render(score.strip().split(":")[0] + " : " + score.strip().split(":")[1], True, COULEUR_SCORE)
            fenetre.blit(score_texte, (LARGEUR/3 * idx, y_position))

def demander_nom(score, mode):
    lcd_font = pygame.font.Font("digital_font.ttf", 32)
    input_box = pygame.Rect(LARGEUR / 2 - 70, HAUTEUR / 2, 140, lcd_font.get_height() + 10)  # Ajustement ici
    color_inactive = pygame.Color('black')
    color_active = pygame.Color('black')
    color = color_inactive
    active = True
    text = ''
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        enregistrer_score(score, text, mode)
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = lcd_font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        fenetre.fill(COULEUR_FOND)
        
        # Ajout d'un texte explicatif
        prompt_texte = lcd_font.render("Entrez votre nom:", True, COULEUR_SCORE)
        fenetre.blit(prompt_texte, (LARGEUR/2 - prompt_texte.get_width()/2, HAUTEUR/2 - 40))
        
        fenetre.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(fenetre, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
    # Effacez l'écran après avoir terminé la saisie
    fenetre.fill(COULEUR_FOND)

    # Affichez les scores
    afficher_meilleurs_scores()

    pygame.display.flip()

    # Attendre que l'utilisateur appuie sur une touche pour commencer une nouvelle partie ou quitte le jeu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                waiting = False

def meilleur_score(score, mode):
    fichier_scores = open("scores.txt", "r")
    scores = fichier_scores.readlines()
    fichier_scores.close()
    if len(scores) < 5 or score > int(scores[-1].split(" : ")[1]):
        demander_nom(score, mode)
        
# Options Murs        
def menu_murs():
    # Initialisation des options et de l'index sélectionné
    options = ["Sans mur", "Murs autour", "Murs en croix"]
    index_selection = 0
    en_attente = True

    while en_attente:
        fenetre.fill(COULEUR_FOND)
        
        # Affichage des options
        for i, option in enumerate(options):
            color = COULEUR_SCORE if i == index_selection else BLANC
            text = lcd_font.render(option, True, color)
            fenetre.blit(text, (LARGEUR/2 - text.get_width()/2, HAUTEUR/2 + i * 40 - len(options) * 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    index_selection = (index_selection + 1) % len(options)
                elif event.key == pygame.K_UP:
                    index_selection = (index_selection - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    en_attente = False

    return options[index_selection]

# Affichage des murs
def dessiner_murs(selection):
    if selection == "Murs autour":
        pygame.draw.rect(fenetre, COULEUR_SERPENT, (0, 0, LARGEUR, TAILLE_CELLULE))
        pygame.draw.rect(fenetre, COULEUR_SERPENT, (0, HAUTEUR - TAILLE_CELLULE, LARGEUR,TAILLE_CELLULE))
        pygame.draw.rect(fenetre, COULEUR_SERPENT, (0, 0, TAILLE_CELLULE, HAUTEUR))
        pygame.draw.rect(fenetre, COULEUR_SERPENT, (LARGEUR - TAILLE_CELLULE, 0, TAILLE_CELLULE, HAUTEUR))
    elif selection == "Murs en croix":
        # Dessinez le mur vertical au centre
        pygame.draw.rect(fenetre, COULEUR_SERPENT, (LARGEUR/2 - TAILLE_CELLULE, 0, TAILLE_CELLULE, HAUTEUR))
        # Dessinez le mur horizontal au centre avec un espace au milieu
        pygame.draw.rect(fenetre, COULEUR_SERPENT, (0, HAUTEUR/2 - TAILLE_CELLULE, LARGEUR/2 - 3*TAILLE_CELLULE, TAILLE_CELLULE))
        pygame.draw.rect(fenetre, COULEUR_SERPENT, (LARGEUR/2 + 3*TAILLE_CELLULE, HAUTEUR/2 - TAILLE_CELLULE, LARGEUR/2 - 3*TAILLE_CELLULE, TAILLE_CELLULE))

# gestion collision
def collision(score, mode):
    demander_nom(score, mode)  # Demandez le nom ici
    afficher_meilleurs_scores()  # Affichez les scores ici
    pygame.display.flip()
    waiting = True
    while waiting:  # Boucle d'attente pour une nouvelle partie
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:  # Appuyez sur n'importe quelle touche pour démarrer une nouvelle partie
                waiting = False
                jeu_snake()
                return
            
# Fonction principale
def jeu_snake():
    
    selection_murs = menu_murs()
    if not selection_murs:  # Si l'utilisateur a fermé la fenêtre
        return
    
    # Initialisation du serpent
    if selection_murs == "Murs en croix":
        serpent = [[LARGEUR / 2 - TAILLE_CELLULE * 8, HAUTEUR / 2 - TAILLE_CELLULE * 4]]
    else:
        serpent = [[LARGEUR / 2, HAUTEUR / 2]]
    mouvement_x, mouvement_y = TAILLE_CELLULE, 0
    
    # Initialisation la direction en cours à None.
    direction_actuelle = "DEPART"

    score = 0
    mouvement_x, mouvement_y = 0, 0
    pomme = [random.randrange(0, LARGEUR, TAILLE_CELLULE), random.randrange(0, HAUTEUR, TAILLE_CELLULE)]
    jeu_en_cours = True
    # Avant la boucle principale du jeu
    
    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_en_cours = False

# Contrôle du mouvement du serpent
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and mouvement_x == 0 and (not direction_actuelle or direction_actuelle != "DROITE"):
                    mouvement_x = -TAILLE_CELLULE
                    mouvement_y = 0
                elif event.key == pygame.K_RIGHT and mouvement_x == 0 and (not direction_actuelle or direction_actuelle != "GAUCHE"):
                    mouvement_x = TAILLE_CELLULE
                    mouvement_y = 0
                elif event.key == pygame.K_UP and mouvement_y == 0 and (not direction_actuelle or direction_actuelle != "BAS"):
                    mouvement_x = 0
                    mouvement_y = -TAILLE_CELLULE
                elif event.key == pygame.K_DOWN and mouvement_y == 0 and (not direction_actuelle or direction_actuelle != "HAUT"):
                    mouvement_x = 0
                    mouvement_y = TAILLE_CELLULE

# Mise à jour de la position de la tête du serpent
        tete_x = serpent[0][0] + mouvement_x
        tete_y = serpent[0][1] + mouvement_y
        nouvelle_tete = [tete_x, tete_y]
        serpent.insert(0, nouvelle_tete)
        
# Dessinez le serpent
        afficher_serpent(serpent)
        
# Mise à jour de la direction actuelle après avoir dessiné le serpent
        if mouvement_x > 0:
            direction_actuelle = "DROITE"
        elif mouvement_x < 0:
            direction_actuelle = "GAUCHE"
        elif mouvement_y > 0:
            direction_actuelle = "BAS"
        elif mouvement_y < 0:
            direction_actuelle = "HAUT"

# Vérification de la collision avec la pomme
        if serpent[0] == pomme:
            score += 5
            pomme = nouvelle_pomme(selection_murs)
        else:
            serpent.pop()

# Vérification de la collision avec les bords de l'écran
        if serpent[0][0] < 0:
            serpent[0][0] = LARGEUR - TAILLE_CELLULE
        elif serpent[0][0] >= LARGEUR:
            serpent[0][0] = 0

        if serpent[0][1] < 0:
            serpent[0][1] = HAUTEUR - TAILLE_CELLULE
        elif serpent[0][1] >= HAUTEUR:
            serpent[0][1] = 0

# Vérification de la collision avec le corps du serpent
        if serpent[0] in serpent[1:]:
            collision(score, selection_murs)
            
# Vérifiez la collision avec les murs
        if selection_murs == "Murs autour":
            if serpent[0][0] <= 0 or serpent[0][0] >= LARGEUR - 1 or serpent[0][1] <= 0 or serpent[0][1] >= HAUTEUR - 1:
                collision(score, selection_murs)
        elif selection_murs == "Murs en croix":
            # Collision avec le mur vertical
            if (LARGEUR/2 - TAILLE_CELLULE <= serpent[0][0] < LARGEUR/2 and 0 <= serpent[0][1] < HAUTEUR):
                collision(score, selection_murs)
            # Collision avec le mur horizontal supérieur
            elif (0 <= serpent[0][0] < LARGEUR/2 - 3*TAILLE_CELLULE and HAUTEUR/2 - TAILLE_CELLULE <= serpent[0][1] < HAUTEUR/2):
                collision(score, selection_murs)
            # Collision avec le mur horizontal inférieur
            elif (LARGEUR/2 + 3*TAILLE_CELLULE <= serpent[0][0] < LARGEUR and HAUTEUR/2 - TAILLE_CELLULE <= serpent[0][1] < HAUTEUR/2):
                collision(score, selection_murs)

# Effacement de l'écran
        fenetre.fill(COULEUR_FOND)

        afficher_serpent(serpent)
        dessiner_murs(selection_murs)  # Dans la boucle principale du jeu, après avoir effacé l'écran
        afficher_pomme(pomme)
        afficher_quadrillage()
        
        afficher_score(score)  # Déplacer l'affichage du score ici pour le mettre à jour à chaque boucle
        
        pygame.display.flip()

        horloge.tick(VITESSE)  # Utiliser l'horloge déjà initialisée
        
# Affichage du score à l'écran
    afficher_score(score)

# Affichage des meilleurs scores à l'écran
    afficher_meilleurs_scores()

# Vérification du meilleur score
    meilleur_score(score)

# Rafraîchissement de l'écran
    pygame.display.flip()
    
# Utiliser l'horloge déjà initialisée
    horloge.tick(VITESSE)

    # Fermeture de pygame
    pygame.quit()
    
# Lancement du jeu
jeu_snake()