import tkinter as tk
from tkinter import messagebox

def start_bingo():
    global score
    score = 0
    score_label.config(text=f"Punkte: {score}")
    
    terms = entry.get("1.0", tk.END).strip().split("\n")
    terms = [term.strip() for term in terms if term.strip()]
    
    if len(terms) < 1 or len(terms) > 9:
        result_label.config(text="Bitte gib zwischen 1 und 9 Begriffe ein.")
        return
    
    grid_size = 3  # Immer eine 3x3 Tabelle
    
    clear_board()
    
    for i in range(grid_size):
        for j in range(grid_size):
            idx = i * grid_size + j
            term = terms[idx] if idx < len(terms) else ""
            btn = tk.Button(board_frame, text=term, width=15, height=4, font=("Arial", 14, "bold"),
                            relief="raised")
            btn.config(command=lambda b=btn, t=term: toggle_bingo(b, t))
            btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
            buttons.append(btn)
    
    for i in range(grid_size):
        board_frame.columnconfigure(i, weight=1)
        board_frame.rowconfigure(i, weight=1)
    
    result_label.config(text="Klicke auf Begriffe, um sie zu markieren!")

def toggle_bingo(button, term):
    global score
    if term == "":
        return  # Keine Punkte für leere Felder vergeben
    
    if button.config('relief')[-1] == 'sunken':
        button.config(relief="raised", bg="SystemButtonFace")
        score -= 1
    else:
        button.config(relief="sunken", bg="lightgreen")
        score += 1
    score_label.config(text=f"Punkte: {score}")

def clear_entries():
    entry.delete("1.0", tk.END)
    clear_board()
    result_label.config(text="Eingaben und Tabelle wurden gelöscht.")

def clear_board():
    for widget in board_frame.winfo_children():
        widget.destroy()
    buttons.clear()
    global score
    score = 0
    score_label.config(text=f"Punkte: {score}")

root = tk.Tk()
root.title("Bingo Spiel")

score = 0 
score_label = tk.Label(root, text=f"Punkte: {score}", font=("Arial", 12, "bold"))
score_label.pack(anchor="nw", padx=10, pady=5)

instruction_label = tk.Label(root, text="Gib zwischen 1 und 9 Begriffe ein (jeweils in einer neuen Zeile):")
instruction_label.pack()

entry = tk.Text(root, height=6, width=30)
entry.pack()

button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(button_frame, text="Bingo starten", command=start_bingo)
start_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Eingaben löschen", command=clear_entries)
clear_button.pack(side=tk.LEFT, padx=5)

board_frame = tk.Frame(root)
board_frame.pack(pady=10, expand=True, fill="both")

result_label = tk.Label(root, text="")
result_label.pack()

buttons = []

root.mainloop()
