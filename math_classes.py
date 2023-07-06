import random
from operator import add, sub


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


class Problems:

    def __init__(self, min, max, operator, symbol):
        self.probs = []
        self.inc_probs(min, max, operator, symbol)

    def inc_probs(self, min, max, operator, symbol):
        for i in range(min, max + 1):
            for j in range(min, max + 1):
                prob = Problem(i, j, operator, symbol)
                if prob.answer > 0:
                    self.probs.append(prob)


class AdditionProblems(Problems):

    def __init__(self, min, max):
        super().__init__(min, max, add, '+')


class SubtractionProblems(Problems):

    def __init__(self, min, max):
        super().__init__(min, max, sub, '-')


class MathProblems:

    def __init__(self):
        self.probs = []
        self.add_probs(AdditionProblems(1, 10), SubtractionProblems(1, 10))
        random.shuffle(self.probs)
        self.probs = self.probs[:20]

    def get_prob(self):
        return random.choice(self.probs)

    def rem_prob(self, problem):
        self.probs.remove(problem)

    def add_probs(self, *problem_groups):
        for problem_group in problem_groups:
            self.probs.extend(problem_group.probs)

    @property
    def remaining(self):
        return len(self.probs)

