import pygame, sys, random, time

#initialisation de pygame
pygame.init()

#dimension de la fenêtre
WIDTH=1000 #x
HEIGHT=600 #y
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("design ennemi")

#définition des couleurs
WHITE = (255, 255, 255)
BLACK = (5, 5, 5)
RED = (255, 0, 0)
RED_DARKER = (200, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARKER = (0, 200, 0)
BLUE = (0, 0, 255)
ORANGE =(255,  120, 0)
ORANGE_DARKER =  (225, 100, 0)
ORANGE_MORE_DARKER = (200, 80, 0)

class Tanks_code:
    def __init__(self):
        self.xA, self.yA = WIDTH/4, HEIGHT/2 #position tank A
        """self.xB, self.yB = WIDTH*3/4, HEIGHT/2 #position tank B"""
        self.speed = 5 #vitesse du tank
        self.width, self.height = 50, 30 #taille du tank
        self.color = GREEN #couleur du tank
        self.bullet_speed = 50 #vitesse de la balle
        self.bullet_radius = 10 #taille de la balle
        self.bullet_color = ORANGE #couleur de la balle
        self.bullet_xA, self.bullet_yA = int(self.xA + self.width),  int(self.yA + self.height/2)#position de départ de la balle du tank A
        self.canon_xA,  self.canon_yA = int(self.xA + self.width/2), int(self.yA + self.height/2) #position du canon du tank A
        self.bullet_state_A=False
        self.cooldown_time = 600  # 500 milliseconds = 0.5 seconds
        self.last_shot_time = 0
        """self.bullet_xB, self.bullet_yB = self.xB - self.width, self.yB/2#position  de départ de la balle du tank B"""

    def draw_tank(self):
        pygame.draw.rect(window, self.color, (self.xA, self.yA, self.width,  self.height))
        pygame.draw.circle(window, GREEN_DARKER, (int(self.xA + self.width/2), int(self.yA + self.height/2)), 10)  # draw the tank circle
        pygame.draw.rect(window, GREEN_DARKER, (int(self.xA + self.width/2), int(self.yA + (self.height/2-5)), 30, 10)) #canon du tank


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
            if  self.xA-self.speed>=0:
                self.xA -= self.speed #reculer
        if keys[pygame.K_RIGHT]:
            if self.xA+self.speed<=(WIDTH-self.width):
                self.xA += self.speed  #avancer
        if keys[pygame.K_UP]:
            if self.yA-self.speed>=0:
                self.yA -= self.speed #monter
        if keys[pygame.K_DOWN]:
            if self.yA+self.speed<=(HEIGHT-self.height):
                self.yA += self.speed #descendre
        if keys[pygame.K_l]:
            pygame.quit()
            sys.exit()

        #bonus
        if  keys[pygame.K_z]: #bouclier (z=w touche qwerty)
            shield_time = pygame.time.get_ticks()
            if shield_time<3000:
                pygame.draw.circle(window, BLUE, (int(self.xA + self.width/2), int(self.yA + self.height/2)), 40, 2)  # draw the tank circle
                pygame.display.update()

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

class Enemy_code:
    def __init__(self):
        self.size = 20 #taille ennemi
        self.x, self.y = WIDTH-self.size, random.randint(0,  int(HEIGHT-self.size)) #position initial
        self.color = RED #couleur
        self.speed = random.randint(1, 3) #vitesse
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size) #hitbox
        self.bullet_speed = 25
        self.bullet_radius = 10 #taille de la balle
        self.bullet_color = ORANGE #couleur de la balle
        self.bullet_x, self.bullet_y = self.x, self.y#position de départ de la balle du tank A
        self.bullet_state=False
        self.cooldown_time_E = 1500  # 500 milliseconds = 0.5 seconds
        self.last_shot_time_E = 0

    def draw_enemy(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def update_enemy(self):
        self.x -= self.speed
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        if self.x < 0:
            self.x, self.y = WIDTH-self.size, random.randint(0,  int(HEIGHT-self.size)) #position initial
            self.hitbox.x = self.x
            self.hitbox.y = self.y

    def shoot(self, current_time):
        if current_time - self.last_shot_time_E > self.cooldown_time_E and not self.bullet_state:
            print("enemy is shooting")
            self.bullet_x = self.y
            self.bullet_y = self.y
            self.bullet_state = True
            self.last_shot_time_E = current_time
            self.bullet_hitbox = pygame.Rect(self.bullet_x - self.bullet_radius, self.bullet_y - self.bullet_radius, self.bullet_radius*2, self.bullet_radius*2) #hitbox balle

    def update_bullet(self):
        if self.bullet_state:
            self.bullet_x = int((tank.xA-self.x) + self.bullet_speed)
            self.bullet_y = int((tank.yA-self.y) + self.bullet_speed)
            self.bullet_hitbox.x = self.bullet_x - self.bullet_radius
            self.bullet_hitbox.y = self.bullet_y - self.bullet_radius
            if self.bullet_x > WIDTH or self.bullet_x <= 0 or self.bullet_y > HEIGHT or self.bullet_y <= 0:
                self.bullet_state = False

    def draw_bullet(self):
        if self.bullet_state:
            pygame.draw.circle(window, self.bullet_color, (int(self.bullet_x), int(self.bullet_y)), self.bullet_radius)
            print("bullet draw")
enemy=Enemy_code()

def nuke(keys):
    if keys[pygame.K_v]:
        first_nuke_radius = 600
        second_nuke_radius = 50
        last_nuke_radius = 30
        for one in range(first_nuke_radius, 10, -10):
            pygame.draw.circle(window, RED, (int(WIDTH/2), int(HEIGHT/2)), one, 2)
            pygame.display.flip()
            pygame.time.delay(30)
            window.fill(WHITE)
        time.sleep(0.5)
        for two in range(second_nuke_radius, 1, -1):
            pygame.draw.circle(window, BLACK, (int(WIDTH/2), int(HEIGHT/2)), two)
            pygame.display.flip()
            pygame.time.delay(30)
            window.fill(WHITE)
        for i in range(3):
            for three in range(last_nuke_radius, 600, 30):
                pygame.draw.circle(window, ORANGE, (int(WIDTH/2), int(HEIGHT/2)),three)
                if three > 120:
                    pygame.draw.circle(window, ORANGE_DARKER, (int(WIDTH/2), int(HEIGHT/2)),  three-120)
                if  three > 240:
                    pygame.draw.circle(window, ORANGE_MORE_DARKER, (int(WIDTH/2), int(HEIGHT/2)), three-240)
                pygame.display.flip()
                pygame.time.delay(30)
        time.sleep(1)





#*****************************************boucle principale
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
    nuke(keys)
    tank.move_tank(keys)
    enemy.update_enemy()
    enemy.shoot(current_time)
    enemy.update_bullet()
    enemy.draw_bullet()
    enemy.draw_enemy()
    tank.draw_tank()
    pygame.display.flip()
    # Limiter la vitesse de la boucle à 60 FPS
    clock.tick(60)
