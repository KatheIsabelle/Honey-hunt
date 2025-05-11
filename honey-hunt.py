import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun
import pygame  
from random import randint, choice

WIDTH = 800
HEIGHT = 480
TITLE = "Honey Hunt"
player_SPEED = 7
NUMBER_OF_flower = 10
BORDER_OFFSET = 10

# Redimensiona a imagem da mesa para o tamanho da tela
background_image = pygame.image.load("images/table.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

player = Actor("still")
flower_images = ["flower00", "flower10", "flower20"]
flower_list = []
baddie = Actor("bee")    
game_ticks = 1

# Aumenta a imagem do baddie
original_baddie = pygame.image.load("images/bee.png")
scaled_baddie = pygame.transform.scale(original_baddie, (original_baddie.get_width() * 3, original_baddie.get_height() * 3))  
baddie._surf = scaled_baddie

def draw():
    screen.surface.blit(background_image, (0, 0)) 

    for flower in flower_list:
        flower.draw()

    player.draw()
    baddie.draw()

    if player.dead:
        display_text("You're dead :(", y=100)
        display_text("Press ENTER to play again", y=160)

    if player.won:
        display_text("You're victorious! Let's play again.", y=100)

def display_text(text, y):
    colours_and_offsets = {(10, 10, 10): 3, (255, 0, 255): 0}
    for colour, offset in colours_and_offsets.items():
        screen.draw.text(
            text,
            center=((WIDTH // 2) + offset, y + offset),
            color=colour,
            fontsize=50
        )

def update():
    global game_ticks
    game_ticks += 1
    move_player()
    check_player_flower_collision()
    move_baddie()
    check_player_baddie_collision()

def move_baddie():
    if baddie.dead:
        return

    if baddie.distance_to(player) < 150:
        baddie_speed = randint(6, 7)
    else:
        baddie_speed = 6

    dx, dy = 0, 0
    if baddie.x > player.x:
        dx = -1
    elif baddie.x < player.x:
        dx = 1

    if baddie.y > player.y:
        dy = -1
    elif baddie.y < player.y:
        dy = 1

    if dx != 0 and dy != 0:
        dx *= 0.707
        dy *= 0.707

    baddie.x += dx * baddie_speed
    baddie.y += dy * baddie_speed

def check_player_flower_collision():
    global flower_list
    for flower in flower_list:
        if player.colliderect(flower) and flower.state == "ready":
            flower.state = "eaten"
            sounds.snd_snap.play()
            animate(flower, tween="accelerate", duration=0.1, pos=(flower.x, -50), on_finished=remove_flower(flower))

    flower_list = [flower for flower in flower_list if flower.state != "gone"]

    if len(flower_list) == 0:
        baddie.dead = True
        player.won = True

def check_player_baddie_collision():
    if not baddie.dead and player.collidepoint(baddie.pos):
        player.dead = True
        baddie.dead = True

def remove_flower(flower):
    flower.state = "gone"

def move_player():
    global game_ticks

    if player.dead or player.won:
        if keyboard.RETURN:
            reset_game()
        return

    dx = -1
    if keyboard.left:
        player.x -= player_SPEED
        dx = 0
    if keyboard.right:
        player.x += player_SPEED
        dx = 1
    if keyboard.up:
        player.y -= player_SPEED
    if keyboard.down:
        player.y += player_SPEED

    player.y = min(407, max(15, player.y))
    player.x = min(755, max(40, player.x))

    if dx == -1:
        player.image = "still"
        original = pygame.image.load("images/still.png")
        scaled = pygame.transform.scale(original, (original.get_width() * 2, original.get_height() * 2))  
        player._surf = scaled

    else:
        run_image = "run" + str(dx) + str((game_ticks // 4) % 4)
        player.image = run_image
        original = pygame.image.load(f"images/{run_image}.png")
        scaled = pygame.transform.scale(original, (original.get_width() * 2, original.get_height() * 2))  
        player._surf = scaled

def reset_game():
    global flower_list
    player.pos = WIDTH // 2, HEIGHT // 2
    player.dead = False
    player.won = False

    flower_list = []
    for _ in range(NUMBER_OF_flower):
        flower = Actor(choice(flower_images))
        flower.topleft = randint(BORDER_OFFSET, WIDTH - BORDER_OFFSET - flower.width), \
                         randint(BORDER_OFFSET, HEIGHT - BORDER_OFFSET - flower.height)
        flower.state = "ready"
        flower_list.append(flower)

    baddie.topleft = BORDER_OFFSET, BORDER_OFFSET
    baddie.dead = False

reset_game()
pgzrun.go()
