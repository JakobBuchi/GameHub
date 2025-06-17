import pygame
import sys
import subprocess

# Initialisiere pygame
pygame.init()

# Bildschirmgröße und Farben
screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hauptmenü")
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
red = (255, 0, 0)
highlight = (0, 255, 0)

# Menüoptionen und zugehörige Bildpfade
menu_options = ["Plane crash", "Bingo", "Snake", "Space shuttle", "Beenden"]
image_paths = [
    "./APP_Icon_PlaneCrash.png",
    "./APP_Icon_Bingo.png",
    "./APP_Icon_Snake.png",
    "./APP_Icon_Spaceshuttle.png",
    "./APP_Icon_Exit.png"
]

def load_and_scale(path, size=(128, 128)):
    if path:
        img = pygame.image.load(path)
        return pygame.transform.smoothscale(img, size)
    return None

menu_images = [load_and_scale(path) for path in image_paths]

selected_option = 0

def draw_menu():
    screen.fill(black)
    icon_size = 128
    spacing = 40
    total_icons = len(menu_images)
    total_width = total_icons * icon_size + (total_icons - 1) * spacing
    start_x = (screen_width - total_width) // 2
    y = screen_height // 2 - icon_size // 2

    for i, image in enumerate(menu_images):
        x = start_x + i * (icon_size + spacing)
        if image:
            screen.blit(image, (x, y))
            # Rahmen um das ausgewählte Icon
            if i == selected_option:
                pygame.draw.rect(screen, highlight, (x-4, y-4, icon_size+8, icon_size+8), 4)
        else:
            # Optional: Für "Beenden" ein rotes Quadrat anzeigen
            if i == selected_option:
                pygame.draw.rect(screen, red, (x-4, y-4, icon_size+8, icon_size+8), 4)
            pygame.draw.rect(screen, gray, (x, y, icon_size, icon_size))

def main():
    global selected_option
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Plane crash
                        subprocess.run(["python", "./Plane crash/Flappy_Jump.py"])
                    elif selected_option == 1:  # Bingo
                        subprocess.run(["python", "./Bingo/Bingo.py"])
                    elif selected_option == 2:  # Snake
                        subprocess.run(["python", "./Snake/Snake.py"])
                    elif selected_option == 3:  # Space shuttle
                        subprocess.run(["python", "./Spaceshuttle/Spiel_slope.py"])
                    elif selected_option == 4:  # Beenden
                        pygame.quit()
                        sys.exit()

        draw_menu()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()