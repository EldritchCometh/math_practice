# Fix prog bar display
# Choice of Data Structure
# Elimate MathProblems class
# Think about the cascading user_settings
# Fix use of config manager in classes
# Event-Driven Design: To decouple FlashCardsGame and FlashCard
# Is making cards ahead of time actually the best solution?
# Look into using a signal to update prog bar for decoupling
# Set starting and value on prog bar inside display_new_card
# display_new_card -> display_next_card
# noticed a hang on entering the final correct answer
# convert running out of time into a signal that just flags failed
# possible bug: asked the same question twice and gave the answer second time
# possible bug: required me to press enter twice after getting wrong first time

import random
import tkinter as tk
from tkinter import ttk
from operator import add, sub, mul


class Problem:

    def __init__(self, fst_operand, snd_operand, operator):
        self.fst_operand = fst_operand
        self.snd_operand = snd_operand
        self.operator = operator
        self.result = operator(fst_operand, snd_operand)
        self.var_idx = random.randint(0, 2)
        self.answer = [fst_operand, snd_operand, self.result][self.var_idx]

    @property
    def question(self):
        symbol = {add: '+', sub: '-', mul: '*'}[self.operator]
        comps = [self.fst_operand, self.snd_operand, self.result]
        comps[self.var_idx] = '_'
        if random.randint(0, 1):
            return [comps[0], symbol, comps[1], '=', comps[2]]
        else:
            return [comps[2], '=', comps[0], symbol, comps[1]]


class FlashCardsApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.configure_window((1200, 325))
        self.main_frame = FlashCardsGame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.on_finished = lambda: self.destroy()
        self.mainloop()

    def configure_window(self, window_dims):
        self.title("Arithmetic Flashcards")
        x = (self.winfo_screenwidth() - window_dims[0]) // 2
        y = (self.winfo_screenheight() - window_dims[1]) // 2
        self.geometry(f"{window_dims[0]}x{window_dims[1]}+{x}+{y}")


class FlashCardsGame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.failed = False
        self.starting = None
        self.remaining = None
        self.current_card = None
        self.deck = self.get_new_deck()
        self.display_new_flashcard()

    @staticmethod
    def make_probs(range_min, range_max, opr):
        probs = []
        for i in range(range_min, range_max + 1):
            for j in range(range_min, range_max + 1):
                prob = Problem(i, j, opr)
                if 0 <= prob.result <= 99:
                    probs.append(prob)
        random.shuffle(probs)
        return probs

    def get_new_deck(self):
        probs = (
            self.make_probs(*User.add_range, add)[:User.num_of_adds] +
            self.make_probs(*User.sub_range, sub)[:User.num_of_subs] +
            self.make_probs(*User.mul_range, mul)[:User.num_of_muls])
        random.shuffle(probs)
        probs = probs[:User.num_of_probs]
        self.starting = len(probs)
        self.remaining = self.starting
        return [FlashCard(self, prob, self.starting) for prob in probs]

    def display_new_flashcard(self):
        if self.current_card:
            self.current_card.pack_forget()
        if self.deck:
            self.current_card = random.choice(self.deck)
            self.current_card.prog_bar['maximum'] = self.starting
            self.current_card.prog_bar['value'] = self.remaining
            self.current_card.pack(fill="both", expand=True)
            self.current_card.on_entered = self.on_entered
            self.current_card.entry.bind("<Return>", self.on_entered)
            self.current_card.entry.bind("<KP_Enter>", self.on_entered)
            self.current_card.entry.focus_set()
            if User.timer:
                self.current_card.start_countdown()
        else:
            self.on_finished()

    def on_entered(self, _):
        try:
            answer = int(self.current_card.entry.get())
        except ValueError:
            return
        if answer == self.current_card.answer:
            if not self.failed and not self.current_card.out_of_time:
                print("should be removing here")
                self.deck.remove(self.current_card)
                self.remaining -= 1
            self.failed = False
            if self.remaining > 0:
                self.display_new_flashcard()
            else:
                self.on_finished()
        else:
            self.failed = True
            self.current_card.timer_setting = None
            self.current_card.entry.delete(0, 'end')


