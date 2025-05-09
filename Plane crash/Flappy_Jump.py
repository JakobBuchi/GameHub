import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class FlappyJump:
    def __init__(self, root):
        self.root = root 
        self.root.title("Flappy Jump")

        # Spielfeld (Canvas) erstellen
        self.canvas_width = 800 #600
        self.canvas_height = 600 #400
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="#F7F7F7")
        self.canvas.pack()

        # Spielerbild laden und skalieren
        image = Image.open(".\Plane crash\WhatsApp Bild 2025-05-05 um 15.23.00_780c9887.jpg")
        image = image.resize((40, 30))  # Spielergröße anpassen
        self.player_image = ImageTk.PhotoImage(image) 
        self.player = self.canvas.create_image(300, 200, image=self.player_image, anchor="center")

        
        #Punktestand (Spieler) initialisieren
        self.score = 0
        self.score_text = self.canvas.create_text(50, 20, text=f"Score: {self.score}", font=("Arial", 16), fill="black")

        # Startgeschwindigkeit und Fall-Status
        self.speed = 3
        self.is_falling = True

        # Hindernisse (Türme) vorbereiten
        self.towers = []
        self.tower_spacing = 300  # Abstand zwischen den Türmen
        self.tower_status = []  # Speichert, ob ein Turm bereits gezählt wurde

        for tower_num in range(4):
            xcoord = 610 + tower_num * self.tower_spacing  # Startpositionen außerhalb des sichtbaren Bereichs
            gap_size = 150  # Lücke zwischen oberem und unterem Turm
            lower_height = random.randint(50, 200)
            upper_height = self.canvas_height - lower_height - gap_size

            # Zwei Rechtecke pro Turm (oben und unten)
            upper_tower = self.canvas.create_rectangle(xcoord, 0, xcoord + 50, upper_height, fill="green")
            lower_tower = self.canvas.create_rectangle(xcoord, self.canvas_height - lower_height, xcoord + 50, self.canvas_height, fill="green")
            self.towers.append([upper_tower, lower_tower])
            self.tower_status.append(False)  # Initialisiere den Status als "nicht gezählt"

        # Rote Begrenzungslinien oben und unten
        self.top_border = self.canvas.create_rectangle(0, 0, self.canvas_width, 10, fill="red")
        self.bottom_border = self.canvas.create_rectangle(0, self.canvas_height - 10, self.canvas_width, self.canvas_height, fill="red")

        # Türme bewegen
        self.move_towers()

        # Tasteneingaben binden
        self.root.bind("<space>", self.move_up)        # Springen
        self.root.bind("<KeyPress>", self.stop_fall)   # Bei Tastendruck fällt Spieler nicht
        self.root.bind("<KeyRelease>", self.start_fall)# Bei Loslassen fällt Spieler weiter

        # Spieler beginnt zu fallen
        self.fall()

    def move_towers(self):
        if not self.canvas.winfo_exists():  # Überprüfen, ob das Canvas noch existiert
            return

        # Bewegt die Türme nach links und setzt sie neu, wenn sie den Bildschirm verlassen.
        for index, row in enumerate(self.towers):
            for rect in row:
                self.canvas.move(rect, -7, 0)  # Bewegung nach links

                coords = self.canvas.coords(rect)
                if coords[2] < 0:  # Wenn rechter Rand des Rechtecks links vom Bildschirm ist
                    gap_size = 180
                    upper_height = random.randint(50, 250)
                    lower_height = self.canvas_height - upper_height - gap_size

                    if rect == row[0]:  # Oberer Turm
                        self.canvas.coords(rect, self.canvas_width + self.tower_spacing, 0, self.canvas_width + self.tower_spacing + 50, upper_height)
                        self.tower_status[index] = False  # Zurücksetzen der "gezählt"-Markierung
                    else:  # Unterer Turm
                        self.canvas.coords(rect, self.canvas_width + self.tower_spacing, self.canvas_height - lower_height, self.canvas_width + self.tower_spacing + 50, self.canvas_height)

            # Überprüfen, ob der Spieler zwischen den Türmen hindurchgeflogen ist
            player_coords = self.canvas.bbox(self.player)  # Bounding Box des Spielers
            if player_coords:
                tower_coords = self.canvas.bbox(row[0])  # Bounding Box des oberen Turms
                if tower_coords[2] < player_coords[0] and not self.tower_status[index]:  # Spieler hat die Türme passiert
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    self.tower_status[index] = True  # Markiere diesen Turm als "gezählt"

        # Hebe den Score-Text über alle anderen Elemente
        self.canvas.tag_raise(self.score_text)

        # Wiederhole die Bewegung der Türme
        self.root.after(50, self.move_towers)

    def move_up(self, event):
        #Lässt den Spieler springen (leicht nach oben bewegen).
        for i in range(60):  # Sanftes Springen (nicht ruckartig)
            self.canvas.move(self.player, 0, -1)


    def fall(self):
        if not self.canvas.winfo_exists():  # Überprüfen, ob das Canvas noch existiert
            return

        # Simuliert den Fall durch die Schwerkraft.
        if self.is_falling:
            self.canvas.move(self.player, 0, self.speed)
            self.speed += 0.001  # Beschleunigung

        self.check_collision()
        self.root.after(30, self.fall)  # Wiederhole alle 30ms

    def stop_fall(self, event):
        #Stoppt den Fall temporär (z. B. beim Tastendruck).
        self.is_falling = False
        self.speed = 3  # Zurücksetzen der Geschwindigkeit

    def start_fall(self, event):
        #Startet den Fall wieder (z. B. nach Loslassen der Taste).
        self.is_falling = True

    def check_collision(self):
        # Prüft, ob der Spieler mit einem Turm oder Rand kollidiert.
        coords = self.canvas.bbox(self.player)  # Bounding Box des Spielers
        if coords is None:
            return

        top_y = coords[1]
        bottom_y = coords[3]

        # Kollision mit oberem oder unterem Rand
        if top_y <= 10 or bottom_y >= self.canvas_height - 10:
            self.game_over()

        # Kollision mit einem Turm
        for tower_group in self.towers:
            for tower in tower_group:
                tower_coords = self.canvas.coords(tower)
                if tower_coords is None:  # Überspringe, wenn der Turm nicht mehr existiert
                    continue
                tx1, ty1, tx2, ty2 = tower_coords
                if coords[2] > tx1 and coords[0] < tx2 and coords[3] > ty1 and coords[1] < ty2:
                    self.game_over()

    def game_over(self):
        #Spielende bei Kollision.
        self.is_falling = False
        self.speed = 0
        self.move_towers = False
        messagebox.showinfo("Game Over", "Du hast eine Grenze berührt!")
        self.root.destroy()

# Hauptprogramm starten 
if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyJump(root)
    root.mainloop()