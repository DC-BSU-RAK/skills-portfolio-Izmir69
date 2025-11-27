import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

RES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
os.makedirs(RES_DIR, exist_ok=True)

FILE_PATH = os.path.join(RES_DIR, "studentMarks.txt")


# ------------------------------
# Student Class
# ------------------------------
class Student:
    def __init__(self, code, name, cw1, cw2, cw3, exam):
        self.code = int(code)
        self.name = name
        self.cw1 = int(cw1)
        self.cw2 = int(cw2)
        self.cw3 = int(cw3)
        self.exam = int(exam)

    @property
    def coursework_total(self):
        return self.cw1 + self.cw2 + self.cw3  # out of 60

    @property
    def overall(self):
        return self.coursework_total + self.exam  # out of 160

    @property
    def percentage(self):
        return (self.overall / 160) * 100

    @property
    def grade(self):
        p = self.percentage
        if p >= 70: return "A"
        if p >= 60: return "B"
        if p >= 50: return "C"
        if p >= 40: return "D"
        return "F"

    def to_line(self):
        return f"{self.code},{self.name},{self.cw1},{self.cw2},{self.cw3},{self.exam}"


# ------------------------------
# Main App
# ------------------------------
class StudentManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager")
        self.geometry("1000x550")
        self.students = []
        self.load_students()

        self.build_ui()
        self.refresh_tree()

    # --------------------------
    # Load / Save
    # --------------------------
    def load_students(self):
        self.students.clear()
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                lines = [x.strip() for x in f.readlines()]
        except:
            messagebox.showerror("Error", "studentMarks.txt not found.")
            return

        if not lines:
            return

        # first line = number of students (ignore)
        for line in lines[1:]:
            parts = line.split(",")
            if len(parts) != 6:
                continue
            code, name, c1, c2, c3, exam = parts
            self.students.append(Student(code, name, c1, c2, c3, exam))

    def save_students(self):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(str(len(self.students)) + "\n")
            for s in self.students:
                f.write(s.to_line() + "\n")

    # --------------------------
    # UI
    # --------------------------
    def build_ui(self):
        frame_buttons = ttk.Frame(self, padding=8)
        frame_buttons.pack(fill="x")

        ttk.Button(frame_buttons, text="View All", command=self.refresh_tree).pack(side="left", padx=4)
        ttk.Button(frame_buttons, text="View Individual", command=self.view_individual).pack(side="left", padx=4)
        ttk.Button(frame_buttons, text="Highest", command=self.show_highest).pack(side="left", padx=4)
        ttk.Button(frame_buttons, text="Lowest", command=self.show_lowest).pack(side="left", padx=4)
        ttk.Button(frame_buttons, text="Sort", command=self.sort_menu).pack(side="left", padx=4)
        ttk.Button(frame_buttons, text="Add", command=self.add_student).pack(side="left", padx=4)
        ttk.Button(frame_buttons, text="Update", command=self.update_student).pack(side="left", padx=4)
        ttk.Button(frame_buttons, text="Delete", command=self.delete_student).pack(side="left", padx=4)

        columns = ("code", "name", "cw", "exam", "overall", "percent", "grade")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("code", text="Code")
        self.tree.heading("name", text="Name")
        self.tree.heading("cw", text="Coursework (60)")
        self.tree.heading("exam", text="Exam (100)")
        self.tree.heading("overall", text="Overall (160)")
        self.tree.heading("percent", text="Percentage")
        self.tree.heading("grade", text="Grade")

        self.tree.column("name", width=220)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.summary = ttk.Label(self, text="", font=("TkDefaultFont", 11))
        self.summary.pack(anchor="w", padx=12)

    # --------------------------
    # Actions
    # --------------------------
    def refresh_tree(self, custom=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = custom if custom else self.students

        for s in data:
            self.tree.insert("", "end", values=(
                s.code, s.name, s.coursework_total, s.exam,
                s.overall, f"{s.percentage:.2f}%", s.grade
            ))

        # Summary
        count = len(data)
        avg = sum(s.percentage for s in data) / count if count else 0
        self.summary.config(text=f"Total students: {count}    Average: {avg:.2f}%")

    def view_individual(self):
        q = simpledialog.askstring("Search", "Enter student code or name:")
        if not q: return
        q = q.lower()

        results = [s for s in self.students if q in s.name.lower() or q == str(s.code)]

        if not results:
            messagebox.showinfo("Not found", "No matching student.")
            return

        s = results[0]  # first match

        msg = (f"Name: {s.name}\n"
               f"Code: {s.code}\n"
               f"Coursework: {s.cw1}, {s.cw2}, {s.cw3}\n"
               f"Coursework Total: {s.coursework_total}/60\n"
               f"Exam: {s.exam}/100\n"
               f"Overall: {s.overall}/160\n"
               f"Percentage: {s.percentage:.2f}%\n"
               f"Grade: {s.grade}")

        messagebox.showinfo("Student Record", msg)

    def show_highest(self):
        if not self.students: return
        s = max(self.students, key=lambda x: x.overall)
        self.view_student_popup(s)

    def show_lowest(self):
        if not self.students: return
        s = min(self.students, key=lambda x: x.overall)
        self.view_student_popup(s)

    def view_student_popup(self, s):
        msg = (f"Name: {s.name}\n"
               f"Code: {s.code}\n"
               f"Coursework Total: {s.coursework_total}\n"
               f"Exam: {s.exam}\n"
               f"Overall: {s.overall}\n"
               f"Percentage: {s.percentage:.2f}%\n"
               f"Grade: {s.grade}")
        messagebox.showinfo("Student", msg)

    # --------------------------
    # Sorting
    # --------------------------
    def sort_menu(self):
        choice = simpledialog.askstring("Sort", "Sort by:\n1 = Name\n2 = Overall\n3 = Code\n(Add '-' for descending, e.g. -1)")
        if not choice: return

        desc = choice.startswith("-")
        key = choice.lstrip("-")

        if key == "1":
            sorted_list = sorted(self.students, key=lambda x: x.name.lower(), reverse=desc)
        elif key == "2":
            sorted_list = sorted(self.students, key=lambda x: x.overall, reverse=desc)
        elif key == "3":
            sorted_list = sorted(self.students, key=lambda x: x.code, reverse=desc)
        else:
            messagebox.showerror("Error", "Invalid option.")
            return

        self.refresh_tree(sorted_list)

    # --------------------------
    # Add / Update / Delete
    # --------------------------
    def add_student(self):
        dialog = StudentEditor(self)
        self.wait_window(dialog)

        if dialog.student:
            # check duplicate code
            if any(s.code == dialog.student.code for s in self.students):
                messagebox.showerror("Error", "Student code already exists.")
                return

            self.students.append(dialog.student)
            self.save_students()
            self.refresh_tree()

    def update_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Error", "Select a student first.")
            return

        code = int(self.tree.item(sel[0], "values")[0])
        s = next(x for x in self.students if x.code == code)

        dialog = StudentEditor(self, s)
        self.wait_window(dialog)

        if dialog.student:
            idx = self.students.index(s)
            self.students[idx] = dialog.student
            self.save_students()
            self.refresh_tree()

    def delete_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Error", "Select a student first.")
            return

        code = int(self.tree.item(sel[0], "values")[0])
        s = next(x for x in self.students if x.code == code)

        if messagebox.askyesno("Confirm", f"Delete {s.name}?"):
            self.students.remove(s)
            self.save_students()
            self.refresh_tree()


# ------------------------------
# Student Editing Popup
# ------------------------------
class StudentEditor(tk.Toplevel):
    def __init__(self, master, student=None):
        super().__init__(master)
        self.title("Edit Student" if student else "Add Student")
        self.geometry("380x320")
        self.student = None

        ttk.Label(self, text="Student Code:").pack()
        self.ent_code = ttk.Entry(self)
        self.ent_code.pack()

        ttk.Label(self, text="Name:").pack()
        self.ent_name = ttk.Entry(self)
        self.ent_name.pack()

        ttk.Label(self, text="Coursework 1:").pack()
        self.ent_c1 = ttk.Entry(self)
        self.ent_c1.pack()

        ttk.Label(self, text="Coursework 2:").pack()
        self.ent_c2 = ttk.Entry(self)
        self.ent_c2.pack()

        ttk.Label(self, text="Coursework 3:").pack()
        self.ent_c3 = ttk.Entry(self)
        self.ent_c3.pack()

        ttk.Label(self, text="Exam:").pack()
        self.ent_exam = ttk.Entry(self)
        self.ent_exam.pack()

        ttk.Button(self, text="Save", command=self.save).pack(pady=10)

        if student:
            self.ent_code.insert(0, student.code)
            self.ent_name.insert(0, student.name)
            self.ent_c1.insert(0, student.cw1)
            self.ent_c2.insert(0, student.cw2)
            self.ent_c3.insert(0, student.cw3)
            self.ent_exam.insert(0, student.exam)

    def save(self):
        try:
            code = int(self.ent_code.get())
            name = self.ent_name.get().strip()
            c1 = int(self.ent_c1.get())
            c2 = int(self.ent_c2.get())
            c3 = int(self.ent_c3.get())
            exam = int(self.ent_exam.get())

            # Validation
            if not (1000 <= code <= 9999):
                raise ValueError("Code must be 1000–9999")
            if not name:
                raise ValueError("Name cannot be empty")
            for c in (c1, c2, c3):
                if not (0 <= c <= 20):
                    raise ValueError("Coursework must be 0–20")
            if not (0 <= exam <= 100):
                raise ValueError("Exam must be 0–100")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.student = Student(code, name, c1, c2, c3, exam)
        self.destroy()


# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    app = StudentManager()
    app.mainloop()
