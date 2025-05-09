import pygame
import random
import time

# Initialisierung von Pygame
pygame.init()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN1 = (210, 180, 140)
BROWN2 = (139, 69, 19)
BROWN3 = (139, 105, 105)
BROWN4 = (205, 102, 29)
BROWN5 = (139, 115, 85)

# Bildschirmgröße
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space shuttle")   

# Hintergrundbild
galaxy_bg = pygame.image.load('.\Spaceshuttle\galaxy_background.webp')
galaxy_bg = pygame.transform.scale(galaxy_bg, (WIDTH, HEIGHT))

# Coin-Bild laden
coin_img = pygame.image.load(".\Spaceshuttle\coin10.png").convert_alpha()
coin_size = 50
coin_img = pygame.transform.scale(coin_img, (coin_size, coin_size))

# Spaceshuttle
ball_img = pygame.image.load(".\Spaceshuttle\spaceshuttle.png").convert_alpha()
ball_size = 40
ball_pos = [WIDTH // 2, HEIGHT * 2 // 3]
ball_speed_x = 5
ball_img = pygame.transform.scale(ball_img, (ball_size, ball_size))

# Objektparameter
object_size = 30
objects = []
green_cubes = []  # Coins werden hier verwaltet
max_objects = 20
object_colors = [BROWN1, BROWN2, BROWN3, BROWN4, BROWN5]

clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 36)

score = 0
high_score = 0

# Countdown
start_ticks = pygame.time.get_ticks()
for i in range(3, 0, -1):
    screen.fill(BLACK)
    text = font.render(str(i), True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

# Hauptschleife
running = True
game_over = False

play_again_text = score_font.render('Press R to play again', True, WHITE)
play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

def reset_game():
    global ball_pos, objects, green_cubes, score, game_over, start_ticks
    ball_pos = [WIDTH // 2, HEIGHT * 2 // 3]
    objects = []
    green_cubes = []
    score = 0
    game_over = False
    start_ticks = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_rect.collidepoint(event.pos):
                reset_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == pygame.K_r:
                reset_game()
    
    
    if not game_over:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and ball_pos[0] - ball_speed_x > 0) or (keys[pygame.K_a] and ball_pos[0] - ball_speed_x > 0):
            ball_pos[0] -= ball_speed_x
        if (keys[pygame.K_RIGHT] and ball_pos[0] + ball_speed_x < WIDTH) or (keys[pygame.K_d] and ball_pos[0] + ball_speed_x < WIDTH):
            ball_pos[0] += ball_speed_x

        if (pygame.time.get_ticks() - start_ticks) > 5000:
            for obj in objects:
                obj[1] += obj[3]
                if obj[1] > HEIGHT:
                    objects.remove(obj)
                    score += 1

            for cube in green_cubes:
                cube[1] += cube[2]
                if cube[1] > HEIGHT:
                    green_cubes.remove(cube)

            if len(objects) < max_objects and random.randint(1, 100) <= min(5 + score // 20, 20):
                x = random.randint(0, WIDTH - object_size)
                y = -object_size
                speed = 5 + (score // 100) * 1.25
                if all(not pygame.Rect(x, y, object_size, object_size).colliderect(
                        pygame.Rect(obj[0], obj[1], object_size, object_size)) for obj in objects):
                    color = random.choice(object_colors)
                    objects.append([x, y, color, speed])

            if len(green_cubes) < 3 and random.randint(1, 500) == 1:
                x = random.randint(0, WIDTH - coin_size)
                y = -coin_size
                speed = 5 + (score // 100) * 1.25
                green_cubes.append([x, y, speed])

            for obj in objects:
                obj_rect = pygame.Rect(obj[0], obj[1], object_size, object_size)
                if obj_rect.colliderect(pygame.Rect(ball_pos[0] - ball_size // 2, ball_pos[1] - ball_size // 2, ball_size, ball_size)):
                    game_over = True
                    if score > high_score:
                        high_score = score

            for cube in green_cubes:
                cube_rect = pygame.Rect(cube[0], cube[1], coin_size, coin_size)
                if cube_rect.colliderect(pygame.Rect(ball_pos[0] - ball_size // 2, ball_pos[1] - ball_size // 2, ball_size, ball_size)):
                    score += 10
                    green_cubes.remove(cube)

        screen.blit(galaxy_bg, (0, 0))
        screen.blit(ball_img, (ball_pos[0] - ball_size // 2, ball_pos[1] - ball_size // 2))
        for obj in objects:
            pygame.draw.rect(screen, obj[2], pygame.Rect(obj[0], obj[1], object_size, object_size))
        for cube in green_cubes:
            screen.blit(coin_img, (cube[0], cube[1]))

        score_text = score_font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))
        high_score_text = score_font.render("Highscore: " + str(high_score), True, WHITE)
        screen.blit(high_score_text, (10, 50))

    if game_over:
        text = font.render('Game Over', True, RED)
        quit_text = score_font.render("Press Q to Quit", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(play_again_text, play_again_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
