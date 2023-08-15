import random
import tkinter as tk
from tkinter import ttk
from operator import add, sub, mul

"lets test adding a comment and a new comment"


class Problem:

    def __init__(self, fst_operand, snd_operand, operator):
        self.fst_operand = fst_operand
        self.snd_operand = snd_operand
        self.operator = operator
        self.result = operator(fst_operand, snd_operand)
        self.var_idx = random.randint(0, 2)
        self.answer = [fst_operand, snd_operand, self.result][self.var_idx]
        self.question_text = self.get_question_text()

    def get_question_text(self):
        symbol = {add: '+', sub: '-', mul: '*'}[self.operator]
        comps = [self.fst_operand, self.snd_operand, self.result]
        comps[self.var_idx] = '_'
        if random.randint(0, 1):
            return [comps[0], symbol, comps[1], '=', comps[2]]
        else:
            return [comps[2], '=', comps[0], symbol, comps[1]]


class MathProblems:

    def __init__(self, settings):
        self.probs = []
        self.make_probs(*settings.add_opr_range, add, settings.num_of_adds)
        self.make_probs(*settings.sub_opr_range, sub, settings.num_of_subs)
        self.make_probs(*settings.mul_opr_range, mul, settings.num_of_muls)
        random.shuffle(self.probs)
        self.probs = self.probs[:settings.num_of_probs]
        self.starting = len(self.probs)

    def make_probs(self, range_min, range_max, operator, num_of_probs):
        probs = []
        for i in range(range_min, range_max + 1):
            for j in range(range_min, range_max + 1):
                prob = Problem(i, j, operator)
                if 0 <= prob.result <= 99:
                    probs.append(prob)
        random.shuffle(probs)
        probs = probs[:num_of_probs]
        self.probs.extend(probs)

    def get_prob(self):
        return random.choice(self.probs)

    def remove(self, problem):
        self.probs.remove(problem)

    @property
    def remaining(self):
        return len(self.probs)


class FlashCardsGame:

    def __init__(self, user_settings):
        self.root = tk.Tk()
        self.configure_window((1200, 325))
        self.controller = ProblemController(user_settings)
        self.controller.on_finished = lambda: self.root.destroy()
        self.root.mainloop()

    def configure_window(self, window_dims):
        self.root.title("Arithmetic Flashcards")
        x = (self.root.winfo_screenwidth() - window_dims[0]) // 2
        y = (self.root.winfo_screenheight() - window_dims[1]) // 2
        self.root.geometry(f"{window_dims[0]}x{window_dims[1]}+{x}+{y}")


class ProblemController:

    def __init__(self, user_settings):
        self.user_settings = user_settings
        self.failed = False
        self.problems = MathProblems(user_settings)
        self.problem = None
        self.current_frame = None
        self.load_new_problem_frame()

    def load_new_problem_frame(self):
        self.failed = False
        self.problem = self.problems.get_prob()
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ProblemFrame(
            self.problem.question_text,
            self.problems.starting,
            self.problems.remaining,
            self.user_settings.timer)
        self.current_frame.on_entered = self.on_entered
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.entry.bind("<Return>", self.on_entered)
        self.current_frame.entry.bind("<KP_Enter>", self.on_entered)

    def on_entered(self, _):
        try:
            answer = int(self.current_frame.entry.get())
        except ValueError:
            return
        if answer == self.problem.answer:
            if not self.failed and not self.current_frame.out_of_time:
                self.problems.remove(self.problem)
            if self.problems.remaining > 0:
                self.load_new_problem_frame()
            else:
                self.on_finished()
        else:
            self.failed = True
            self.current_frame.timer_setting = None
            self.current_frame.entry.delete(0, 'end')


class ProblemFrame(tk.Frame):

    def __init__(self, text, starting, remaining, timer_setting):
        super().__init__()
        self.timer_setting = timer_setting
        self.out_of_time = False
        self.font_size = None
        self.timer_frame, self.timer_bar = self.make_timer_bar()
        self.progress_frame = self.make_progress_bar(starting, remaining)
        self.question_components, self.entry = self.make_question(text)
        self.update_timer(self.timer_bar)
        self.bind("<Configure>", self.resize_elements)

    def make_question(self, text):
        question_frame = tk.Frame(self)
        question_frame.pack(side='top', fill='y', expand=True, padx=6, pady=6)
        question_components = []
        for t in text:
            comp_frame = tk.Frame(question_frame)
            comp_frame.pack(side='left', anchor='center')
            if t == '_':
                entry = tk.Entry(comp_frame, width=2)
                entry.pack(padx=3, pady=3)
                question_components.append(entry)
                entry.focus_set()
            else:
                label = tk.Label(comp_frame, text=t)
                question_components.append(label)
                label.pack(padx=3, pady=3)
        return question_components, entry

    def make_progress_bar(self, num_starting_probs, num_remaining_probs):
        progress_frame = ttk.Frame(self, height=30)
        progress_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        progress_bar = ttk.Progressbar(
            progress_frame,
            maximum=num_starting_probs,
            value=(num_starting_probs - num_remaining_probs))
        progress_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        return progress_frame

    def make_timer_bar(self):
        timer_frame = ttk.Frame(self, height=30)
        timer_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        timer_duration = self.timer_setting or 1
        timer_bar = ttk.Progressbar(
            timer_frame,
            maximum=timer_duration * 10,
            value=timer_duration * 10)
        timer_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        return timer_frame, timer_bar

    def update_timer(self, timer_bar):
        if not timer_bar.winfo_exists():
            return
        if not self.timer_setting:
            return
        if timer_bar['value'] <= 0:
            self.out_of_time = True
            return
        timer_bar['value'] -= 1
        self.after(100, lambda: self.update_timer(timer_bar))

    def resize_elements(self, _):
        prog_bars_heights = max(25, self.winfo_height() * 0.05)
        q_frame_width = self.winfo_width() - 12
        q_frame_height = self.winfo_height() - (prog_bars_heights * 2) - 18
        self.font_size = int(min(q_frame_width * 0.153, q_frame_height * 0.7))
        for comp in self.question_components:
            comp.config(font=("Arial", self.font_size))
        self.progress_frame.config(height=prog_bars_heights)
        self.timer_frame.config(height=prog_bars_heights)


class Olive:

    timer = None
    num_of_probs = None
    num_of_adds = 30
    num_of_subs = 30
    num_of_muls = 40
    add_opr_range = (0, 9)
    sub_opr_range = (0, 9)
    mul_opr_range = (1, 12)


class Clem:

    timer = None
    num_of_probs = 50
    num_of_adds = None
    num_of_subs = None
    num_of_muls = 0
    add_opr_range = (0, 6)
    sub_opr_range = (0, 6)
    mul_opr_range = (0, 0)


if __name__ == "__main__":

    game = FlashCardsGame(Clem)
