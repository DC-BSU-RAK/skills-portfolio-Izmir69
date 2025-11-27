import tkinter as tk
from tkinter import ttk, messagebox
import random

class MathsQuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maths Quiz")
        self.geometry("520x380")
        self.resizable(False, False)

        # Quiz config/state
        self.difficulty = tk.StringVar(value="Easy")
        self.min_val = 0
        self.max_val = 9
        self.total_questions = 10
        self.current_index = 0
        self.current_answer = None
        self.attempts = 0
        self.score = 0
        self.timer_seconds = 20
        self.timer_id = None
        self.remaining = 0

        self._build_ui()
        self.show_menu()

    def _build_ui(self):
        pad = 8
        header = ttk.Label(self, text="Maths Quiz", font=("TkDefaultFont", 16, "bold"))
        header.pack(pady=(12, 6))

        # --- Menu frame ---
        self.menu_frame = ttk.Frame(self, padding=pad)
        ttk.Label(self.menu_frame, text="DIFFICULTY LEVEL", font=("TkDefaultFont", 12)).grid(row=0, column=0, columnspan=3, pady=(0,6))
        ttk.Radiobutton(self.menu_frame, text="Easy (1-digit)", variable=self.difficulty, value="Easy").grid(row=1,column=0,sticky="w")
        ttk.Radiobutton(self.menu_frame, text="Moderate (2-digit)", variable=self.difficulty, value="Moderate").grid(row=1,column=1,sticky="w")
        ttk.Radiobutton(self.menu_frame, text="Advanced (4-digit)", variable=self.difficulty, value="Advanced").grid(row=1,column=2,sticky="w")
        ttk.Button(self.menu_frame, text="Start Quiz", command=self.start_quiz).grid(row=2,column=0,columnspan=3,pady=(10,0))

        # --- Quiz frame ---
        self.quiz_frame = ttk.Frame(self, padding=pad)

        self.lbl_progress = ttk.Label(self.quiz_frame, text="Question 0/0", anchor="w")
        self.lbl_progress.pack(fill="x")
        self.progress = ttk.Progressbar(self.quiz_frame, orient="horizontal", length=460, mode="determinate")
        self.progress.pack(pady=(4,8))
        self.lbl_question = ttk.Label(self.quiz_frame, text="", font=("Courier", 18))
        self.lbl_question.pack(pady=(6,8))

        entry_frame = ttk.Frame(self.quiz_frame)
        entry_frame.pack()
        ttk.Label(entry_frame, text="Your Answer:").pack(side="left")
        self.entry_answer = ttk.Entry(entry_frame, width=12)
        self.entry_answer.pack(side="left", padx=(6,0))
        self.entry_answer.bind("<Return>", lambda e: self.submit_answer())

        btn_frame = ttk.Frame(self.quiz_frame)
        btn_frame.pack(pady=(8,0))
        self.btn_submit = ttk.Button(btn_frame, text="Submit", command=self.submit_answer)
        self.btn_submit.pack(side="left", padx=6)
        self.btn_giveup = ttk.Button(btn_frame, text="Give Up", command=self.give_up)
        self.btn_giveup.pack(side="left", padx=6)

        self.lbl_feedback = ttk.Label(self.quiz_frame, text="")
        self.lbl_feedback.pack(pady=(8,0))

        # Score frame
        self.score_frame = ttk.Frame(self, padding=pad)

    # ---- Menu / start ----
    def show_menu(self):
        self.score_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.menu_frame.pack(pady=12)

    def start_quiz(self):
        diff = self.difficulty.get()
        if diff == "Easy":
            self.min_val, self.max_val = 0, 9
            self.timer_seconds = 15
        elif diff == "Moderate":
            self.min_val, self.max_val = 10, 99
            self.timer_seconds = 20
        else:
            self.min_val, self.max_val = 1000, 9999
            self.timer_seconds = 30

        self.current_index = 0
        self.score = 0
        self.progress["maximum"] = self.total_questions
        self.menu_frame.pack_forget()
        self.quiz_frame.pack(fill="both", expand=True, pady=12)
        self.next_question()

    # ---- Random generation ----
    def randomInt(self):
        return random.randint(self.min_val, self.max_val)

    def decideOperation(self):
        return random.choice(["+", "-"])

    # ---- Quiz flow ----
    def next_question(self):
        # Cancel any timer
        self.cancel_timer()
        self.entry_answer.delete(0, "end")
        self.lbl_feedback["text"] = ""
        self.attempts = 0
        self.current_index += 1
        if self.current_index > self.total_questions:
            self.finish_quiz()
            return
        a = self.randomInt()
        b = self.randomInt()
        op = self.decideOperation()
        self.current_answer = eval(f"{a}{op}{b}")
        self.lbl_question["text"] = f"{a} {op} {b} ="
        self.lbl_progress["text"] = f"Question {self.current_index}/{self.total_questions}"
        self.progress["value"] = self.current_index - 1
        # start timer
        self.start_timer(self.timer_seconds)
        self.entry_answer.focus_set()

    def submit_answer(self):
        if self.timer_id is None and self.remaining <= 0:
            # safety: timer expired and next_question scheduled already
            return
        text = self.entry_answer.get().strip()
        if text == "":
            messagebox.showwarning("No answer", "Please enter an integer answer.")
            return
        try:
            val = int(text)
        except ValueError:
            messagebox.showerror("Invalid", "Please enter a valid integer.")
            return
        self.attempts += 1
        if self.is_correct(val):
            if self.attempts == 1:
                self.score += 10
                self.lbl_feedback["text"] = "Correct! +10"
            else:
                self.score += 5
                self.lbl_feedback["text"] = "Correct on 2nd try! +5"
            self.after(700, self.next_question)
        else:
            if self.attempts >= 2:
                self.lbl_feedback["text"] = f"Wrong again. Correct: {self.current_answer}"
                self.after(900, self.next_question)
            else:
                self.lbl_feedback["text"] = "Wrong. One more try."
                # shorten timer for second attempt
                self.cancel_timer()
                self.start_timer(max(3, self.timer_seconds // 2))

    def is_correct(self, user_val):
        return user_val == self.current_answer

    def give_up(self):
        self.cancel_timer()
        self.lbl_feedback["text"] = f"Answer: {self.current_answer}"
        self.after(800, self.next_question)

    def finish_quiz(self):
        self.cancel_timer()
        possible = self.total_questions * 10
        for w in self.score_frame.winfo_children():
            w.destroy()
        ttk.Label(self.score_frame, text="Quiz Complete", font=("TkDefaultFont", 14, "bold")).pack(pady=(8,4))
        ttk.Label(self.score_frame, text=f"Score: {self.score} / {possible}").pack()
        ttk.Label(self.score_frame, text=f"Grade: {self.rank_from_score(self.score, possible)}").pack(pady=(4,8))
        btn_frame = ttk.Frame(self.score_frame)
        btn_frame.pack(pady=(6,4))
        ttk.Button(btn_frame, text="Play Again", command=self.play_again).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Exit", command=self.destroy).pack(side="left", padx=6)
        self.quiz_frame.pack_forget()
        self.score_frame.pack(pady=12)

    def rank_from_score(self, score, possible):
        percent = (score / possible) * 100 if possible else 0
        if percent >= 90:
            return "A+"
        if percent >= 80:
            return "A"
        if percent >= 70:
            return "B"
        if percent >= 60:
            return "C"
        if percent >= 50:
            return "D"
        return "F"

    def play_again(self):
        self.score_frame.pack_forget()
        self.show_menu()

    # ---- Timer ----
    def start_timer(self, seconds):
        self.remaining = seconds
        self._tick()

    def _tick(self):
        self.lbl_progress["text"] = f"Question {self.current_index}/{self.total_questions} | Time: {self.remaining}s"
        if self.remaining <= 0:
            self.timer_id = None
            # treat as immediate fail -> proceed to next question (show answer)
            self.lbl_feedback["text"] = f"Time's up. Answer: {self.current_answer}"
            self.after(900, self.next_question)
            return
        self.remaining -= 1
        self.timer_id = self.after(1000, self._tick)

    def cancel_timer(self):
        if self.timer_id:
            try:
                self.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None

if __name__ == "__main__":
    app = MathsQuizApp()
    app.mainloop()