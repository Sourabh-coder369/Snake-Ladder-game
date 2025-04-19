import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

class SnakeLadderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake & Ladder")

        self.board = tk.Canvas(self.window, width=500, height=500, bg="white")
        self.board.pack()

        self.roll_btn = tk.Button(self.window, text="Roll Dice", command=self.roll_dice)
        self.roll_btn.pack()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = simpledialog.askstring("Name", "Enter your name:")

        self.positions = {}
        self.tokens = {}
        self.colors = ["red", "blue", "green", "orange", "purple", "pink"]

        self.draw_board()
        self.connect()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def draw_board(self):
        size = 50
        # Draw 10x10 grid
        for row in range(10):
            for col in range(10):
                x1 = col * size
                y1 = (9 - row) * size
                x2 = x1 + size
                y2 = y1 + size
                cell_number = row * 10 + (col + 1 if row % 2 == 0 else 10 - col)
                self.board.create_rectangle(x1, y1, x2, y2, outline="black")
                self.board.create_text(x1 + 25, y1 + 25, text=str(cell_number), font=("Arial", 8))

        # Draw ladders (green)
        ladders = {
            2: 38, 4: 14, 9: 31, 21: 42,
            28: 84, 36: 44, 51: 67, 71: 91, 80: 100
        }
        for start, end in ladders.items():
            x1, y1 = self.get_coords(start)
            x2, y2 = self.get_coords(end)
            self.board.create_line(x1, y1, x2, y2, fill="green", width=3, arrow=tk.LAST)

        # Draw snakes (red)
        snakes = {
            16: 6, 47: 26, 49: 11, 56: 53,
            62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78
        }
        for start, end in snakes.items():
            x1, y1 = self.get_coords(start)
            x2, y2 = self.get_coords(end)
            self.board.create_line(x1, y1, x2, y2, fill="red", width=3, arrow=tk.LAST)

    def get_coords(self, pos):
        if pos < 1 or pos > 100:
            return (-100, -100)
        row = (pos - 1) // 10
        col = (pos - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        x = col * 50 + 25
        y = (9 - row) * 50 + 25
        return (x, y)

    def draw_tokens(self):
        self.board.delete("token")
        for i, (player, pos) in enumerate(self.positions.items()):
            x, y = self.get_coords(pos)
            color = self.colors[i % len(self.colors)]
            self.board.create_oval(x-10, y-10, x+10, y+10, fill=color, tags="token")
            self.board.create_text(x, y, text=player[0], font=("Arial", 8), tags="token", fill="white")

    def connect(self):
        try:
            self.client.connect(('192.168.204.139', 12345))
            self.client.send(self.name.encode())
            threading.Thread(target=self.receive_data).start()
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def receive_data(self):
        while True:
            try:
                msg = self.client.recv(1024).decode()
                if msg.startswith("positions:"):
                    self.positions = eval(msg.split(":", 1)[1])
                    self.draw_tokens()
                elif "wins the game!" in msg:
                    messagebox.showinfo("Game Over", msg)
                    self.on_close()
                    break
            except:
                break

    def roll_dice(self):
        self.client.send("roll".encode())

    def on_close(self):
        self.client.close()
        self.window.destroy()

if __name__ == "__main__":
    SnakeLadderGUI()

