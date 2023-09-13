
# combine some of the levels so that the num of probs are more consistent

from operator import add, sub, mul
import random


def gen_probs(range_min, operators, range_max, mixing, num_of_probs=8):
    if isinstance(operators, int):
        operators = [operators]
    probs = []
    while len(probs) < num_of_probs:
        temp = []
        for operator in operators:
            encoded_opr = {0: add, 1: sub, 2: mul}[operator]
            for i in range(range_min, range_max + 1):
                for j in range(range_min, range_max + 1):
                    answer = encoded_opr(i, j)
                    if 0 <= answer <= 99:
                        temp.append((i, operator, j, answer, mixing))
        random.shuffle(temp)
        temp = temp[:num_of_probs-len(probs)]
        probs.extend(temp)
    random.shuffle(probs)
    return probs


def get_level(level):
    return [
        gen_probs(0, [0, 1], 0, 0, 4),  # up to 0 with mixed operator
        gen_probs(0,      0, 1, 0, 4),  # up to 1 with addition
        gen_probs(0,      1, 1, 0, 4),  # up to 1 with sutraction
        gen_probs(0, [0, 1], 1, 0, 4),  # up to 1 with mixed operator
        gen_probs(0,      0, 1, 1, 4),  # up to 1 with addition and reversed
        gen_probs(0,      1, 1, 1, 4),  # up to 1 with subtraction and reversed
        gen_probs(0, [0, 1], 1, 1, 4),  # up to 1 with mixed opearator and reversed
        gen_probs(0,      0, 2, 0, 6),  # up to 2 with addition
        gen_probs(0,      1, 2, 0, 6),  # up to 2 with subtraction
        gen_probs(0,      0, 1, 2, 6),  # introduce random blanks up to 1+1
        gen_probs(0,      1, 1, 2, 6),  # random blanks up to 1-1
        gen_probs(0,      0, 2, 2, 6),  # random blanks up to 2+2
        gen_probs(0,      1, 2, 2, 6),  # random blanks up to 2-2



    ][level]


for i in range(1):
    print(get_level(i))
