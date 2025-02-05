import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 1000
WIDTH = 1000

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GOLD = (212, 175, 55)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()  # pygame.Surface(player_size)
# player.fill(COLOR_BLACK)
player_rect = player.get_rect()
# player_speed = [1, 1]
player_move_down = [0, 7]
player_move_right = [7, 0]
player_move_left = [-7, 0]
player_move_up = [0, -7]
enemy_size = (pygame.image.load('enemy.png').get_width(), pygame.image.load('enemy.png').get_height())
print(enemy_size)
bonus_size = (30, 30)


def create_enemy():
    enemy_size = (pygame.image.load('enemy.png').get_width(), pygame.image.load('enemy.png').get_height())
    enemy = pygame.image.load('enemy.png').convert_alpha()  # pygame.Surface(enemy_size)
    # enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_move = [random.randint(-10, -6), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (pygame.image.load('bonus.png').get_width(), pygame.image.load('bonus.png').get_height())
    bonus = pygame.image.load('bonus.png')  # pygame.Surface(bonus_size)
    # bonus.fill(COLOR_GOLD)
    bonus_rect = pygame.Rect(random.randint(200, 800), 0, *bonus_size)
    bonus_move = [0, random.randint(6, 10)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_BONUS, 2000)
enemies = []
bonus_lst = []
score = 0

playing = True

while playing:
    FPS.tick(175)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonus_lst.append(create_bonus())

    # main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    # print(player_rect)
    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left < WIDTH:
        player_rect = player_rect.move(player_move_left)

    if keys[K_UP] and player_rect.top < HEIGHT:
        player_rect = player_rect.move(player_move_up)
    # if type(player_rect[0]) =="<class 'int'>":
    #     print(type(player_rect[0]))

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        # if player_rect.colliderect(enemy[1]):
        #     playing = False
        if pygame.Rect.colliderect(player_rect, enemy[1]):
            playing = False

    for bonus in bonus_lst:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if pygame.Rect.colliderect(player_rect, bonus[1]):
            score += 1
            bonus_lst.pop(bonus_lst.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))

    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))