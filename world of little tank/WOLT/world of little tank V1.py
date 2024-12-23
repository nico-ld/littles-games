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
        self.speed = 5 #vitesse du tank
        self.width, self.height = 50, 30 #taille du tank
        self.bullet_speed = 50 #vitesse de la balle
        self.bullet_radius = 10 #taille de la balle
        self.bullet_color = ORANGE #couleur de la balle
        self.bullet_xA, self.bullet_yA = int(self.xA + self.width),  int(self.yA + self.height/2)#position de départ de la balle du tank A
        self.canon_xA,  self.canon_yA = int(self.xA + self.width/2), int(self.yA + self.height/2) #position du canon du tank A
        self.bullet_state_A=False
        self.cooldown_time = 600  # 500 milliseconds = 0.5 seconds
        self.last_shot_time = 0
        self.tank_hitbox = pygame.Rect(0, 0, self.width, self.height)
        self.canon_hitbox = pygame.Rect(0, 0, 30, 10)

    def draw_tank(self):
        pygame.draw.rect(window, GREEN, (self.xA, self.yA, self.width,  self.height))
        pygame.draw.circle(window, GREEN_DARKER, (int(self.xA + self.width/2), int(self.yA + self.height/2)), 10)  # draw the tank circle
        pygame.draw.rect(window, GREEN_DARKER, (int(self.xA + self.width/2), int(self.yA + (self.height/2-5)), 30, 10)) #canon du tank
        self.tank_hitbox = pygame.Rect(self.xA, self.yA, self.width,  self.height) #hitbox du tank
        self.canon_hitbox = pygame.Rect(int((self.xA + self.width/2)), int(self.yA + (self.height/2-5)),  30, 10) #hitbox canon


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
            print("votre score est de "  + str(score))
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


#définition nb ennemi
NB_ENEMY = 5

class Enemy_code:
    def __init__(self):
        self.size = 20 #taille ennemi
        self.x, self.y = WIDTH-self.size, random.randint(0,  int(HEIGHT-self.size)) #position initial
        self.color = RED #couleur
        self.speed = random.randint(1, 3) #vitesse
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size) #hitbox

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

enemy_grp = [Enemy_code() for _ in range(NB_ENEMY)]

class life_code:
    def __init__(self):
        self.x, self.y = 10, 10 #position initial
        self.width_life, self.height_life = 202, 24 #taille barre de vie
        self.width_outline, self.height_outline = 202, 24 #taille contour barre de vie
        self.color_outline = (0, 0, 0, 0.5) #couleur contour barre
        self.color = (0, 255, 0, 0.5) #couleur

    def  draw_life(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width_life, self.height_life)) #barre de vie
        pygame.draw.rect(window, self.color_outline, (self.x, self.y, self.width_outline, self.height_outline), 2) #contour barre de vie

    def update_life(self):
        self.width_life -= 20
        if  self.width_life < 10:
            for radius in range(explosion_radius, 81, 5):
                window.fill(BLACK)
                pygame.draw.circle(window, ORANGE, (int(tank.xA+(tank.width/2)), int(tank.yA+(tank.height/2))), radius)
                if radius > 30 :
                    pygame.draw.circle(window, ORANGE_DARKER, (int(tank.xA+(tank.width/2)), int(tank.yA+(tank.height/2))), radius-20)
                pygame.display.flip()
                pygame.time.delay(30)
            window.fill(BLACK)
            pygame.time.delay(500)
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over! Your score is " + str(score), True, WHITE)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            window.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()


life = life_code()


#variable score
score=0
#fonction ennemi toucher
def enemy_touch(score, enemy):
    score += 1
    tank.bullet_state_A = False
    for radius in range(explosion_radius, 51, 5):
        window.fill(WHITE)  # clear the screen
        for e in enemy_grp:
            e.draw_enemy()
        tank.draw_tank()
        pygame.draw.circle(window, ORANGE, (enemy.x+int((enemy.size/2)), enemy.y+int((enemy.size/2))), radius)
        explosion_hitbox=pygame.Rect( enemy.x+int((enemy.size/2))-radius, enemy.y+int((enemy.size/2))-radius, radius*2, radius*2)
        for e in enemy_grp:
            if e != enemy and explosion_hitbox.colliderect(e.hitbox):
                enemy.x = WIDTH - enemy.size
                enemy.y = random.randint(0, HEIGHT - enemy.size)
                enemy.hitbox.x = enemy.x
                enemy.hitbox.y = enemy.y
                enemy_touch(score, e)
        pygame.display.flip()
    enemy.x = WIDTH - enemy.size
    enemy.y = random.randint(0, HEIGHT - enemy.size)
    enemy.hitbox.x = enemy.x
    enemy.hitbox.y = enemy.y
    return score

#*****************************************boucle principale*****************************************
clock=pygame.time.Clock()
while True:
    #pour quitter proprement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("votre score est de "  + str(score))
            pygame.quit()
            sys.exit()
    window.fill(WHITE)
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    life.draw_life()

#gérer la balle du tank
    tank.move_tank(keys)
    if keys[pygame.K_SPACE] and not tank.bullet_state_A:
        tank.shoot(current_time)
    tank.update_bullet()

#detecter les ennemis sortant
    enemies_off_screen=0 #variable qui compte les ennemis sortant

    for enemy in enemy_grp: #on met à jour tout les ennemis présents sur la map
        enemy.update_enemy()

        if enemy.x<=0: #si un ennemi touche le bord gauche
            enemies_off_screen += 1 #on compte pour connaitre le nombre d'ennemis qui touche et donc le nombre de pv à enlever

        for die in range(enemies_off_screen): #on update la vie
            life.update_life()

        if tank.bullet_state_A and tank.bullet_hitbox.colliderect(enemy.hitbox): #si ennemi toucher par la balle
            score = enemy_touch(score, enemy) #on met à jour le score

        if tank.tank_hitbox.colliderect(enemy.hitbox) or tank.canon_hitbox.colliderect(enemy.hitbox): #si tank touche ennemi
            enemy.x = WIDTH - enemy.size
            enemy.y = random.randint(0, HEIGHT - enemy.size)
            enemy.hitbox.x = enemy.x
            enemy.hitbox.y = enemy.y
            life.update_life()
        enemy.draw_enemy()



#on dessine la balle si le tank tire
    if tank.bullet_state_A:
        pygame.draw.circle(window, tank.bullet_color, (tank.bullet_xA, tank.bullet_yA), tank.bullet_radius)
#on dessine le tank
    tank.draw_tank()
    pygame.display.flip()
    # Limiter la vitesse de la boucle à 60 FPS
    clock.tick(60)
