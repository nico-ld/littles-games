import pygame, sys
from random import randint

#résolution
LARGEUR = 800
HAUTEUR = 600

pygame.display.init()
pygame.font.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("SpaceShooter")
# Chargement de l'image d'icône
icon = pygame.image.load("img/icon.png")

# Définition de l'icône de la fenêtre
pygame.display.set_icon(icon)

#couleurs (rgb)

NOIR = (0, 0, 0)
BLANCA = (255, 255, 255)
BLANCB = (190, 190, 190)
BLANCC = (130, 130, 130)
BLEU_MARINE = (3, 11, 20)
GRIS = (180, 180, 180)
GRIS_FONCER = (120, 120, 120)
BLEU = (0, 0, 255)
BLEU_CLAIR = (100, 100, 255)
ROUGE_CLAIR = (255, 100, 100)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
VERT_CLAIR = (150, 255, 150)
MARRON = (169, 114, 80)
ORANGE =(255,  120, 0)
ORANGE_FONCER =  (200, 80, 0)

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

class METEOR:
    def __init__(self):
        self.detruit = False # vérifie si le météor est détruit
        self.toucher = False # vérifie si le joeur est toucher
        self.reset()
        self.division()

    def reset(self):
        """Réinitialise les propriétés du météore."""
        self.rayon = randint(15, 30) # rayon
        self.MVitX = randint(1, 4)  # Vitesse X
        self.Mx = randint(1, 2)

        # Définir la position initiale et la direction
        if self.Mx == 1:  # Si X est dans la fenêtre --> Y est au-dessus
            self.MVitY = randint(1, 4)  # Vitesse Y
            self.Mx = randint(-self.rayon, LARGEUR + self.rayon)  # Position X
            self.My = -self.rayon
            self.direction = randint(0, 1)  # Direction aléatoire
        else:
            self.Mx = randint(0, 1)  # Position X
            if self.Mx == 0:  # Si X est à gauche de la fenêtre --> Y est aléatoire
                self.Mx = 0 - self.rayon
                self.My = randint(-self.rayon, HAUTEUR)
                self.direction = 1  # Direction --> à droite

            else:  # Si X est à droite de la fenêtre --> Y est aléatoire
                self.Mx = LARGEUR + self.rayon
                self.My = randint(-self.rayon, HAUTEUR)
                self.direction = 0  # Direction --> à gauche
            if self.My > self.rayon*2:
                self.MVitY = randint(0, 4)  # Vitesse Y
            else:
                self.MVitY = randint(1, 4)  # Vitesse Y

        if self.direction == 0 : # dé placement vers la gauche
            self.MVitX = -self.MVitX

        # gérer la hitbox
        self.hitbox = pygame.Rect(self.Mx, self.My, self.rayon*2, self.rayon*2)

    def dessine(self):
        pygame.draw.circle(fenetre, MARRON, (self.Mx, self.My), self.rayon)


    def bouge(self):
        self.Mx += self.MVitX
        self.My += self.MVitY
        self.hitbox.x = self.Mx-self.rayon
        self.hitbox.y = self.My-self.rayon

        # Vérifier si le météore quitte la fenêtre
        if (self.Mx < -self.rayon or self.Mx > LARGEUR + self.rayon) or self.My > HAUTEUR + self.rayon:
            self.reset()

        # Vérifier si le météor a été touché
        if joueur.BalleTiree:
            if joueur.HitboxBalleA and joueur.HitboxBalleA.colliderect(self.hitbox): #si la balle A touche
                if joueur.HitboxBalleB and joueur.HitboxBalleB.colliderect(self.hitbox): # on vérifie pour la balle B
                    joueur.BalleTiree = False # on arrete le tir
                    if self.rayon < 23: # on vérifie la taille du météor --> évite de trop petit météor
                        self.reset()
                        if self.rayon<=12:
                            joueur.score+=30
                        else:
                            joueur.score += 20
                    else: # si assez grand on le divise
                        self.detruit = True
                        self.division()
                        joueur.score += 10

                else: # si la balle B touche pas
                    joueur.BalleTiree = False # on arrete le tir
                    if self.rayon < 20: # on vérifie la taille du météor évite de trop petit météor
                        self.reset()
                        if self.rayon<=12:
                            joueur.score+=30
                        else:
                            joueur.score += 20

                    else: # si assez grand on le divise
                        self.detruit = True
                        self.division()
                        joueur.score += 10

            elif joueur.HitboxBalleB and joueur.HitboxBalleB.colliderect(self.hitbox): # si la balle b touche --> léger problème de detection
                joueur.BalleTiree = False # on arrete le tir
                if self.rayon < 20: # on vérifie la taille du météor --> évite de trop petit météor
                    self.reset()
                    if self.rayon<=12:
                        joueur.score+=30
                    else:
                        joueur.score += 20
                else: # si assez grand on le divise
                    self.detruit = True
                    self.division()
                    joueur.score += 5

        # Si joueur touche météor
        if not self.toucher:
            if self.hitbox.colliderect(joueur.HitboxA) or self.hitbox.colliderect(joueur.HitboxB):
                vie.kaboum = True # déclanche l'explosion

                #récupère la position du joueur
                vie.x = joueur.Hx_PP
                vie.y = joueur.Hy_PP + int((joueur.Hy_PP-joueur.Dy_PP)/2)

                joueur.position_init() # on réinitialise la position du joueur
                joueur.vie -= 1 # on retire une vie
                self.toucher = True # on active l'immortalité
                print("Dichotomie dans ta gueule.") # d'accord Tom

    """intervient lors de la divsion du météor"""
    def division(self):
        # M = moitié A ; m = moitié B
        self.taille = int(self.rayon/2) # pour retrecir les cercles
        self.hitbox.width, self.hitbox.height = self.rayon, self.rayon # largeur et longeur hitbox A
        self.mx, self.my = self.Mx, self.My # la deuxième moitié à le même départ
        self.scdHitbox = pygame.Rect(self.mx - self.taille, self.my - self.taille, self.rayon, self.rayon) # création d'une deuxième hitbox
        self.moitieA, self.moitieB = True, True

    def dessine_division(self):
        if self.moitieA:
            pygame.draw.circle(fenetre, MARRON, (self.Mx, self.My), self.taille)

        if self.moitieB:
            pygame.draw.circle(fenetre, MARRON, (self.mx, self.my), self.taille)


    def bouge_division(self):
        """
        moitié A correspond au météor mais réduit
        """
        #déplacement moitié A
        self.Mx += self.MVitX
        self.My += -self.MVitY
        self.hitbox.x, self.hitbox.y = self.Mx-self.taille, self.My-self.taille

        #déplacment moitié B
        self.mx -= self.MVitX
        self.my += -self.MVitY
        self.scdHitbox.x, self.scdHitbox.y = self.mx-self.taille, self.my-self.taille

        # Vérifier si la moitié A quitte la fenêtre
        if (self.Mx < -self.taille or self.Mx > LARGEUR + self.taille) or self.My > HAUTEUR + self.taille:
            self.moitieA = False
        # Vérifier si la moitié B quitte la fenêtre
        if (self.mx < -self.taille or self.mx > LARGEUR + self.taille) or self.my > HAUTEUR + self.taille:
            self.moitieB = False

        # on vérifie les collisions pour la moitié A
        if joueur.BalleTiree and self.moitieA:
            if joueur.HitboxBalleA and joueur.HitboxBalleA.colliderect(self.hitbox): #si la balle A touche
                if joueur.HitboxBalleB and joueur.HitboxBalleB.colliderect(self.hitbox): # on vérifie pour la balle B
                    joueur.BalleTiree = False # on arrete le tir
                    self.moitieA = False
                    joueur.score+=30

                else: # si la balle B touche pas --> prévu en cas de modification des tirs
                    joueur.BalleTiree = False # on arrete le tir
                    self.moitieA = False
                    joueur.score+=30

            elif joueur.HitboxBalleB and joueur.HitboxBalleB.colliderect(self.hitbox): # si la balle b touche --> léger problème de detection
                joueur.BalleTiree = False # on arrete le tir
                self.moitieA = False
                joueur.score+=30

        # on vérifie les collisions pour la moitié B
        if joueur.BalleTiree and self.moitieB:
            if joueur.HitboxBalleA and joueur.HitboxBalleA.colliderect(self.scdHitbox): #si la balle A touche
                if joueur.HitboxBalleB and joueur.HitboxBalleB.colliderect(self.scdHitbox): # on vérifie pour la balle B
                    joueur.BalleTiree = False # on arrete le tir
                    self.moitieB = False
                    joueur.score+=30

                else: # si la balle B touche pas --> prévu en cas de modification des tirs
                    joueur.BalleTiree = False # on arrete le tir
                    self.moitieB = False
                    joueur.score+=30

            elif joueur.HitboxBalleB and joueur.HitboxBalleB.colliderect(self.scdHitbox): # si la balle b touche --> léger problème de detection
                joueur.BalleTiree = False # on arrete le tir
                self.moitieB = False
                joueur.score+=30


        # Si joueur touche une moitié de météor
        if not self.toucher:
            if (self.hitbox.colliderect(joueur.HitboxA) or self.hitbox.colliderect(joueur.HitboxB)) or (self.scdHitbox.colliderect(joueur.HitboxA) or self.scdHitbox.colliderect(joueur.HitboxB)):
                vie.kaboum = True
                vie.x = joueur.Hx_PP
                vie.y = joueur.Hy_PP + int((joueur.Hy_PP-joueur.Dy_PP)/2)
                joueur.position_init() # on réinitialise la position du joueur
                joueur.vie -= 1 # on retire une vie
                self.toucher = True # on active l'immortalité
                print("Dichotomie dans ta gueule.") # d'accord Tom

        # si les deux moitié sont plus la
        if not self.moitieA and not self.moitieB :
            print(f"votre score est de {joueur.score}")
            self.detruit = False
            self.reset()

