import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class FlappyJump:
    def __init__(self, root):
        self.root = root 
        self.root.title("Flappy Jump")

        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="#F7F7F7")
        self.canvas.pack()

        image = Image.open(".\Plane crash\WhatsApp Bild 2025-05-05 um 15.23.00_780c9887.jpg")
        image = image.resize((40, 30))
        self.player_image = ImageTk.PhotoImage(image)

        self.reset_game_state()

        self.root.bind("<space>", self.move_up)
        self.root.bind("<KeyPress>", self.stop_fall)
        self.root.bind("<KeyRelease>", self.start_fall)

        self.fall()

    def reset_game_state(self):
        self.canvas.delete("all")

        self.score = 0
        self.speed = 3
        self.is_falling = True
        self.is_game_over = False

        self.player = self.canvas.create_image(300, 200, image=self.player_image, anchor="center")
        self.score_text = self.canvas.create_text(50, 20, text=f"Score: {self.score}", font=("Arial", 16), fill="black")

        self.towers = []
        self.tower_status = []
        self.tower_spacing = 300

        for tower_num in range(4):
            xcoord = 610 + tower_num * self.tower_spacing
            gap_size = 150
            lower_height = random.randint(50, 200)
            upper_height = self.canvas_height - lower_height - gap_size

            upper_tower = self.canvas.create_rectangle(xcoord, 0, xcoord + 50, upper_height, fill="green")
            lower_tower = self.canvas.create_rectangle(xcoord, self.canvas_height - lower_height, xcoord + 50, self.canvas_height, fill="green")
            self.towers.append([upper_tower, lower_tower])
            self.tower_status.append(False)

        self.top_border = self.canvas.create_rectangle(0, 0, self.canvas_width, 10, fill="red")
        self.bottom_border = self.canvas.create_rectangle(0, self.canvas_height - 10, self.canvas_width, self.canvas_height, fill="red")

        self.move_towers()

    def move_towers(self):
        if not self.canvas.winfo_exists() or self.is_game_over:
            return

        for index, row in enumerate(self.towers):
            for rect in row:
                self.canvas.move(rect, -7, 0)

                coords = self.canvas.coords(rect)
                if coords[2] < 0:
                    gap_size = 180
                    upper_height = random.randint(50, 250)
                    lower_height = self.canvas_height - upper_height - gap_size

                    if rect == row[0]:
                        self.canvas.coords(rect, self.canvas_width + self.tower_spacing, 0,
                                           self.canvas_width + self.tower_spacing + 50, upper_height)
                        self.tower_status[index] = False
                    else:
                        self.canvas.coords(rect, self.canvas_width + self.tower_spacing,
                                           self.canvas_height - lower_height,
                                           self.canvas_width + self.tower_spacing + 50, self.canvas_height)

            player_coords = self.canvas.bbox(self.player)
            if player_coords:
                tower_coords = self.canvas.bbox(row[0])
                if tower_coords[2] < player_coords[0] and not self.tower_status[index]:
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    self.tower_status[index] = True

        self.canvas.tag_raise(self.score_text)
        self.root.after(50, self.move_towers)

    def move_up(self, event):
        for _ in range(60):
            self.canvas.move(self.player, 0, -1)

    def fall(self):
        if not self.canvas.winfo_exists():
            return

        if self.is_falling:
            self.canvas.move(self.player, 0, self.speed)
            self.speed += 0.001

        self.check_collision()
        self.root.after(30, self.fall)

    def stop_fall(self, event):
        self.is_falling = False
        self.speed = 3

    def start_fall(self, event):
        self.is_falling = True

    def check_collision(self):
        coords = self.canvas.bbox(self.player)
        if coords is None:
            return

        top_y = coords[1]
        bottom_y = coords[3]

        if top_y <= 10 or bottom_y >= self.canvas_height - 10:
            self.game_over()

        for tower_group in self.towers:
            for tower in tower_group:
                tower_coords = self.canvas.coords(tower)
                if tower_coords is None:
                    continue
                tx1, ty1, tx2, ty2 = tower_coords
                if coords[2] > tx1 and coords[0] < tx2 and coords[3] > ty1 and coords[1] < ty2:
                    self.game_over()

    def game_over(self):
        self.is_falling = False
        self.speed = 0
        self.is_game_over = True

        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2, text="Game Over", font=("Arial", 30), fill="red")
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 40, text=f"Score: {self.score}", font=("Arial", 20), fill="black")
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 80, text="Drücke R zum Neustart", font=("Arial", 20), fill="black")
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 120, text="Drücke Q zum Beenden", font=("Arial", 20), fill="black")

        self.root.bind("<q>", lambda event: self.root.destroy())
        self.root.bind("<r>", lambda event: self.restart_game())

    def restart_game(self):
        self.reset_game_state()

# Hauptprogramm starten 
if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyJump(root)
    root.mainloop()
