import pygame, sys
from random import randint

#résolution
LARGEUR = 800
HAUTEUR = 600

pygame.display.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("jeu fusée")

#couleurs (rgb)

BLANCA = (255, 255, 255)
BLANCB = (190, 190, 190)
BLANCC = (130, 130, 130)
BLEU_MARINE = (3, 11, 20)
GRIS = (180, 180, 180)
GRIS_FONCER = (120, 120, 120)
BLEU = (0, 0, 255)
BLEU_CLAIR = (100, 100, 255)
ROUGE_CLAIR = (255, 100, 100)

NB_ETOILES = 30 # --> la classe gère 3 étoile à la fois, donc il y a 90 étoiles

class Etoile:
    def __init__(self):
        #gestion des positions
        self.xA, self.yA = randint(0, LARGEUR), randint(0, HAUTEUR)
        self.xB, self.yB = randint(0, LARGEUR), randint(0, HAUTEUR)
        self.xC, self.yC = randint(0, LARGEUR), randint(0, HAUTEUR)

        #gestion des vitesses
        self.dyA = 3
        self.dyB = 2
        self.dyC = 1

        #gestion des couleurs
        self.couleurA = BLANCA
        self.couleurB = BLANCB
        self.couleurC = BLANCC

        #rayon
        self.RAYON = 3


    def dessine(self):
        pygame.draw.circle(fenetre, self.couleurA, (self.xA, self.yA), self.RAYON)
        pygame.draw.circle(fenetre, self.couleurB, (self.xB, self.yB), self.RAYON)
        pygame.draw.circle(fenetre, self.couleurC, (self.xC, self.yC), self.RAYON)

    def bouge(self):
        self.yA += self.dyA
        self.yB += self.dyB
        self.yC += self.dyC

        if self.yA == HAUTEUR:
            self.yA = 0
            self.xA = randint(0, LARGEUR)
        if self.yB == HAUTEUR:
            self.yB = 0
            self.xB = randint(0, LARGEUR)
        if self.yC == HAUTEUR:
            self.yC = 0
            self.xC = randint(0, LARGEUR)

mon_espace = [Etoile() for _ in range(NB_ETOILES)]