# Initialisation des météores
NB_METEOR = 5
METEORS = [METEOR() for _ in range(NB_METEOR)]

class JOUEUR:
    def __init__(self):
        #définition points triangles
        self.position_init()

        #*****************Autre données*****************
        self.compteur = 0 # pour modifier le feu du réacteur
        self.VitBalle = 50
        self.LongBalle, self.LargBalle = 20, 4
        self.cooldown = 250 # correspond à 0.25 secondes
        self.XBalleA, self.YBalleA = self.Hx_PG - 2, self.Hy_PG - int(self.LongBalle/2) # position balle canon gauche
        self.XBalleB, self.YBalleB = self.Hx_PD - 2, self.Hy_PD - int(self.LongBalle/2) #position balle canon droit
        self.BalleTiree = False # vérifie pour les deux balles --> à supprimer par la suite
        self.BalleATiree = False # servira plus tard
        self.BalleBTiree = False
        self.DernierTirDelai = 0
        self.HitboxBalleA = pygame.Rect(self.XBalleA, self.YBalleA, self.LargBalle, self.LongBalle) #hitbox balle A
        self.HitboxBalleB = pygame.Rect(self.XBalleB, self.YBalleB, self.LargBalle, self.LongBalle) #hitbox balle B
        self.vie = 4 # vie initiale
        self.HitboxHS = False # désactive la hitbox si le joueur est touché
        self.TIMER_EVENT = pygame.USEREVENT + 1 #permet de faire un timer pour l'invinncibilité
        self.score = 0 # score
        self.invincible = 0 # compteur pour fair clignoter le joueur

    def position_init(self):
        """
        signification abréviation:

        PP --> partie principale --> H 40px
        PG --> partie gauche --> H 25px
        PD --> partie droite --> H 25px
        PR --> partie réacteur --> H 20px
        PRC --> partie réacteur centre --> H 10px

        fenetre de 800x600
        """
        #*****************Partie Principale*****************

        # hauteur
        self.Hx_PP, self.Hy_PP = 400, 600
        # sommet gauche
        self.Gx_PP, self.Gy_PP = 390, 640
        # sommet droit
        self.Dx_PP, self.Dy_PP = 410, 640
        # ensemble
        self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]

        #*****************Partie Gauche*****************

        # hauteur
        self.Hx_PG, self.Hy_PG = 390, 615
        # sommet gauche
        self.Gx_PG, self.Gy_PG = 385, 640
        # sommet droit
        self.Dx_PG, self.Dy_PG = 395, 640
        # ensemble
        self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]

        #*****************Partie Droite*****************

        # hauteur
        self.Hx_PD, self.Hy_PD = 410, 615
        # sommet gauche
        self.Gx_PD, self.Gy_PD = 405, 640
        # sommet droit
        self.Dx_PD, self.Dy_PD = 415, 640
        # ensemble
        self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]

        #*****************Partie réacteur*****************

        # Hauteur réacteur
        self.Hx_PR, self.Hy_PR = 400, 660
        self.Hx_PRC, self.Hy_PRC = 400, 650
        # sommet gauche
        self.Gx_PR, self.Gy_PR = 395, 640
        self.Gx_PRC, self.Gy_PRC = 398, 640
        # sommet droit
        self.Dx_PR, self.Dy_PR = 405, 640
        self.Dx_PRC, self.Dy_PRC = 402, 640
        # ensemble
        self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
        self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        self.HitboxA = pygame.Rect(self.Gx_PG, self.Hy_PG, self.Dx_PD-self.Gx_PG, self.Gy_PG-self.Hy_PG) #Hitbox vaisseau
        self.HitboxB = pygame.Rect(self.Dx_PG, self.Hy_PP, self.Gx_PD-self.Dx_PG, self.Hy_PG-self.Hy_PP) #Hitbox vaisseau

        self.spawn = True

    def dessine(self):
        if self.HitboxHS:
            self.invincible += 1
            if self.invincible < 6:
                pygame.draw.polygon(fenetre, GRIS_FONCER,  self.trg_PP)
                pygame.draw.polygon(fenetre, GRIS,  self.trg_PG)
                pygame.draw.polygon(fenetre, GRIS,  self.trg_PD)
                pygame.draw.polygon(fenetre, BLEU,  self.trg_PR)
                pygame.draw.polygon(fenetre, BLEU_CLAIR,  self.trg_PRC)
            if self.invincible == 12:
                self.invincible = 0
        else:
            pygame.draw.polygon(fenetre, GRIS_FONCER,  self.trg_PP)
            pygame.draw.polygon(fenetre, GRIS,  self.trg_PG)
            pygame.draw.polygon(fenetre, GRIS,  self.trg_PD)
            pygame.draw.polygon(fenetre, BLEU,  self.trg_PR)
            pygame.draw.polygon(fenetre, BLEU_CLAIR,  self.trg_PRC)

    def bouge(self, current_time):

        if self.spawn == True:
            if self.Hy_PP > 440:
                #PP
                self.Hy_PP -= 5
                self.Gy_PP -= 5
                self.Dy_PP -= 5
                self.trg_PP = [(self.Hx_PP, self.Hy_PP), (self.Gx_PP, self.Gy_PP), (self.Dx_PP, self.Dy_PP)]
                #PG
                self.Hy_PG -= 5
                self.Gy_PG -= 5
                self.Dy_PG -= 5
                self.trg_PG = [(self.Hx_PG, self.Hy_PG), (self.Gx_PG, self.Gy_PG), (self.Dx_PG, self.Dy_PG)]
                #PD
                self.Hy_PD -= 5
                self.Gy_PD -= 5
                self.Dy_PD -= 5
                self.trg_PD = [(self.Hx_PD, self.Hy_PD), (self.Gx_PD, self.Gy_PD), (self.Dx_PD, self.Dy_PD)]
                #PR
                self.Hy_PR -= 5
                self.Gy_PR -= 5
                self.Dy_PR -= 5
                #PRC
                self.Hy_PRC -= 5
                self.Gy_PRC -= 5
                self.Dy_PRC -= 5

                self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
                self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]
            else:
                self.spawn = False

        if not self.spawn:
            # Aller à gauche
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: # a=q touche qwerty
                if  self.Gx_PG-5>=0: #aller à gauche
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
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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
            if keys[pygame.K_UP] or keys[pygame.K_w]: # w=z touche qwerty
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
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
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

        # faire bouger le feu du réacteur
        self.compteur +=1
        if self.compteur<=5:
            self.Hy_PR += 1
            self.Hy_PRC += 1
        elif self.compteur>5 and self.compteur<=10:
            self.Hy_PR -= 1
            self.Hy_PRC -= 1
        elif self.compteur>10:
            self.compteur=0

        # on met à jour la position des points des triangles
        self.trg_PR = [(self.Hx_PR, self.Hy_PR), (self.Gx_PR, self.Gy_PR), (self.Dx_PR, self.Dy_PR)]
        self.trg_PRC = [(self.Hx_PRC, self.Hy_PRC), (self.Gx_PRC, self.Gy_PRC), (self.Dx_PRC, self.Dy_PRC)]

        for meteor in METEORS:
            if meteor.toucher:  # Vérifie si un météore a touché le joueur
                pygame.time.set_timer(self.TIMER_EVENT, 2000)  # Lancer le timer de 2 secondes
                self.HitboxA = pygame.Rect(10000, self.Hy_PG, self.Dx_PD - self.Gx_PG, self.Gy_PG - self.Hy_PG)  # Hitbox vaisseau
                self.HitboxB = pygame.Rect(10000, self.Hy_PP, self.Gx_PD - self.Dx_PG, self.Hy_PG - self.Hy_PP)  # Hitbox vaisseau
                meteor.toucher = False  # Réinitialiser l'état de ce météore
                self.HitboxHS = True

        if event.type == self.TIMER_EVENT:  # Timer de 2 secondes terminé
            self.HitboxHS = False

        if not self.HitboxHS:
            self.HitboxA = pygame.Rect(self.Gx_PG, self.Hy_PG, self.Dx_PD-self.Gx_PG, self.Gy_PG-self.Hy_PG) #Hitbox vaisseau
            self.HitboxB = pygame.Rect(self.Dx_PG, self.Hy_PP, self.Gx_PD-self.Dx_PG, self.Hy_PG-self.Hy_PP) #Hitbox vaisseau

    def tir(self, current_time):
        if current_time - self.DernierTirDelai > self.cooldown and not self.BalleTiree:
            self.BalleTiree = True
            self.DernierTirDelai = current_time
            self.XBalleA, self.YBalleA = self.Hx_PG - 2, self.Hy_PG - int(self.LongBalle/2) # position balle canon gauche
            self.XBalleB, self.YBalleB = self.Hx_PD - 2, self.Hy_PD - int(self.LongBalle/2) #position balle canon droit

    def update_balle(self):
        if self.BalleTiree: # vérifier si les balle n'est pas déjà tirée
            #déplacement de la balle A et sa Hitbox
            self.YBalleA -= self.VitBalle
            self.HitboxBalleA.x = self.XBalleA
            self.HitboxBalleA.y = self.YBalleA
            #déplacement de la balle B et sa Hitbox
            self.YBalleB -= self.VitBalle
            self.HitboxBalleB.x = self.XBalleB
            self.HitboxBalleB.y = self.YBalleB
            #dessiner les balles
            pygame.draw.rect(fenetre, ROUGE_CLAIR, (joueur.XBalleA, joueur.YBalleA, joueur.LargBalle, joueur.LongBalle))
            pygame.draw.rect(fenetre, ROUGE_CLAIR, (joueur.XBalleB, joueur.YBalleB, joueur.LargBalle, joueur.LongBalle))
            # si les balles quittent la fenêtre arrêter le tir
            if self.YBalleA < 0:
                self.BalleTiree = False

