import pygame
import sys

pygame.init()


screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    pygame.display.flip()


pygame.draw.rect(screen, red, [10, 20, 100, 100],2)















pygame.quit()
sys.exit()