import pygame, sys, random

#initialisation de pygame
pygame.init()

#dimension de la fenêtre
WIDTH=1000 #x
HEIGHT=600 #y
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("jeu de tank")

#définition des couleurs
WHITE = (255, 255, 255)
BLACK = (5, 5, 5)
RED = (255, 0, 0)
RED_DARKER = (200, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARKER = (0, 200, 0)
BLUE = (0, 0, 255)
ORANGE =(255,  120, 0)
ORANGE_DARKER =  (200, 80, 0)


#definition rond explosion
explosion_radius = 5

class Tanks_code:
    def __init__(self):
        self.xA, self.yA = WIDTH/4, HEIGHT/2 #position tank A
        self.xB, self.yB = WIDTH*3/4, HEIGHT/2 #position tank B
        self.speed = 5 #vitesse du tank
        self.width, self.height = 50, 30 #taille du tank
        self.bullet_speed = 50 #vitesse de la balle
        self.bullet_radius = 10 #taille de la balle
        self.bullet_color = ORANGE #couleur de la balle
        self.bullet_xA, self.bullet_yA = int(self.xA + self.width),  int(self.yA + self.height/2)#position de départ de la balle du tank A
        self.bullet_xB, self.bullet_yB = int(self.xB - self.width), int(self.yB +self.height/2)#position  de départ de la balle du tank
        self.canon_xA,  self.canon_yA = int(self.xA + self.width/2), int(self.yA + self.height/2) #position du canon du tank A
        self.canon_xB,  self.canon_yB = int(self.xB - self.width/2), int(self.yB + self . height/2)  #position du canon du tank B
        self.bullet_state_A=False
        self.bullet_state_B=False
        self.cooldown_time = 600  # 500 milliseconds = 0.5 seconds
        self.last_shot_time = 0

    def draw_tank(self):
        #tank A
        pygame.draw.rect(window, GREEN, (self.xA, self.yA, self.width,  self.height))
        pygame.draw.circle(window, GREEN_DARKER, (int(self.xA + self.width/2), int(self.yA + self.height/2)), 10)  # draw the tank circle
        pygame.draw.rect(window, GREEN_DARKER, (int(self.xA + self.width/2), int(self.yA + (self.height/2-5)), 30, 10)) #canon du tank
        #tank B
        pygame.draw.rect(window, RED, (self.xB, self.yB, self.width,  self.height))
        pygame.draw.circle(window, RED_DARKER, (int(self.xB + self.width/2), int(self.yB + self.height/2)), 10)  # draw the tank circle
        pygame.draw.rect(window, RED_DARKER, (int(self.xB - 5), int(self.yB + (self.height/2-5)), 30, 10)) # canon du tank



    def move_tank(self, keys):
        #avec ZQSD
        if keys[pygame.K_w]: # w=z touche qwerty
            if self.yA-self.speed>=0:
                self.yA -= self.speed #monter
        if keys[pygame.K_s]:
            if self.yA+self.speed<=(HEIGHT-self.height):
                self.yA += self.speed #descendre
        if keys[pygame.K_a]: # a=q touche qwerty
            if  self.xA-self.speed>=0:
                self.xA -= self.speed #reculer
        if keys[pygame.K_d]:
            if self.xA+self.speed<=(WIDTH-self.width):
                self.xA += self.speed  #avancer

        #avec les flèches
        if keys[pygame.K_LEFT]:
            if  self.xB-self.speed>=0:
                self.xB -= self.speed #reculer
        if keys[pygame.K_RIGHT]:
            if self.xB+self.speed<=(WIDTH-self.width):
                self.xB += self.speed  #avancer
        if keys[pygame.K_UP]:
            if self.yB-self.speed>=0:
                self.yB -= self.speed #monter
        if keys[pygame.K_DOWN]:
            if self.yB+self.speed<=(HEIGHT-self.height):
                self.yB += self.speed #descendre
        if keys[pygame.K_l]:
            pygame.quit()
            sys.exit()

    def shoot(self, current_time):
        if current_time - self.last_shot_time > self.cooldown_time and not self.bullet_state_A:
            self.bullet_xA = int(self.xA + self.width)
            self.bullet_yA = int(self.yA + self.height/2)
            self.bullet_state_A = True
            self.last_shot_time = current_time
            self.bullet_hitbox = pygame.Rect(self.bullet_xA - self.bullet_radius, self.bullet_yA - self.bullet_radius, self.bullet_radius*2, self.bullet_radius*2) #hitbox balle

    def update_bullet(self):
        if self.bullet_state_A:
            self.bullet_xA += self.bullet_speed
            self.bullet_hitbox.x = self.bullet_xA - self.bullet_radius
            self.bullet_hitbox.y = self.bullet_yA - self.bullet_radius
            if self.bullet_xA > WIDTH:
                self.bullet_state_A = False
    
    
tank=Tanks_code()


#*****************************************boucle principale*****************************************
clock=pygame.time.Clock()
while True:
    #pour quitter proprement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    window.fill(WHITE)
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    tank.move_tank(keys)
    if keys[pygame.K_SPACE] and not tank.bullet_state_A:
        tank.shoot(current_time)
    tank.update_bullet()
    
    
    

    if tank.bullet_state_A:
        pygame.draw.circle(window, tank.bullet_color, (tank.bullet_xA, tank.bullet_yA), tank.bullet_radius)
    tank.draw_tank()
    pygame.display.flip()
    # Limiter la vitesse de la boucle à 60 FPS
    clock.tick(60)