joueur = JOUEUR()

class VIE:
    def __init__(self):
        """
        Classe représentant les vaisseaux affichés pour représenter les vies du joueur.

        Chaque vaisseau est constitué de trois parties :
        PP --> Partie principale (largeur 20px, hauteur 10px)
        PG --> Partie gauche (largeur 5px, hauteur 5px)
        PD --> Partie droite (largeur 5px, hauteur 5px)
        """
        # Définir les triangles de base pour un vaisseau
        self.base_vaisseau = {
            "PP": [(20, 10), (14, 40), (26, 40)],  # Partie principale
            "PG": [(14, 18), (11, 40), (17, 40)],  # Partie gauche
            "PD": [(26, 18), (23, 40), (29, 40)], # Partie droite
        }

        # Position de départ pour le premier vaisseau
        self.vaisseaux = []
        for i in range(3):  # Trois vaisseaux représentant les vies
            offset_x = i * 30  # Espacement horizontal entre les vaisseaux
            vaisseau = {
                part: [(x + offset_x, y) for x, y in coords]
                for part, coords in self.base_vaisseau.items()
            }
            self.vaisseaux.append(vaisseau)

        # initialisation de l'explosion en cas de la mort du joeur
        self.kaboum = False
        self.rayon = 1 #rayon de l'explosion avant
        self.rayon2 = 1 #rayon du deuxième cercle d'explosion
        self.x, self.y = 0, 0

    def dessine(self):
        """
        Dessine les vaisseaux en fonction du nombre de vies restantes.
        """
        # Le joueur commence avec 4 vies, dont une est déjà utilisée pour le vaisseau contrôlé.
        # Nous affichons donc les 3 vaisseaux représentant les vies restantes.

        vies_restantes = max(0, joueur.vie - 1)  # Parce que le joueur a déjà un vaisseau actif

        # Limiter à 3 vaisseaux maximum
        for i in range(min(vies_restantes, len(self.vaisseaux))):
            vaisseau = self.vaisseaux[i]
            for part, coords in vaisseau.items():
                color = GRIS_FONCER if part == "PP" else GRIS
                pygame.draw.polygon(fenetre, color, coords)

    def boum(self):
        if self.rayon < 50:
            pygame.draw.circle(fenetre, ORANGE, (self.x, self.y), self.rayon)
            if self.rayon >= 15:
                pygame.draw.circle(fenetre, ORANGE_FONCER, (self.x, self.y), self.rayon2)
                self.rayon2 += 5
            self.rayon += 5
        else:
            self.kaboum = False
            self.rayon, self.rayon2 = 0, 0
        """ici faire le vaisseau qui explose --> meileur en droit pour ne pas bloquer le jeu"""


