import pygame
import sys
import random

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 36)  # Neue kleinere Schrift für den Score

rect_height = 20
rect_width = 20
x = screen_width // 2
y = screen_height // 2
block_size = rect_width  # Blockgröße für Bewegung
speed_x = 0
speed_y = 0

# Schlange als Liste von Segmenten (je ein Tupel für x, y)
snake = [(x, y)]

radius = 10
circle_x = random.randint(radius, screen_width - radius)
circle_y = random.randint(radius, screen_height - radius)


def game_over():
    font = pygame.font.SysFont("Arial", 50)
    text = font.render("Game Over", True, red)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(1000)
    quit_text = font.render("Press Q to Quit", True, red)
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 50))
    play_again_text = font.render("Press R to Play Again", True, red)
    screen.blit(play_again_text, (screen_width // 2 - play_again_text.get_width() // 2, screen_height // 2 + 100))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    # Spiel zurücksetzen
                    global x, y, speed_x, speed_y, snake, Score
                    x = screen_width // 2
                    y = screen_height // 2
                    speed_x = 0
                    speed_y = 0
                    snake = [(x, y)]
                    Score = 0
                    return  # Zurück zur Hauptschleife

Score = 0
Highscore = Score

def apple_collision():
    global Highscore, circle_x, circle_y, snake
    global Score, circle_x, circle_y, snake
    tolerance = 5  # Toleranzbereich für die Kollision
    if (
        x < circle_x + radius + tolerance
        and x + rect_width > circle_x - tolerance
        and y < circle_y + radius + tolerance
        and y + rect_height > circle_y - tolerance
    ):
        circle_x = random.randint(radius, screen_width - radius)
        circle_y = random.randint(radius, screen_height - radius)
        Score = Score + 1
        
        if Score > Highscore:
            Highscore = Score

        # Neuen Block anhängen (am Ende der Schlange)
        snake.append((snake[-1][0], snake[-1][1]))
        

def self_collision():
    # Überprüfen, ob der Kopf der Schlange mit einem anderen Segment kollidiert
    for segment in snake[1:]:
        if x == segment[0] and y == segment[1]:
            game_over()


clock = pygame.time.Clock()
running = True

# Hauptspiel-Loop
while running:
    clock.tick(10)  # 10 FPS für blockweise Bewegung
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Richtung basierend auf Tasteneingabe ändern
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and speed_x == 0:  # Nach links
        speed_x = -block_size
        speed_y = 0
    elif keys[pygame.K_d] and speed_x == 0:  # Nach rechts
        speed_x = block_size
        speed_y = 0
    elif keys[pygame.K_w] and speed_y == 0:  # Nach oben
        speed_x = 0
        speed_y = -block_size
    elif keys[pygame.K_s] and speed_y == 0:  # Nach unten
        speed_x = 0
        speed_y = block_size

    # Neue Position berechnen (blockweise Bewegung)
    x += speed_x
    y += speed_y

    # Schlange bewegen: neues Kopfsegment vorne einfügen, letztes entfernen
    snake.insert(0, (x, y))
    if len(snake) > Score + 1:
        snake.pop()

    boarder_x = screen_width - rect_width
    boarder_y = screen_height - rect_height
    if x < 0:
        x = 0
        game_over()
    elif x > boarder_x:
        x = boarder_x
        game_over()
    if y < 0:
        y = 0
        game_over()
    elif y > boarder_y:
        y = boarder_y
        game_over()

    self_collision()
    
    apple_collision()
    screen.fill(black)
    pygame.draw.circle(screen, red, (circle_x, circle_y), radius)
    for segment in snake:
        pygame.draw.rect(screen, green, (segment[0], segment[1], rect_width, rect_height))

    # Score oben links anzeigen
    score_text = score_font.render("Score: " + str(Score), True, white)
    screen.blit(score_text, (10, 10))

    Highscore_text = score_font.render("Highscore: " + str(Highscore), True, white)
    screen.blit(Highscore_text, (10, 40))

    pygame.display.flip()

pygame.quit()
sys.exit()