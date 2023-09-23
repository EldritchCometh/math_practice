
import random
from itertools import product
from operator import add, sub, mul


class Problem:

    def __init__(self, operands, operator, rand_order, mixed_unknown):
        symbol = {add: '+', sub: '-', mul: '*'}[operator]
        result = operator(operands[0], operands[1])
        self.question = [operands[0], symbol, operands[1], '=', result]
        self.unknown_idx = 4
        self.unknown = self.question[4]
        if rand_order: self.rand_reorder()
        if mixed_unknown: self.mix_unknown()
        self.question[self.unknown_idx] = None

    def rand_reorder(self):
        if random.choice([True, False]):
            return
        self.question = [self.question[4], '='] + self.question[:3]
        self.unknown_idx = 0

    def mix_unknown(self):
        self.unknown_idx = random.choice([0, 2, 4])
        self.unknown = self.question[self.unknown_idx]


def gen_probs(operand_range, mixed_unknown, rand_order, answer_range=(0, 99)):
    all_probs = []
    operations = [add, sub]
    if operand_range[1] >= 10:
        operations.append(mul)
    for opr in operations:
        probs = []
        while len(probs) < 3:
            probs.extend(
                Problem((i, j), opr, rand_order, mixed_unknown)
                for i in range(operand_range[0], operand_range[1] + 1)
                for j in range(operand_range[0], operand_range[1] + 1)
                if answer_range[0] <= opr(i, j) <= answer_range[1])
        random.shuffle(probs)
        all_probs.extend(probs[:3])
    random.shuffle(all_probs)
    return all_probs


def get_level(level):
    levels = (
        [((0, i), j, k) for i, j, k in product(range(3), range(2), range(2))] +
        [((0, i), j, j) for i, j in product(range(3, 6), range(2))] +
        [((0, i), 1, 1) for i in range(7, 12, 2)] +
        [((j, i), 1, 1, (j, 99)) for j, i in enumerate(range(13, 20, 2))] +
        [((3, i), 1, 1, (3, 99)) for i in range(24, 100, 5)])
    return gen_probs(*levels[level])


