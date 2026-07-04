import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import platform
import time
import os

if platform.system() == "Windows":
    import winsound

class ChessTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Chess Timer")
        self.root.geometry("500x850")

        self.default_time = 10 * 60 * 100
        self.increment = 0
        self.white_time = self.default_time
        self.black_time = self.default_time
        
        self.white_moves = 0
        self.black_moves = 0
        self.active = None
        self.running = False

        self.last_update = time.perf_counter()

        self.canvas = tk.Canvas(root, highlightthickness=0, bg="#1a1a1a")
        self.canvas.pack(fill="both", expand=True)

        self.black_rect = self.canvas.create_rectangle(0, 0, 0, 0, fill="", outline="")
        self.white_rect = self.canvas.create_rectangle(0, 0, 0, 0, fill="", outline="")

        self.black_text = self.canvas.create_text(0, 0, text="10:00.00", fill="white", font=("Courier", 35, "bold"), angle=180)
        self.white_text = self.canvas.create_text(0, 0, text="10:00.00", fill="white", font=("Courier", 35, "bold"))
        
        self.black_move_label = self.canvas.create_text(0,0, text="Moves: 0", fill="#aaa", font=("Arial", 14), angle=180)
        self.white_move_label = self.canvas.create_text(0,0, text="Moves: 0", fill="#aaa", font=("Arial", 14))

        self.button_frame = tk.Frame(self.canvas, bg="#333", padx=8, pady=8)
        self.buttons_window = self.canvas.create_window(0, 0, window=self.button_frame)
        self.setup_buttons()

        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("r", lambda e: self.reset_timer())
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Configure>", lambda e: self.layout())

        self.update_clock()

    def setup_buttons(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10))
        ttk.Button(self.button_frame, text="Start/Pause", command=self.toggle_pause).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Reset", command=self.reset_timer).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Set", command=self.set_timer).pack(side="left", padx=5)

    def layout(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 10:
            return

        self.canvas.coords(self.black_rect, 0, 0, w, h//2)
        self.canvas.coords(self.white_rect, 0, h//2, w, h)
        
        self.canvas.coords(self.black_text, w // 2, h * 0.25)
        self.canvas.coords(self.black_move_label, w // 2, h * 0.10)
        self.canvas.coords(self.white_text, w // 2, h * 0.75)
        self.canvas.coords(self.white_move_label, w // 2, h * 0.90)
        self.canvas.coords(self.buttons_window, w // 2, h // 2)

    def toggle_pause(self):
        self.running = not self.running
        if self.running and self.active is None:
            self.active = "white"

    def update_labels(self):
        wc = "#ba2525" if self.white_time <= 6000 else "white"
        bc = "#ba2525" if self.black_time <= 6000 else "white"

        self.canvas.itemconfig(self.white_text, text=self.format_time(self.white_time), fill=wc)
        self.canvas.itemconfig(self.black_text, text=self.format_time(self.black_time), fill=bc)
        self.canvas.itemconfig(self.white_move_label, text=f"Moves: {self.white_moves}")
        self.canvas.itemconfig(self.black_move_label, text=f"Moves: {self.black_moves}")

        self.canvas.itemconfig(self.white_rect, fill="#2c3e50" if self.active == "white" and self.running else "")
        self.canvas.itemconfig(self.black_rect, fill="#2c3e50" if self.active == "black" and self.running else "")

    def play_click(self):
        if platform.system() == "Windows":
            base_path = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(base_path, "click.wav")
            if os.path.exists(sound_path):
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                self.root.bell()
        else:
            self.root.bell()

    def on_click(self, event):
        if not self.running:
            return
        h = self.canvas.winfo_height()

        if event.y > h / 2 and self.active == "white":
            self.white_time += self.increment
            self.white_moves += 1
            self.active = "black"
            self.play_click()
        elif event.y < h / 2 and self.active == "black":
            self.black_time += self.increment
            self.black_moves += 1
            self.active = "white"
            self.play_click()
        self.update_labels()

    def update_clock(self):
        now = time.perf_counter()
        elapsed = (now - self.last_update) * 100
        self.last_update = now

        if self.running:
            if self.active == "white":
                self.white_time -= elapsed
            else:
                self.black_time -= elapsed

            if self.white_time <= 0 or self.black_time <= 0:
                self.running = False
                winner = "Black" if self.white_time <= 0 else "White"
                self.play_beep()
                messagebox.showinfo("Game Over", f"Time is up! {winner} wins.")
            
            self.update_labels()
        self.root.after(10, self.update_clock)

    def format_time(self, t):
        t = max(0, int(t))
        s, hs = divmod(t, 100)
        m, s = divmod(s, 60)
        return f"{m:02}:{s:02}.{hs:02}"

    def play_beep(self):
        if platform.system() == "Windows":
            winsound.Beep(800, 500)
        else:
            self.root.bell()

    def reset_timer(self):
        self.running = False
        self.active = None
        self.white_time = self.default_time
        self.black_time = self.default_time
        self.white_moves = 0
        self.black_moves = 0
        self.update_labels()

    def set_timer(self):
        s = simpledialog.askstring("Set Timer", "Minutes + Increment (e.g., 3 2)")
        if s:
            try:
                parts = s.split()
                m = int(parts[0])
                inc = int(parts[1]) if len(parts) > 1 else 0
                self.increment = inc * 100
                self.default_time = (m * 60) * 100
                self.reset_timer()
            except ValueError:
                messagebox.showerror("Error", "Format: Minutes [Increment]")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessTimerApp(root)
    root.mainloop()
    