class JOUEUR:
    def __init__(self):
        #définition points triangles
        """
        signification abréviation:

        PP --> partie principale
        PG --> partie gauche
        PD --> partie droite
        PR --> partie réacteur
        PRC --> partie réacteur centre
        """
        #*****************Partie Principale*****************

        # hauteur
        self.Hx_PP, self.Hy_PP = 250, 260
        # sommet gauche
        self.Gx_PP, self.Gy_PP = 240, 300
        # sommet droit
        self.Dx_PP, self.Dy_PP = 260, 300
        # ensemble
        self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]

        #*****************Partie Gauche*****************

        # hauteur
        self.Hx_PG, self.Hy_PG = 240, 275
        # sommet gauche
        self.Gx_PG, self.Gy_PG = 235, 300
        # sommet droit
        self.Dx_PG, self.Dy_PG = 245, 300
        # ensemble
        self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]

        #*****************Partie Droite*****************

        # hauteur
        self.Hx_PD, self.Hy_PD = 260, 275
        # sommet gauche
        self.Gx_PD, self.Gy_PD = 255, 300
        # sommet droit
        self.Dx_PD, self.Dy_PD = 265, 300
        # ensemble
        self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]

        #*****************Partie réacteur*****************

        # Hauteur réacteur
        self.Hx_PR, self.Hy_PR = 250, 320
        self.Hx_PRC, self.Hy_PRC = 250, 310
        # sommet gauche
        self.Gx_PR, self.Gy_PR = 245, 300
        self.Gx_PRC, self.Gy_PRC = 248, 300
        # sommet droit
        self.Dx_PR, self.Dy_PR = 255, 300
        self.Dx_PRC, self.Dy_PRC = 252, 300
        # ensemble
        self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
        self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        #*****************Autre données*****************
        self.compteur = 0
        self.VitBalle = 50
        self.LongBalle, self.LargBalle = 20, 4
        self.cooldown = 250 # correspond à 0.25 secondes
        self.XBalleA, self.YBalleA = self.Hx_PG - 2, self.Hy_PG - int(self.LongBalle/2) # position balle canon gauche
        self.XBalleB, self.YBalleB = self.Hx_PD - 2, self.Hy_PD - int(self.LongBalle/2) #position balle canon droit
        self.BalleTiree = False
        self.DernierTirDelai = 0

    def dessine(self):
        pygame.draw.polygon(fenetre, GRIS_FONCER,  self.trg_PP)
        pygame.draw.polygon(fenetre, GRIS,  self.trg_PG)
        pygame.draw.polygon(fenetre, GRIS,  self.trg_PD)
        pygame.draw.polygon(fenetre, BLEU,  self.trg_PR)
        pygame.draw.polygon(fenetre, BLEU_CLAIR,  self.trg_PRC)

    def bouge(self):
        #**********************************avec les flèches**********************************

        # Aller à gauche
        if keys[pygame.K_LEFT]:
            if  self.Gx_PG-2>=0: #aller à gauche
                #*****************Partie Principale*****************
                self.Hx_PP -= 5
                self.Gx_PP -= 5
                self.Dx_PP -= 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #*****************Partie Gauche*****************
                self.Hx_PG -= 5
                self.Gx_PG -= 5
                self.Dx_PG -= 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #*****************Partie Droite*****************
                self.Hx_PD -= 5
                self.Gx_PD -= 5
                self.Dx_PD -= 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #*****************Partie réacteur*****************
                self.Hx_PR -= 5
                self.Hx_PRC -= 5
                self.Gx_PR -= 5
                self.Gx_PRC -= 5
                self.Dx_PR -= 5
                self.Dx_PRC -= 5
                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        # Aller à droite
        if keys[pygame.K_RIGHT]:
            if  self.Dx_PD+2<LARGEUR:  #aller à droite
                #*****************Partie Principale*****************
                self.Hx_PP += 5
                self.Gx_PP += 5
                self.Dx_PP += 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #*****************Partie Gauche*****************
                self.Hx_PG += 5
                self.Gx_PG += 5
                self.Dx_PG += 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #*****************Partie Droite*****************
                self.Hx_PD += 5
                self.Gx_PD += 5
                self.Dx_PD += 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #*****************Partie réacteur*****************
                self.Hx_PR += 5
                self.Hx_PRC += 5
                self.Gx_PR += 5
                self.Gx_PRC += 5
                self.Dx_PR += 5
                self.Dx_PRC += 5
                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        # Aller en haut
        if keys[pygame.K_UP]:
            if  self.Hy_PG-2>=0: #aller en haut
                #*****************Partie Principale*****************
                self.Hy_PP -= 5
                self.Gy_PP -= 5
                self.Dy_PP -= 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #*****************Partie Gauche*****************
                self.Hy_PG -= 5
                self.Gy_PG -= 5
                self.Dy_PG -= 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #*****************Partie Droite*****************
                self.Hy_PD -= 5
                self.Gy_PD -= 5
                self.Dy_PD -= 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #*****************Partie réacteur*****************
                self.Hy_PR -= 5
                self.Hy_PRC -= 5
                self.Gy_PR -= 5
                self.Gy_PRC -= 5
                self.Dy_PR -= 5
                self.Dy_PRC -= 5
                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        # Aller en bas
        if keys[pygame.K_DOWN]:
            if  self.Dy_PD+2<HAUTEUR:  #aller en bas
                #*****************Partie Principale*****************
                self.Hy_PP += 5
                self.Gy_PP += 5
                self.Dy_PP += 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #*****************Partie Gauche*****************
                self.Hy_PG += 5
                self.Gy_PG += 5
                self.Dy_PG += 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #*****************Partie Droite*****************
                self.Hy_PD += 5
                self.Gy_PD += 5
                self.Dy_PD += 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #*****************Partie réacteur*****************
                self.Hy_PR += 5
                self.Hy_PRC += 5
                self.Gy_PR += 5
                self.Gy_PRC += 5
                self.Dy_PR += 5
                self.Dy_PRC += 5
                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        #**********************************avec ZQSD**********************************

        if keys[pygame.K_a]: # a=q touche qwerty
            if  self.Gx_PG-2>=0: #aller à gauche
                #*****************Partie Principale*****************
                self.Hx_PP -= 5
                self.Gx_PP -= 5
                self.Dx_PP -= 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #*****************Partie Gauche*****************
                self.Hx_PG -= 5
                self.Gx_PG -= 5
                self.Dx_PG -= 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #*****************Partie Droite*****************
                self.Hx_PD -= 5
                self.Gx_PD -= 5
                self.Dx_PD -= 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #*****************Partie réacteur*****************
                self.Hx_PR -= 5
                self.Hx_PRC -= 5
                self.Gx_PR -= 5
                self.Gx_PRC -= 5
                self.Dx_PR -= 5
                self.Dx_PRC -= 5
                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        # Aller à droite
        if keys[pygame.K_d]:
            if  self.Dx_PD+2<LARGEUR:  #aller à droite
                #*****************Partie Principale*****************
                self.Hx_PP += 5
                self.Gx_PP += 5
                self.Dx_PP += 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #*****************Partie Gauche*****************
                self.Hx_PG += 5
                self.Gx_PG += 5
                self.Dx_PG += 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #*****************Partie Droite*****************
                self.Hx_PD += 5
                self.Gx_PD += 5
                self.Dx_PD += 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #*****************Partie réacteur*****************
                self.Hx_PR += 5
                self.Hx_PRC += 5
                self.Gx_PR += 5
                self.Gx_PRC += 5
                self.Dx_PR += 5
                self.Dx_PRC += 5
                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        # Aller en haut
        if keys[pygame.K_w]: # w=z touche qwerty
            if  self.Hy_PG-2>=0: #aller en haut
                #*****************Partie Principale*****************
                self.Hy_PP -= 5
                self.Gy_PP -= 5
                self.Dy_PP -= 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #*****************Partie Gauche*****************
                self.Hy_PG -= 5
                self.Gy_PG -= 5
                self.Dy_PG -= 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #*****************Partie Droite*****************
                self.Hy_PD -= 5
                self.Gy_PD -= 5
                self.Dy_PD -= 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #*****************Partie réacteur*****************
                self.Hy_PR -= 5
                self.Hy_PRC -= 5
                self.Gy_PR -= 5
                self.Gy_PRC -= 5
                self.Dy_PR -= 5
                self.Dy_PRC -= 5
                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        # Aller en bas
        if keys[pygame.K_s]:
            if  self.Dy_PD+2<HAUTEUR:  #aller en bas
                #*****************Partie Principale*****************
                self.Hy_PP += 5
                self.Gy_PP += 5
                self.Dy_PP += 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #*****************Partie Gauche*****************
                self.Hy_PG += 5
                self.Gy_PG += 5
                self.Dy_PG += 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #*****************Partie Droite*****************
                self.Hy_PD += 5
                self.Gy_PD += 5
                self.Dy_PD += 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #*****************Partie réacteur*****************
                self.Hy_PR += 5
                self.Hy_PRC += 5
                self.Gy_PR += 5
                self.Gy_PRC += 5
                self.Dy_PR += 5
                self.Dy_PRC += 5
                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        self.compteur +=1
        if self.compteur<=5:
            self.Hy_PR += 1
            self.Hy_PRC += 1
        elif self.compteur>5 and self.compteur<=10:
            self.Hy_PR -= 1
            self.Hy_PRC -= 1
        elif self.compteur>10:
            self.compteur=0
        self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
        self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

joueur = JOUEUR()

n=0
fps = pygame.time.Clock()
while True:
    #pour fermer le jeu proprement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    #pour récupérer les touches pressées
    keys = pygame.key.get_pressed()

    #remplir le fond
    fenetre.fill(BLEU_MARINE)

    #dessiner et mettre à jour  les étoiles
    for etoile in mon_espace:
        etoile.dessine()
        etoile.bouge()

    #dessiner et bouger le joueur
    joueur.dessine()
    joueur.bouge()


    pygame.display.flip()


    fps.tick(60)
    n += 1
    if n == 6:
        print(fps)
        n = 0

"""
NOTE :
    l'idée serait de faire en sorte que les réacteurs s'allume seulement si on déplace le vaisseau
    si on déplace le vaisseau à gauche ou à droite --> faire pencher le vaisseau (à faire en dernier)

A FAIRE :
    finir le vaisseau
    faire les astéroides --> faire la barre de vie et le score
    faire cinématique de début (vaisseau qui décolle) --> si le joueur perd on repasse sur cet écran
"""