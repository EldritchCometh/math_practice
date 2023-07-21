import random
from operator import add, sub, mul


class Problem:

    def __init__(self, l_operand, r_operand, operator, symbol):
        self.operands = (l_operand, r_operand)
        self.operator = operator
        self.symbol = symbol

    @property
    def question(self):
        return f'{self.operands[0]} {self.symbol} {self.operands[1]} ='

    @property
    def answer(self):
        return self.operator(self.operands[0], self.operands[1])


class MathProblems:

    def __init__(self):
        self.probs = []
        self.probs.extend(self.make_probs(2, 99, add, '+')[:13])
        self.probs.extend(self.make_probs(2, 99, sub, '-')[:13])
        self.probs.extend(self.make_probs(3, 9, mul, '*')[:13])
        self.num_starting_probs = len(self.probs)
        random.shuffle(self.probs)

    @staticmethod
    def make_probs(range_min, range_max, operator, symbol):
        to_be_added = []
        for i in range(range_min, range_max + 1):
            for j in range(range_min, range_max + 1):
                prob = Problem(i, j, operator, symbol)
                if 2 <= prob.answer <= 99:
                    to_be_added.append(prob)
        random.shuffle(to_be_added)
        return to_be_added

    def get_prob(self):
        return random.choice(self.probs)

    def rem_prob(self, problem):
        self.probs.remove(problem)

    @property
    def remaining(self):
        return len(self.probs)
