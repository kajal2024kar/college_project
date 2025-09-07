import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox

# File paths
bolly = "The_project/Bollywood.xlsx"
histry = "The_project/HISTORY.xlsx"
tech = "The_project/Technology.xlsx"
science = "The_project/SCIENCE.xlsx"
sport = "The_project/SPORTS.xlsx"

# Load Excel
def load_excel(path: str):
    if not os.path.exists(path):
        messagebox.showerror("Error", f"Quiz file not found: {path}")
        return None
    try:
        df = pd.read_excel(path)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading quiz file: {e}")
        return None

    required_cols = {"Question", "Option A", "Option B", "Option C", "Option D", "Answer"}
    if not required_cols.issubset(df.columns):
        messagebox.showerror("Error", f"Excel file must contain columns: {required_cols}")
        return None

    df = df.dropna(subset=list(required_cols))
    if df.empty:
        messagebox.showerror("Error", "No valid questions found in the quiz file.")
        return None
    return df

# Main GUI class
class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Quiz App")
        master.geometry("600x400")

        # Category selection
        tk.Label(master, text="Choose a Quiz Category:", font=("Arial", 14)).pack(pady=10)

        categories = [("Bollywood", bolly),
                      ("History", histry),
                      ("Technology", tech),
                      ("Science", science),
                      ("Sports", sport)]
        
        self.df = None
        self.current_question = None
        self.var = tk.StringVar()
        self.var.set(None)

        for text, path in categories:
            tk.Radiobutton(master, text=text, variable=self.var, value=path, font=("Arial", 12)).pack(anchor="w")

        tk.Button(master, text="Start Quiz", command=self.start_quiz).pack(pady=10)

        self.question_label = tk.Label(master, text="", wraplength=550, font=("Arial", 12))
        self.question_label.pack(pady=20)

        self.options = {}
        for option in ["A", "B", "C", "D"]:
            self.options[option] = tk.Button(master, text="", width=30, command=lambda o=option: self.check_answer(o))
            self.options[option].pack(pady=5)

        tk.Button(master, text="Quit", command=master.quit).pack(side="bottom", pady=10)

    def start_quiz(self):
        path = self.var.get()
        if not path:
            messagebox.showwarning("Warning", "Please select a category!")
            return
        self.df = load_excel(path)
        if self.df is not None:
            self.next_question()

    def next_question(self):
        if self.df is None or self.df.empty:
            messagebox.showinfo("Info", "No questions available.")
            return
        self.current_question = self.df.sample().iloc[0]
        self.question_label.config(text=f"❓ {self.current_question['Question']}")
        for option in ["A", "B", "C", "D"]:
            self.options[option].config(text=f"{option}. {self.current_question[f'Option {option}']}")

    def check_answer(self, selected_option):
        correct = str(self.current_question["Answer"]).strip().upper()
        if selected_option == correct:
            messagebox.showinfo("Result", "✅ Correct!")
        else:
            correct_text = self.current_question.get(f"Option {correct}", "Unknown")
            messagebox.showinfo("Result", f"❌ Wrong! Correct answer: {correct}. {correct_text}")
        self.next_question()

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
