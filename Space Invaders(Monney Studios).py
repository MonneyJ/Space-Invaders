import pygame
import random
import math
from pygame import mixer

"""
This game was developed by Monney Joshua(Monney Studios)
All images used here are freely allowed permissions from the owners
You need to install python 3,pygame and the pycharm app or any python IDE to run the game
This game can also be run in command prompt
"""
pygame.init()  # This initializes the codes below after this has been declared

# This sets the resolution for your game window
window = pygame.display.set_mode((800, 600))

# game title7
pygame.display.set_caption("Space Invaders")

# icon
title_icon = pygame.image.load("ufo.png")
pygame.display.set_icon(title_icon)  # This sets the game icon

# player
user_player = pygame.image.load("player.png")
user_player_x_position = 370
user_player_y_position = 480

enemy = []
enemy_x_position = []
enemy_y_position = []
enemy_transform_x = []
enemy_transform_y = []
number_of_enemies = 6

enemy_change_speed = 1.5 # Change the speed of the enemies
enemy_opposite_speed = -1.5
for i in range(number_of_enemies):
    enemy.append(pygame.image.load("enemy.png"))
    enemy_x_position.append(random.randint(0, 736))
    enemy_y_position.append(random.randint(50, 150))
    enemy_transform_x.append(enemy_change_speed)
    enemy_transform_y.append(40)

# background
wall = pygame.image.load("background.jpeg")
mixer.music.load("background.wav")
mixer.music.play(-1)

# bullet
bullets = pygame.image.load("bullet.png")
bullet_x_position = 0
bullet_y_position = 480
bullet_y_transform = 3
bullet_state = "ready"

font_position_x = 10
font_position_y = 20

score_value = 0
font_property = pygame.font.Font("freesansbold.ttf", 25)

wall_game_over = pygame.image.load("background_game_over.jpeg")


def player(x, y):  # A function for the user player
    window.blit(user_player, (x, y))  # This blit function draws the image on the game window


# This while loop runs when true and a location for all the active objects in the game

def ui_enemy(x, y, i):
    window.blit(enemy[i], (x, y))


def background():
    window.blit(wall, (0, 0))


def fire_bullets1(x, y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bullets, (x - 8, y))


def fire_bullets2(x, y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bullets, (x + 29, y))


def is_collision(enemy_x_position, enemy_y_position, bullet_x_position, bullet_y_position):
    distance = math.sqrt(
        (math.pow(enemy_x_position - bullet_x_position, 2)) + (math.pow(enemy_y_position - bullet_y_position, 2)))
    if distance < 50:
        return True
    else:
        return False


def show_font(x, y):
    score = font_property.render("Score: " + str(score_value), True, (255, 255, 255))
    window.blit(score, (x, y))


def contact(user_player_x_position, user_player_y_position, enemy_x_position, enemy_y_position):
    distance = math.sqrt(
        (math.pow(user_player_x_position - enemy_x_position, 2)) + (
            math.pow(user_player_y_position - enemy_y_position, 2)))
    if distance < 80:
        return True
    else:
        return False


game_over = pygame.font.Font("Scream Real.ttf", 64)
game_over_x = 170
game_over_y = 180


def game_over_prompt(x, y):
    game_over_text = game_over.render("Game Over", True, (255, 255, 255))
    window.blit(game_over_text, (x, y))


last_question = pygame.font.Font("freesansbold.ttf", 32)
question_x = 110
question_y = 350


def question(x, y):
    question_popup = last_question.render("press Q to quit", True, (255, 255, 255))
    window.blit(question_popup, (x, y))


name = pygame.font.Font("Scream Real.ttf", 16)
name_x = 620
name_y = 560


def monney_studios(x, y):
    studio_name = name.render("MONNEY STUDIOS", True, (255, 255, 0))
    window.blit(studio_name, (x, y))


player_transform_x = 0

execute = True
while execute:

    window.fill((0, 0, 0))  # This sets the colour of the game window(R,G,B)
    background()
    for method in pygame.event.get():
        if method.type == pygame.QUIT:
            execute = False

        if method.type == pygame.KEYDOWN:
            if method.key == pygame.K_LEFT:
                player_transform_x = -2
            if method.key == pygame.K_RIGHT:
                player_transform_x = 2
            if method.key == pygame.K_SPACE:
                fire_bullets1(user_player_x_position, bullet_y_position)
                fire_bullets2(user_player_x_position, bullet_y_position)
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()

        if method.type == pygame.KEYUP:
            if method.key == pygame.K_LEFT or method.key == pygame.K_RIGHT:
                player_transform_x = 0

    user_player_x_position += player_transform_x

    if user_player_x_position <= 0:
        player_transform_x = 0
    elif user_player_x_position >= 736:
        player_transform_x = 0

    for i in range(number_of_enemies):

        user_enemy_contact = contact(user_player_x_position, user_player_y_position, enemy_x_position[i],
                                     enemy_y_position[i])

        if user_enemy_contact:
            window.blit(wall_game_over,(0,0))
            break
        enemy_x_position[i] += enemy_transform_x[i]
        if enemy_x_position[i] <= 0:
            enemy_y_position[i] += enemy_transform_y[i]
            enemy_transform_x[i] = enemy_change_speed
        elif enemy_x_position[i] >= 736:
            enemy_y_position[i] += enemy_transform_y[i]
            enemy_transform_x[i] = enemy_opposite_speed

        collision = is_collision(enemy_x_position[i], enemy_y_position[i], bullet_x_position, bullet_y_position)

        if collision:
            kill_enemies = mixer.Sound("explosion.wav")
            kill_enemies.play()
            bullet_state = "ready"
            bullet_y_position = 480
            enemy_x_position[i] = random.randint(0, 736)
            enemy_y_position[i] = random.randint(50, 150)
            score_value += 1

        ui_enemy(enemy_x_position[i], enemy_y_position[i], i)

    if bullet_y_position <= -35:
        bullet_y_position = 480
        bullet_state = "ready"

    if bullet_y_position == 480:
        bullet_x_position = user_player_x_position
    else:
        bullet_x_position

    if bullet_state == "fire":
        fire_bullets1(bullet_x_position, bullet_y_position)
        fire_bullets2(bullet_x_position, bullet_y_position)
        bullet_y_position -= bullet_y_transform

    monney_studios(name_x, name_y)

    # call
    if user_enemy_contact:
        game_over_prompt(game_over_x, game_over_y)
        show_font(350,300)
        question(question_x, question_y)
        for method in pygame.event.get():
            if method.type == pygame.KEYDOWN:
                if method.key == pygame.K_q:
                    quit()
    else:
        player(user_player_x_position, user_player_y_position)
    show_font(font_position_x, font_position_y)
    pygame.display.update()
