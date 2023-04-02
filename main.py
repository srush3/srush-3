from pygame import *
from random import *
import   time as time_module

mixer.init()
mixer.music.load("space (1).ogg")
mixer.music.play(-1)

window = display.set_mode((700,500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image) , (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = player_width
        self.height = player_height
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - self.width - 5:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet (1).png", self.rect.centerx - 7, self.rect.top, -5, 15, 20)
        bullets.add(bullet)


class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()
 
lost = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700-70-5)
            lost = lost + 1

monster = Enemy("ufo (2).png", randint(0,700-70-5), 0, randint(1,2), 30,30)
monster2 = Enemy("ufo (2).png", randint(0,700-70-5), 0, randint(1,2), 30,30)
monster3 = Enemy("ufo (2).png", randint(0,700-70-5), 0, randint(1,2), 30,30)
monster4 = Enemy("ufo (2).png", randint(0,700-70-5), 0, randint(1,2), 40,40)
monster5 = Enemy("ufo (2).png", randint(0,700-70-5), 0, randint(1,2), 50,50)

monsters = sprite.Group()
monsters.add(monster)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

asteroids = sprite.Group()
asteroid1 = Enemy("asteroid (2).png", randint(0,700-70-5), 0, randint(1,2), 30,30)
asteroid2 = Enemy("asteroid (2).png", randint(0,700-70-5), 0, randint(1,2), 30,30)
asteroid3 = Enemy("asteroid (2).png", randint(0,700-70-5), 0, randint(1,2), 30,30)

asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)


font.init()
font = font.SysFont('Arial', 40)
win = font.render("Winner Winner Chiken Dinner", True, (0, 255, 0))
lose = font.render("HAH, LDH!!!", True, (255, 0, 0))
perez = font.render("ТОРМОЗИ!!!", True, (255, 255, 255))


background = transform.scale(image.load("galaxy (1).jpg"), (700,500))

hero = Player("rocket (1).png", 50, 420, 5, 50,80)

game = True

clock = time.Clock()
finish = False
score = 0
num_fire = 0
rel_time = False
start_time = 0
while game:


    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    hero.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start_time = time_module.time()
                    num_fire = 0
    if finish != True:
        window.blit(background, (0, 0))
        hero.reset()
        hero.update()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            window.blit(lose, (200, 200))

        if sprite.spritecollide(hero, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))

        sprite_list2 = sprite.groupcollide(monsters, bullets, True, True)
        for e in sprite_list2:
            score += 1
            monster = Enemy("ufo (2).png", randint(0, 700 - 70 - 5), 0, randint(1, 4), 40, 40)
            monsters.add(monster)

        lost_label = font.render("ПропUщено: " + str(lost), 1, (255, 255, 255))
        window.blit(lost_label,(20,20))
        lost_label2 = font.render("Сбито:" + str(score), 1, (255, 255, 255))
        window.blit(lost_label2,(20,60))

        if lost >= 5:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 15:
            finish = True
            window.blit(win, (150, 200))

        end_time = time_module.time()
        if int(end_time - start_time) < 3:
            window.blit(perez, (250, 450))
            pass
        else:
            rel_time = False




    display.update()
    clock.tick(60)