vie = VIE()

#fin du jeu
def mort():
    fenetre.fill(NOIR)
    pygame.time.delay(500)
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over! Your score is " + str(joueur.score), True, BLANCA)
    text_rect = text.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))
    fenetre.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

#*****************Boucle Principale*****************

font = pygame.font.Font(None, 36)  # Police par défaut, taille 36
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
    joueur.bouge(current_time)

    for meteors in METEORS:
        if not meteors.detruit:
            meteors.bouge()
            meteors.dessine()
        else:
            meteors.dessine_division()
            meteors.bouge_division()
        if vie.kaboum:
            vie.boum()
    #si le joueur tir
    if keys[pygame.K_SPACE] and not joueur.BalleTiree:
        joueur.tir(current_time)

    joueur.update_balle()

    vie.dessine()

    score_text = f"Score: {joueur.score}"
    text_surface = font.render(score_text, True, VERT)
    text_rect = text_surface.get_rect(topright=(LARGEUR - 10, 10))  # En haut à droite avec marge de 10px
    fenetre.blit(text_surface, text_rect)

    pygame.display.update()

    if joueur.vie == 0:
        mort()

    fps.tick(60)
    n += 1
    if n == 10:
        #print(fps)
        n = 0

"""
IDEE :
    l'idée serait de faire en sorte que les réacteurs s'allume seulement si on déplace le vaisseau
    si on déplace le vaisseau à gauche ou à droite --> faire pencher le vaisseau (à faire en dernier)

A FAIRE :
    faire clignoté le joueur quand il respawn --> temps d'invincibilité
    faire cinématique de début (vaisseau qui décolle) --> si le joueur perd on repasse sur cet écran
"""