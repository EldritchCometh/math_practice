import random
from operator import add, sub, mul


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
        '''
        if random.randint(0, 1):
            return [comps[0], symbol, comps[1], '=', comps[2]]
        else:
            return [comps[2], '=', comps[0], symbol, comps[1]]
        '''
        return [comps[2], '=', comps[0], symbol, comps[1]]

class MathProblems:

    def __init__(self, user):
        self.probs = []
        self.probs.extend(self.make_probs(0, 6, add)[:user.num_of_adds])
        self.probs.extend(self.make_probs(0, 6, sub)[:user.num_of_subs])
        self.probs.extend(self.make_probs(0, 6, mul)[:user.num_of_muls])
        random.shuffle(self.probs)
        self.probs = self.probs[:user.num_of_probs]
        self.num_starting_probs = len(self.probs)

    @staticmethod
    def make_probs(self, range_min, range_max, operator):
        probs = []
        for i in range(range_min, range_max + 1):
            for j in range(range_min, range_max + 1):
                prob = Problem(i, j, operator)
                if 0 <= prob.result <= 99:
                    probs.append(prob)
        random.shuffle(probs)
        return probs

    def get_prob(self):
        return random.choice(self.probs)

    def rem_prob(self, problem):
        self.probs.remove(problem)

    @property
    def remaining(self):
        return len(self.probs)
