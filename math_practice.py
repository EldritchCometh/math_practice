import random
import tkinter as tk
from tkinter import ttk
from operator import add, sub, mul


class Olive:

    timer = None
    num_of_probs = 100
    num_of_adds = 30
    num_of_subs = 30
    num_of_muls = 40
    add_opr_range = (0, 6)
    sub_opr_range = (0, 6)
    mul_opr_range = (1, 6)


class Clem:

    timer = None
    num_of_probs = 10
    num_of_adds = 25
    num_of_subs = 25
    num_of_muls = 0
    add_opr_range = (0, 5)
    sub_opr_range = (0, 5)
    mul_opr_range = (0, 0)


class Problem:

    def __init__(self, fst_operand, snd_operand, operator):
        self.fst_operand = fst_operand
        self.snd_operand = snd_operand
        self.operator = operator
        self.result = operator(fst_operand, snd_operand)
        self.var_idx = random.randint(0, 2)
        self.variable = [fst_operand, snd_operand, self.result][self.var_idx]
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
        self.num_starting_probs = len(self.probs)
        print(self.num_starting_probs)

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

    def rem_prob(self, problem):
        self.probs.remove(problem)

    @property
    def remaining(self):
        return len(self.probs)


class FlashCardsGame:

    def __init__(self, settings):
        self.root = tk.Tk()
        self.configure_window((1200, 325))
        self.problems = MathProblems(settings)
        self.problem = self.problems.get_prob()
        self.current_frame = ProblemFrame(
            self.problem.question_text,
            self.problems.num_starting_probs,
            self.problems.remaining,
            settings)
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.bind(ProblemFrame.ANSWER_ENTERED_EVENT,
                                self.handle_answer_entered)

    def configure_window(self, window_dims):
        self.root.title("Arithmetic Flashcards")
        x = (self.root.winfo_screenwidth() - window_dims[0]) // 2
        y = (self.root.winfo_screenheight() - window_dims[1]) // 2
        self.root.geometry(f"{window_dims[0]}x{window_dims[1]}+{x}+{y}")

    @staticmethod
    def handle_answer_entered(event):
        print("handle_answer_entered successfully called")


class ProblemFrame(tk.Frame):

    ANSWER_ENTERED_EVENT = "<<AnswerEntered>>"

    def __init__(self, text, num_starting_probs, num_remaining_probs, settings):
        super().__init__()
        self.frozen = False
        self.q_comps = []
        self.font_size = None
        self.progress_frame = None
        self.timer_frame = None
        self.entry = None
        self.make_timer_bar(settings)
        self.make_progress_bar(num_starting_probs, num_remaining_probs)
        self.make_question(text)
        self.bind("<Configure>", self.resize_elements)

    def make_question(self, text):
        question_frame = tk.Frame(self)
        question_frame.pack(side='top', fill='y', expand=True, padx=6, pady=6)
        for t in text:
            comp_frame = tk.Frame(question_frame)
            comp_frame.pack(side='left', anchor='center')
            if t == '_':
                self.entry = tk.Entry(comp_frame, width=2)
                self.q_comps.append(self.entry)
                self.entry.pack(padx=3, pady=3)
                self.entry.focus_set()
                self.entry.bind("<Return>", self.on_return_pressed)
                self.entry.bind("<KP_Enter>", self.on_return_pressed)
            else:
                label = tk.Label(comp_frame, text=t)
                self.q_comps.append(label)
                label.pack(padx=3, pady=3)

    def on_return_pressed(self, event):
        try:
            answer = int(self.entry.get())
            print(
                f"Answer obtained: {answer}")  # Let's print the answer to debug
            self.event_generate(
                self.ANSWER_ENTERED_EVENT)  # No need to pass answer here
        except ValueError:
            return

    def make_progress_bar(self, num_starting_probs, num_remaining_probs):
        self.progress_frame = ttk.Frame(self, height=30)
        self.progress_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        progress_bar = ttk.Progressbar(
            self.progress_frame,
            maximum=num_starting_probs,
            value=(num_starting_probs - num_remaining_probs))
        progress_bar.place(relx=0, rely=0, relwidth=1, relheight=1)

    def make_timer_bar(self, settings):
        self.timer_frame = ttk.Frame(self, height=30)
        self.timer_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        timer_duration = settings.timer or 1
        timer_bar = ttk.Progressbar(
            self.timer_frame,
            maximum=timer_duration * 10,
            value=timer_duration * 10)
        timer_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        if settings.timer:
            self.update_timer_bar(timer_bar)

    def update_timer_bar(self, timer_bar):
        if not timer_bar.winfo_exists():
            return
        elif self.frozen:
            return
        else:
            timer_bar['value'] -= 1
        self.after(100, lambda: self.update_timer_bar(timer_bar))

    def resize_elements(self, _):
        prog_bars_heights = max(25, self.winfo_height() * 0.05)
        q_frame_width = self.winfo_width() - 12
        q_frame_height = self.winfo_height() - (prog_bars_heights * 2) - 18
        self.font_size = int(min(q_frame_width * 0.153, q_frame_height * 0.7))
        for comp in self.q_comps:
            comp.config(font=("Arial", self.font_size))
        self.progress_frame.config(height=prog_bars_heights)
        self.timer_frame.config(height=prog_bars_heights)


if __name__ == "__main__":

    settings = Clem()
    game = FlashCardsGame(settings)
    game.root.mainloop()
