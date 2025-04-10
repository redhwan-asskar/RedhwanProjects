import tkinter as tk
from tkinter import messagebox

class Exam:
    def __init__(self, name, e_id):
        self.name = name
        self.e_id = e_id
        self.questions = {}  # Store questions and options
        self.answers = []  # Store correct answers
        self.correct_count = 0
        self.incorrect_count = 0
        self.time_left = 180  # One minute
        self.user_answers = {}  # Store user answers
        self.selected_button = None  # Track selected button
        self.result_shown = False  # Track if result is shown
        self.timer_task = None

    def load_questions(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            counter = 1
            question = None
            options = []
            for line in f:
                line = line.strip()
                if line.startswith("---"):  # End of question
                    self.questions[counter] = (question, options)
                    question = None
                    options = []
                    counter += 1
                elif line.startswith('ans:'):
                    self.answers.append(line.split(":")[1].strip())
                else:
                    if question is None:
                        question = line
                    else:
                        options.append(line)

    def start_exam(self):
        self.window = tk.Tk()
        self.window.title(f"{self.name} - Exam")
        self.window.geometry("800x600")
        self.window.config(bg="#f0f0f0")

        self.current_question = 1

        self.header_label = tk.Label(self.window, text="Python Exam", font=("Arial", 20, "bold"), bg="#f0f0f0")
        self.header_label.pack(pady=10)

        self.timer_label = tk.Label(self.window, text="Time Left: 01:00", font=("Arial", 14), fg="#ff0000", bg="#f0f0f0")
        self.timer_label.pack(pady=10)

        self.progress_label = tk.Label(self.window, text="Question 1/10", font=("Arial", 12), bg="#f0f0f0")
        self.progress_label.pack(pady=5)

        self.question_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.question_frame.pack(pady=20)
        self.question_label = tk.Label(self.question_frame, text="", font=("Arial", 16), wraplength=600, bg="#f0f0f0")
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(3):
            btn = tk.Button(self.question_frame, text="", font=("Arial", 14), width=35, height=2,
                            command=lambda i=i: self.select_option(i), bg="#4CAF50", fg="white")
            btn.pack(pady=10)
            self.option_buttons.append(btn)

        self.navigation_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.navigation_frame.pack(pady=10)

        self.nav_buttons = []
        for i in range(1, len(self.questions) + 1):
            btn = tk.Button(self.navigation_frame, text=f"Q{i}", font=("Arial", 12),
                            command=lambda i=i: self.display_question(i), width=4, bg="#ddd")
            btn.pack(side=tk.LEFT, padx=5)
            self.nav_buttons.append(btn)

        self.button_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        self.submit_button = tk.Button(self.button_frame, text="Submit", font=("Arial", 14), command=self.submit_answer,
                                       bg="#2196F3", fg="white", width=15, state="disabled")
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.finish_button = tk.Button(self.button_frame, text="Finish Exam", font=("Arial", 14), command=self.finish_exam,
                                       bg="#FF0000", fg="white", width=15)
        self.finish_button.pack(side=tk.LEFT, padx=10)

        self.update_timer()
        self.display_question(self.current_question)
        self.window.mainloop()

    def update_timer(self):
     minutes, seconds = divmod(self.time_left, 60)
     self.timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
     if self.time_left > 0:
        self.time_left -= 1
        self.timer_task = self.window.after(1000, self.update_timer)
     else:
        messagebox.showwarning("Time Finished", "Time is up! The exam is now closing.")
        self.window.destroy()  

    def display_question(self, question_number):
        self.current_question = question_number
        question, options = self.questions[self.current_question]
        self.question_label.config(text=question)
        self.progress_label.config(text=f"Question {self.current_question}/{len(self.questions)}")

        for i, option in enumerate(options):
            self.option_buttons[i].config(text=option, bg="#4CAF50")

            if self.user_answers.get(self.current_question) == option:
                self.option_buttons[i].config(bg="#FFD700")

        self.submit_button.config(state="disabled")

    def select_option(self, selected_option):
        if self.selected_button:
            self.selected_button.config(bg="#4CAF50")
        
        self.selected_button = self.option_buttons[selected_option]
        self.selected_button.config(bg="#FFD700")
        
        question, options = self.questions[self.current_question]
        self.user_answers[self.current_question] = options[selected_option]
        self.submit_button.config(state="normal")

    def submit_answer(self):
        if self.user_answers.get(self.current_question, "") == self.answers[self.current_question - 1]:
            self.correct_count += 1
        else:
            self.incorrect_count += 1
        
        self.nav_buttons[self.current_question - 1].config(bg="#90EE90")  

        if self.current_question < len(self.questions):
            self.current_question += 1
            self.display_question(self.current_question)
        else:
            self.finish_exam()

    def finish_exam(self):
        unanswered = [q for q in self.questions if q not in self.user_answers]
        if unanswered:
            messagebox.showwarning("Incomplete Exam", f"You have unanswered questions: {', '.join(map(str, unanswered))}. Please answer them before finishing.")
            for q in unanswered:
                self.nav_buttons[q - 1].config(bg="#FF6347")  
            return

        if self.result_shown:
            return

        if self.timer_task:
            self.window.after_cancel(self.timer_task)

        total_questions = len(self.questions)
        percentage = (self.correct_count / total_questions) * 100
        result_message = f"Your results:\n\nCorrect Answers: {self.correct_count}\nIncorrect Answers: {self.incorrect_count}\nPercentage: {percentage:.2f}%\n"
        messagebox.showinfo("Exam Results", result_message)
        self.result_shown = True


def start_exam(level):
    e1 = Exam(f'Python {level} Level', 123)
    e1.load_questions("Exam.txt")
    e1.start_exam()

root = tk.Tk()
root.title("Python Exam Levels")
root.geometry("400x400")
root.config(bg="#f0f0f0")

tk.Button(root, text="Start Exam", font=("Arial", 16), command=lambda: start_exam('Beginner'), bg="#4CAF50", fg="white").pack(pady=20)
root.mainloop()
 