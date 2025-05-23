import pygame
import sys
import subprocess

# Initialisiere pygame
pygame.init()

# Bildschirmgröße und Farben
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hauptmenü")
font = pygame.font.Font(None, 74)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
red = (255, 0, 0)

# Menüoptionen
menu_options = ["Plane crash", "Bingo", "Snake", "Space shuttle", "Beenden"]
selected_option = 0

def draw_menu():
    screen.fill(black)
    for i, option in enumerate(menu_options):
        color = white if i == selected_option else gray
        if selected_option == 4: # hier muss die gleiche zahl wie bei beenden stehen
            color = red if i == selected_option else gray

        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 7 + i * 100))
        screen.blit(text, text_rect)

def main():
    global selected_option
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    
                    if selected_option == 0:  # Plain crash
                        subprocess.run(["python", ".\Plane crash\Flappy_Jump.py"])  
                    
                    elif selected_option == 1:  # Bingo
                        subprocess.run(["python", ".\Bingo\Bingo.py"])
                
                    elif selected_option == 2:  #Snake
                        subprocess.run(["python", ".\Snake\Snake.py"])

                    elif selected_option == 3:
                        subprocess.run(["python", ".\Spaceshuttle\Spiel_slope.py"])
                
                    elif selected_option == 4:  # Beenden
                        pygame.quit()
                        sys.exit()
                

        draw_menu()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()