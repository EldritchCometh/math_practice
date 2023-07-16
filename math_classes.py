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
        self.add_probs(2, 9, add, '+')
        self.add_probs(2, 9, sub, '-')
        # self.add_probs(2, 9, mul, '*')
        self.num_starting_probs = len(self.probs)
        random.shuffle(self.probs)

    def add_probs(self, range_min, range_max, operator, symbol):
        for i in range(range_min, range_max + 1):
            for j in range(range_min, range_max + 1):
                prob = Problem(i, j, operator, symbol)
                if prob.answer > 1:
                    self.probs.append(prob)

    def get_prob(self):
        return random.choice(self.probs)

    def rem_prob(self, problem):
        self.probs.remove(problem)

    @property
    def remaining(self):
        return len(self.probs)
