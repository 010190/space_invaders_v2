import sys
import random
import time
from rembg import remove
from PIL import Image
import pygame

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
WIDTH = 640
HEIGHT = 480
SPRITE_HEIGHT = 40
SPRITE_WIDTH = 40
pygame.init()

""""Code responsible for image processing"""
# Image.open(r"bg.jpg").resize((640, 480)).save("bg.jpg")
# Image.open(r"spaceship.png").resize((40, 40)).save("spaceship.png")
# Image.open(r"alien.png").resize((40, 40)).save("alien.png")
#
# for image in ["alien.png", "bullet.png", "spaceship.png"]:
#     img = Image.open(image)
#     rgba = img.convert("RGBA")
#     datas = rgba.getdata()
#
#     newData = []
#     for item in datas:
#         if item[0] == 41 and item[1] == 41 and item[2] == 41:  # finding black colour by its RGB value
#             # storing a transparent value when we find a black colour
#             newData.append((255, 255, 255, 0))
#         else:
#             newData.append(item)  # other colours remain unchanged
#
#     rgba.putdata(newData)
#     rgba.save(f"{image}", "PNG")
#     print("done")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.image.load("spaceship.png").convert_alpha()
background = pygame.image.load("bg.jpg").convert()
entity = pygame.image.load('alien.png').convert_alpha()
bullet = pygame.image.load('bullet.png').convert_alpha()

screen.blit(background, (0, 0))
position = player.get_rect()
pygame.display.update()

running = True


class GameObject:
    def __init__(self, image, x_cord, y_cord, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(x_cord, y_cord)
        self.lives = 3
        self.points = 0
        self.starting_pos = 0

    def move(self, up=False, down=False, left=False, right=False):
        screen.blit(background, self.pos, self.pos)
        if right:
            self.pos.right += self.speed
        if left:
            self.pos.right -= self.speed

        if up:
            self.pos.top -= self.speed

        if down:
            self.pos.top += self.speed

        if self.pos.right > WIDTH:
            self.pos.left = 0

        if self.pos.right < SPRITE_WIDTH:
            self.pos.right = WIDTH


bullet_list = []
bullet_list_alien = []
font = pygame.font.Font('CourierPrime-Regular.ttf', 32)

points = font.render('Points', True, white)
lives = font.render('lives', True, white)

pointsRect = points.get_rect()
livesRect = lives.get_rect()
pointsRect.center = (0, 0)


def make_bullet_player():
    global bullet
    bullet_list = []
    if not bullet_list:
        bullet_object = GameObject(image=bullet, x_cord=p.pos.right, y_cord=p.pos.top - 45, speed=15)
        bullet_list.append(bullet_object)
        return bullet_list


def make_bullet_alien(alien):
    global bullet

    bullet_object = GameObject(image=bullet, x_cord=alien.pos.right, y_cord=alien.pos.top + 45, speed=15)
    bullet_list_alien.append(bullet_object)
    return bullet_list_alien


font = pygame.font.Font("CourierPrime-Regular.ttf", 20)


def write(text, location, color=(255, 255, 255)):
    update(location)
    screen.blit(font.render(text, True, color), location)


def update(location):
    screen.blit(background, location, (location[0], location[1], 140, 80))


objects = []
p = GameObject(player, 300, 440, 3)
n = 0
for y in range(2):
    for x in range(10):
        o = GameObject(entity, 75 + (x * 50), y * 50, 50)
        o.starting_pos = 75 + (x * 50)
        objects.append(o)

while True:
    pygame.event.pump()
    n += 1
    write(text=f"Points: {p.points}", location=(500, 400))
    write(text=f"Lives: {p.lives}", location=(500, 425))
    screen.blit(background, p.pos, p.pos)
    for o in objects:
        screen.blit(background, o.pos, o.pos)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        p.move(left=True)
    if keys[pygame.K_d]:
        p.move(right=True)
    if keys[pygame.K_w]:
        p.move(up=True)
    if keys[pygame.K_SPACE]:
        bullet_list = make_bullet_player()

    for bullet_obj in bullet_list:
        bullet_obj.move(up=True)
        screen.blit(bullet, bullet_obj.pos)
        for alien in objects:
            if abs(bullet_obj.pos.right - alien.pos.right) <= 15 and abs(bullet_obj.pos.top - alien.pos.top) <= 50:
                print(
                    f"hit {objects.index(alien)}, {alien.pos.top, alien.pos.right},{bullet_obj.pos.top, bullet_obj.pos.right} ")
                p.points += 10
                print(p.points)
                screen.blit(background, bullet_obj.pos, bullet_obj.pos)
                screen.blit(background, alien.pos, alien.pos)
                objects.remove(alien)
                try:
                    bullet_list.remove(bullet_obj)
                except ValueError:
                    pass
                pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.blit(p.image, p.pos)
    if n % 20 == 0:
        for o in objects:
            if o.pos[0] == o.starting_pos:
                o.move(right=True)
            else:
                o.move(left=True)

            screen.blit(o.image, o.pos)

        alien_choice = random.choice(objects)
        alien_bullet = make_bullet_alien(alien_choice)
        if alien_bullet is not None:
            for alien_bullet_obj in alien_bullet[:3]:
                alien_bullet_obj.move(down=True)
                screen.blit(bullet, alien_bullet_obj.pos)
                if alien_bullet_obj.pos.top >= 440:
                    screen.blit(background, alien_bullet_obj.pos, alien_bullet_obj.pos)
                    alien_bullet.remove(alien_bullet_obj)
                if abs(alien_bullet_obj.pos.right - p.pos.right) <= 15 and abs(
                        alien_bullet_obj.pos.top - p.pos.top) <= 50:
                    print(
                        f"hit player bullet, {p.pos.top, p.pos.right},{alien_bullet_obj.pos.top, alien_bullet_obj.pos.right} ")
                    screen.blit(background, alien_bullet_obj.pos, alien_bullet_obj.pos)
                    screen.blit(background, p.pos, p.pos)
                    try:
                        alien_bullet.remove(alien_bullet_obj)
                    except ValueError:
                        pass
                    p.lives -= 1
                    print(p.lives)
                    pygame.display.update()
    elif n % 400 == 0:
        for o in objects:
            o.move(down=True)
    else:
        for o in objects:
            screen.blit(o.image, o.pos)
    if p.lives == 0:
        write(text="GAME OVER", location=(250, 200))

    if len(objects) == 0:
        write(text="YOU WON!", location=(250, 200))

    pygame.display.update()
    clock.tick(60)
