import tkinter as tk
from tkinter import ttk, messagebox
import os, random

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
os.makedirs(RESOURCES_DIR, exist_ok=True)
JOKES_FILE = os.path.join(RESOURCES_DIR, "randomJokes.txt")

# create small sample if missing
if not os.path.isfile(JOKES_FILE):
    sample = [
        "Why did the chicken cross the road?To get to the other side.",
        "What happens if you boil a clown?You get a laughing stock.",
        "Why don't scientists trust atoms?Because they make up everything."
    ]
    with open(JOKES_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(sample))

class JokeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alexa - Tell Me a Joke")
        self.geometry("640x300")
        self.resizable(False, False)

        self.jokes = []
        self.current = None
        self._load_jokes()
        self._build_ui()

    def _load_jokes(self):
        try:
            with open(JOKES_FILE, "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f if ln.strip()]
        except FileNotFoundError:
            messagebox.showerror("Missing file", f"Jokes file not found: {JOKES_FILE}")
            lines = []
        out = []
        for line in lines:
            if "?" in line:
                idx = line.index("?")
                setup = line[:idx+1].strip()
                punch = line[idx+1:].strip()
                out.append((setup, punch))
            else:
                out.append((line, ""))
        self.jokes = out

    def _build_ui(self):
        ttk.Label(self, text="Alexa — Tell Me A Joke", font=("TkDefaultFont", 16, "bold")).pack(pady=(12,6))
        self.lbl_setup = ttk.Label(self, text="Click the button to hear a joke", wraplength=600, font=("TkDefaultFont", 12))
        self.lbl_setup.pack(pady=(6,6))
        self.lbl_punchline = ttk.Label(self, text="", wraplength=600, font=("TkDefaultFont", 11, "italic"))
        self.lbl_punchline.pack(pady=(6,6))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)
        self.btn_tell = ttk.Button(btn_frame, text="Alexa tell me a Joke", command=self.tell_joke)
        self.btn_tell.pack(side="left", padx=6)
        self.btn_punch = ttk.Button(btn_frame, text="Show Punchline", command=self.show_punchline, state="disabled")
        self.btn_punch.pack(side="left", padx=6)
        self.btn_next = ttk.Button(btn_frame, text="Next Joke", command=self.next_joke, state="disabled")
        self.btn_next.pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Quit", command=self.destroy).pack(side="left", padx=6)

        self.lbl_count = ttk.Label(self, text=f"Jokes available: {len(self.jokes)}")
        self.lbl_count.pack(pady=(6,0))

    def tell_joke(self):
        if not self.jokes:
            self.lbl_setup["text"] = "No jokes available."
            return
        self.current = random.choice(self.jokes)
        self.lbl_setup["text"] = self.current[0]
        self.lbl_punchline["text"] = ""
        self.btn_punch["state"] = "normal"
        self.btn_next["state"] = "disabled"

    def show_punchline(self):
        if not self.current:
            return
        self.lbl_punchline["text"] = self.current[1] if self.current[1] else "(No punchline provided)"
        self.btn_next["state"] = "normal"
        self.btn_punch["state"] = "disabled"

    def next_joke(self):
        self.current = None
        self.lbl_setup["text"] = "Click the button to hear another joke"
        self.lbl_punchline["text"] = ""
        self.btn_punch["state"] = "disabled"
        self.btn_next["state"] = "disabled"

if __name__ == "__main__":
    app = JokeApp()
    app.mainloop()