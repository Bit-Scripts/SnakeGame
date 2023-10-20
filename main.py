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

def afficher_quadrillage():
    for x in range(0, LARGEUR, TAILLE_CELLULE):
        pygame.draw.line(fenetre, COULEUR_QUADRILLAGE, (x, 0), (x, HAUTEUR))
    for y in range(0, HAUTEUR, TAILLE_CELLULE):
        pygame.draw.line(fenetre, COULEUR_QUADRILLAGE, (0, y), (LARGEUR, y))

def enregistrer_score(score, nom):
    with open("scores.txt", "a") as fichier_scores:
        fichier_scores.write(f"{nom} : {score}\n")

def afficher_scores():
    with open("scores.txt", "r") as fichier_scores:
        scores = fichier_scores.readlines()

    scores_tries = sorted(scores, key=lambda s: int(s.split(" : ")[1]), reverse=True)
    top_scores = scores_tries[:10]

    y = HAUTEUR / 4 + 50
    for score in top_scores:
        score_texte = lcd_font.render(score.strip(), True, COULEUR_SCORE)
        fenetre.blit(score_texte, [LARGEUR/2 - score_texte.get_width()/2, y])
        y += 30

def demander_nom(score):
    lcd_font = pygame.font.Font("digital_font.ttf", 32)
    input_box = pygame.Rect(LARGEUR / 2 - 70, HAUTEUR / 2, 140, lcd_font.get_height() + 10)  # Ajustement ici
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
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
                        enregistrer_score(score, text)
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
    
    # Affichez le titre "High Scores"
    lcd_title_font = pygame.font.Font("digital_font.ttf", 40)
    title = lcd_title_font.render("High Scores", True, COULEUR_SCORE)
    fenetre.blit(title, (LARGEUR/2 - title.get_width()/2, HAUTEUR/4))
    
    # Affichez les scores
    afficher_scores()

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

def meilleur_score(score):
    fichier_scores = open("scores.txt", "r")
    scores = fichier_scores.readlines()
    fichier_scores.close()
    if len(scores) < 5 or score > int(scores[-1].split(" : ")[1]):
        demander_nom(score)

# Fonction principale
def jeu_snake():
    serpent = [[LARGEUR / 2, HAUTEUR / 2]]
    score = 0
    mouvement_x, mouvement_y = 0, 0
    pomme = [random.randrange(0, LARGEUR, TAILLE_CELLULE), random.randrange(0, HAUTEUR, TAILLE_CELLULE)]
    jeu_en_cours = True

    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_en_cours = False

# Contrôle du mouvement du serpent
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mouvement_x = -TAILLE_CELLULE
                    mouvement_y = 0
                elif event.key == pygame.K_RIGHT:
                    mouvement_x = TAILLE_CELLULE
                    mouvement_y = 0
                elif event.key == pygame.K_UP:
                    mouvement_x = 0
                    mouvement_y = -TAILLE_CELLULE
                elif event.key == pygame.K_DOWN:
                    mouvement_x = 0
                    mouvement_y = TAILLE_CELLULE

# Mise à jour de la position de la tête du serpent
        tete_x = serpent[0][0] + mouvement_x
        tete_y = serpent[0][1] + mouvement_y
        nouvelle_tete = [tete_x, tete_y]
        serpent.insert(0, nouvelle_tete)

# Vérification de la collision avec la pomme
        if serpent[0] == pomme:
            score += 5
            pomme = [random.randrange(0, LARGEUR, TAILLE_CELLULE), random.randrange(0, HAUTEUR, TAILLE_CELLULE)]
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
            demander_nom(score)  # Demandez le nom ici
            afficher_scores()  # Affichez les scores ici
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
            

# Effacement de l'écran
        fenetre.fill(COULEUR_FOND)

        afficher_serpent(serpent)
        afficher_pomme(pomme)
        afficher_quadrillage()
        
        afficher_score(score)  # Déplacer l'affichage du score ici pour le mettre à jour à chaque boucle
        
        pygame.display.flip()

        horloge.tick(VITESSE)  # Utiliser l'horloge déjà initialisée
        
# Affichage du score à l'écran
    afficher_score(score)

# Affichage des meilleurs scores à l'écran
    afficher_scores()

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