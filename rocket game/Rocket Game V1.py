import pygame, sys
from random import randint

#résolution
LARGEUR = 800
HAUTEUR = 600

pygame.display.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("SpaceShooter")

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
MARRON = (169, 114, 80)

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

        PP --> partie principale --> H 40px
        PG --> partie gauche --> H 25px
        PD --> partie droite --> H 25px
        PR --> partie réacteur --> H 20px
        PRC --> partie réacteur centre --> H 10px
        """
        #*****************Partie Principale*****************

        # hauteur
        self.Hx_PP, self.Hy_PP = 400, 400
        # sommet gauche
        self.Gx_PP, self.Gy_PP = 390, 440
        # sommet droit
        self.Dx_PP, self.Dy_PP = 410, 440
        # ensemble
        self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]

        #*****************Partie Gauche*****************

        # hauteur
        self.Hx_PG, self.Hy_PG = 390, 415
        # sommet gauche
        self.Gx_PG, self.Gy_PG = 385, 440
        # sommet droi
        self.Dx_PG, self.Dy_PG = 395, 440
        # ensemble
        self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]

        #*****************Partie Droite*****************

        # hauteur
        self.Hx_PD, self.Hy_PD = 410, 415
        # sommet gauche
        self.Gx_PD, self.Gy_PD = 405, 440
        # sommet droit
        self.Dx_PD, self.Dy_PD = 415, 440
        # ensemble
        self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]

        #*****************Partie réacteur*****************

        # Hauteur réacteur
        self.Hx_PR, self.Hy_PR = 400, 460
        self.Hx_PRC, self.Hy_PRC = 400, 450
        # sommet gauche
        self.Gx_PR, self.Gy_PR = 395, 440
        self.Gx_PRC, self.Gy_PRC = 398, 440
        # sommet droit
        self.Dx_PR, self.Dy_PR = 405, 440
        self.Dx_PRC, self.Dy_PRC = 402, 440
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
        self.HitboxBalleA = pygame.Rect(self.XBalleA, self.YBalleA, self.LargBalle, self.LongBalle) #hitbox balle A
        self.HitboxBalleB = pygame.Rect(self.XBalleB, self.YBalleB, self.LargBalle, self.LongBalle) #hitbox balle

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

    def tir(self, current_time):
        if current_time - self.DernierTirDelai > self.cooldown and not self.BalleTiree:
            self.BalleTiree = True
            self.DernierTirDelai = current_time
            self.XBalleA, self.YBalleA = self.Hx_PG - 2, self.Hy_PG - int(self.LongBalle/2) # position balle canon gauche
            self.XBalleB, self.YBalleB = self.Hx_PD - 2, self.Hy_PD - int(self.LongBalle/2) #position balle canon droit

    def update_balle(self):
        if self.BalleTiree:
            self.YBalleA -= self.VitBalle
            self.HitboxBalleA.x = self.XBalleA
            self.HitboxBalleA.y = self.YBalleA
            self.YBalleB -= self.VitBalle
            self.HitboxBalleB.x = self.XBalleB
            self.HitboxBalleB.y = self.YBalleB
            pygame.draw.rect(fenetre, ROUGE_CLAIR, (joueur.XBalleA, joueur.YBalleA, joueur.LargBalle, joueur.LongBalle))
            pygame.draw.rect(fenetre, ROUGE_CLAIR, (joueur.XBalleB, joueur.YBalleB, joueur.LargBalle, joueur.LongBalle))
            if self.YBalleA < 0:
                self.BalleTiree = False

joueur = JOUEUR()

class METEOR:
    def __init__(self):
        self.rayon = 20 # rayon
        self.reset()

    def reset(self):
        """Réinitialise les propriétés du météore."""
        self.MVitY = randint(1, 4)  # Vitesse Y
        self.MVitX = randint(1, 4)  # Vitesse X
        self.Mx = randint(-self.rayon, LARGEUR + self.rayon)  # Position X

        # Définir la position initiale et la direction
        if 0 <= self.Mx <= LARGEUR:  # Si X est dans la fenêtre --> Y est au-dessus
            self.My = -self.rayon
            self.direction = randint(0, 1)  # Direction aléatoire

        elif self.Mx < 0:  # Si X est à gauche de la fenêtre --> Y est aléatoire
            self.My = randint(-self.rayon, HAUTEUR // 2)
            self.direction = 1  # Direction --> à droite

        else:  # Si X est à droite de la fenêtre --> Y est aléatoire
            self.My = randint(-self.rayon, HAUTEUR // 2)
            self.direction = 0  # Direction --> à gauche

        # gérer la hitbox
        self.hitbox = pygame.Rect(self.Mx, self.My, self.rayon*2, self.rayon*2)

    def dessine(self):
        pygame.draw.circle(fenetre, MARRON, (self.Mx, self.My), self.rayon)

    def bouge(self):
        # si MVitX non nul :
        if self.direction == 0: # déplacement vers la gauche
            self.Mx -= self.MVitX
        else: # déplacement vers la droite
            self.Mx += self.MVitX
        self.My += self.MVitY
        self.hitbox.x = self.Mx
        self.hitbox.y = self.My

        # Vérifier si le météore quitte la fenêtre
        if (self.Mx < -self.rayon or self.Mx > LARGEUR + self.rayon) or self.My > HAUTEUR + self.rayon:
            self.reset()
        # Vérifier si le météor a été touché
        if joueur.BalleTiree:
            if joueur.HitboxBalleA and joueur.HitboxBalleA.colliderect(self.hitbox):
                if joueur.HitboxBalleB and joueur.HitboxBalleB.colliderect(self.hitbox):
                    self.reset()
                    joueur.BalleTiree = False
                else:
                    self.reset()
                    joueur.BalleTiree = False
            if joueur.HitboxBalleB and joueur.HitboxBalleB.colliderect(self.hitbox):
                self.reset()
                joueur.BalleTiree = False

# Initialisation des météores
NB_METEOR = 5
METEORS = [METEOR() for _ in range(NB_METEOR)]

#*****************Boucle Principale*****************

n=0
fps = pygame.time.Clock()
while True:
    #pour fermer le jeu proprement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    #pour calculer le cooldown du tir
    current_time = pygame.time.get_ticks()

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

    for meteors in METEORS:
        meteors.bouge()
        meteors.dessine()

    #si le joueur tir
    if keys[pygame.K_SPACE] and not joueur.BalleTiree:
        joueur.tir(current_time)

    joueur.update_balle()

    pygame.display.flip()

    fps.tick(60)
    n += 1
    if n == 10:
        print(fps)
        n = 0

"""
NOTE :
    l'idée serait de faire en sorte que les réacteurs s'allume seulement si on déplace le vaisseau
    si on déplace le vaisseau à gauche ou à droite --> faire pencher le vaisseau (à faire en dernier)

A FAIRE :
    faire les astéroides --> faire la barre de vie et le score
    faire cinématique de début (vaisseau qui décolle) --> si le joueur perd on repasse sur cet écran
"""