from pygame import *
from random import randint
from time import time as timer
#создание окна
screen = display.set_mode((700,500))
display.set_caption('Space Shooter Game')
background = transform.scale(image.load('space-ambient-1024x640.jpg'),(700,500))
#музыка
clock= time.Clock()
fps = 60
mixer.init()
mixer.music.load('background.wav')
mixer.music.play(-1)
mixer.music.load('space.ogg')
mixer.music.play(-1)
player_fire = mixer.Sound('fire.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        screen.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x :
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 10, 20, 30)
        bullets.add(bullet)
score_kills = 0
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            lost += 1
            self.rect.x = randint(300,620)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monsters.add(Enemy('4682279.png',randint(100,620),0,randint(1,3),70,70))
asteroids = sprite.Group()
for i in range(3):
    asteroids.add(Enemy('asteroid.png',randint(100,620),0,randint(1,3),90,90))
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0: 
            self.kill()
font.init()
allien = Enemy('4682279.png',100,50,3,80,50)        
rocket = Player('rocket.png',300,400,5,80,80)
asteroid = Enemy('asteroid.png',200,100,3,80,50)
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 30)
font3 = font.SysFont('Arial', 70)
font4 = font.SysFont('Arial', 70)
font5 = font.SysFont('Arial',25)
game = True
finish = False
rel_time = False
num_fire = 0
while game:
    for e in event.get():
        if e.type==QUIT:
            game = False
        if e.type == KEYDOWN:
            if num_fire < 5:
                if e.key == K_SPACE:
                    rocket.fire()
                    player_fire.play()
                    num_fire += 1
            else:
                rel_time = True
                start_time = timer()
    if finish != True:
        screen.blit(background,(0,0))
        font_lost = font2.render('Losts:'+str(lost), 1, (255, 255, 255))
        font_score = font1.render('Score:'+str(score_kills), 1, (255, 255, 255))
        screen.blit(font_score, (10, 10))
        screen.blit(font_lost, (10, 40))
        bullets.update()
        bullets.draw(screen)
        monsters.update()
        monsters.draw(screen)
        rocket.reset()
        rocket.update()
        if sprite.groupcollide(asteroids, bullets,True, True):
            asteroids.add(Enemy('asteroid.png',randint(100, 620),0,randint(1,3),80,90))
            score_kills += 3
        if sprite.groupcollide(monsters, bullets,True, True):
            monsters.add(Enemy('4682279.png',randint(100, 620),0,randint(1,3),70,70))
            score_kills += 1
        if score_kills >= 30:
            asteroids.draw(screen)
            asteroids.update()
        if score_kills >= 50:
            screen.blit(background,(0,0))
            rocket.reset()
            rocket.update()
            font_win = font3.render('You Win',1,(0,255,0))
            screen.blit(font_win, (255,255))
            finish= True
        if lost >= 30:
            screen.blit(background,(0,0))
            font_lose = font4.render('You Lose',1,(255,0,0))
            screen.blit(font_lose, (250,250))
            finish = True
        
        now_time = timer()
        if rel_time == True and now_time - start_time < 3:
            font_reload = font5.render('waiting reload' +str(round(now_time-start_time,2)), 1, (255, 0, 0))
            screen.blit(font_reload,(530,470))
        elif rel_time == True and now_time - start_time > 3:
            rel_time = False
            num_fire = 0
    else:
        finish = False
        time.delay(1000)
    display.update()
    clock.tick(fps)
    