class  FlashCard(tk.Frame):

    def __init__(self, parent, prob, num_of_probs):
        super().__init__(parent)
        self.answer = prob.answer
        self.out_of_time = False
        self.font_size = None
        self.timer_setting = User().timer
        self.timer_frame, self.timer_bar = self.make_timer_bar()
        self.prog_frame, self.prog_bar = self.make_prog_bar(num_of_probs)
        self.question_comps, self.entry = self.make_question(prob.question)
        self.bind("<Configure>", self.resize_elements)

    def make_question(self, text):
        question_frame = tk.Frame(self)
        question_frame.pack(side='top', fill='y', expand=True, padx=6, pady=6)
        question_comps = []
        for t in text:
            comp_frame = tk.Frame(question_frame)
            comp_frame.pack(side='left', anchor='center')
            if t == '_':
                entry = tk.Entry(comp_frame, width=2)
                entry.pack(padx=3, pady=3)
                question_comps.append(entry)
            else:
                label = tk.Label(comp_frame, text=t)
                question_comps.append(label)
                label.pack(padx=3, pady=3)
        return question_comps, entry

    def make_prog_bar(self, num_of_probs):
        prog_frame = ttk.Frame(self, height=30)
        prog_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        prog_bar = ttk.Progressbar(prog_frame, maximum=1, value=1)
        prog_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        return prog_frame, prog_bar

    def make_timer_bar(self):
        timer_frame = ttk.Frame(self, height=30)
        timer_frame.pack(side='bottom', fill='x', padx=5, pady=(0, 4))
        duration = self.timer_setting or 1
        timer_bar = ttk.Progressbar(
            timer_frame, maximum=duration * 10, value=duration * 10)
        timer_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        return timer_frame, timer_bar

    def start_countdown(self):
        if not self.timer_bar.winfo_exists():
            return
        if self.timer_bar['value'] <= 0:
            self.out_of_time = True
            return
        self.timer_bar['value'] -= 1
        self.after(100, lambda: self.start_countdown())

    def resize_elements(self, _):
        prog_bars_heights = max(25, self.winfo_height() * 0.05)
        q_frame_width = self.winfo_width() - 12
        q_frame_height = self.winfo_height() - (prog_bars_heights * 2) - 18
        self.font_size = int(min(q_frame_width * 0.153, q_frame_height * 0.7))
        for comp in self.question_comps:
            comp.config(font=("Arial", self.font_size))
        self.prog_frame.config(height=prog_bars_heights)
        self.timer_frame.config(height=prog_bars_heights)


class Olive:

    timer = None
    num_of_probs = None
    num_of_adds = 30
    num_of_subs = 30
    num_of_muls = 40
    add_opr_range = (2, 19)
    sub_opr_range = (2, 19)
    mul_opr_range = (1, 12)


class Clem:

    timer = None
    num_of_probs = 3
    num_of_adds = None
    num_of_subs = None
    num_of_muls = 0
    add_range = (0, 9)
    sub_range = (0, 9)
    mul_range = (0, 0)


if __name__ == "__main__":

    User = Clem
    FlashCardsApp()


'''
class User:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(User, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def set_clem(self):
        self.timer = None
        self.num_of_probs = 40
        self.num_of_adds = None
        self.num_of_subs = None
        self.num_of_muls = 0
        self.add_opr_range = (0, 9)
        self.sub_opr_range = (0, 9)
        self.mul_opr_range = (0, 0)

    def set_olive(self):
        self.timer = None
        self.num_of_probs = None
        self.num_of_adds = 30
        self.num_of_subs = 30
        self.num_of_muls = 40
        self.add_opr_range = (2, 19)
        self.sub_opr_range = (2, 19)
        self.mul_opr_range = (1, 12)
'''
