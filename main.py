import tkinter as tk
from tkinter import ttk
import subprocess
import os

def start_game(script_name, time=None, fen=None):
    command = ["python", script_name]
    if time:
        command += ["--time", str(time)]
    if fen:
        command += ["--fen", fen]
    subprocess.Popen(command)

def start_two_player():
    time_limit = int(time_entry.get()) * 60 if time_entry.get() else None
    start_game("two_player.py", time_limit)

def start_two_player_from_fen():
    if os.path.exists('chess_position.fen'):
        with open('chess_position.fen', 'r') as f:
            fen = f.read().strip()
        time_limit = int(time_entry.get()) * 60 if time_entry.get() else None
        start_game("two_player.py", time_limit, fen)
    else:
        print("No saved FEN file found.")

def start_analysis():
    start_game("analyze.py")

app = tk.Tk()
app.title("Chess Game")

# Time Entry
tk.Label(app, text="Time for each player (minutes):").pack()
time_entry = tk.Entry(app)
time_entry.pack()

# Buttons
tk.Button(app, text="Start Two Player Game", command=start_two_player).pack(pady=10)
tk.Button(app, text="Start Two Player Game from Saved FEN", command=start_two_player_from_fen).pack(pady=10)
tk.Button(app, text="Start Analysis Board", command=start_analysis).pack(pady=10)

app.mainloop()
