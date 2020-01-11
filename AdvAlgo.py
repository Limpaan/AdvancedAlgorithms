from itertools import chain, combinations
import math


def get_cheapest(subset):
    if len(subset) == 1:
        return 0
    minimum = math.inf
    for j in range(len(subset)):
        element = subset[j]
        tmp = list(subset)
        tmp.remove(element)
        subset_minus_e = tuple(tmp)
        minimum = min(minimum, scores[subset_minus_e][0] + scores[subset_minus_e][1])
    return minimum

def count_open_sets(sets, subset):
    count = 0
    for j in range(len(sets)):
        if not set(sets[j]) <= set(subset):
            for k in range(len(subset)):
                if subset[k] in sets[j]:
                    count += 1
                    break

    return count

sets = ((1, 2, 3), (3, 4), (2, 5), (1, 4), (3, 5))
universe = [1, 2, 3, 4, 5]

powerset = list(chain.from_iterable(combinations(universe, r) for r in range(1, len(universe) + 1)))
scores = {}

for i in range(len(powerset)):
    scores[powerset[i]] = [0,0]
    scores[powerset[i]][0] = get_cheapest(powerset[i])
    scores[powerset[i]][1] = count_open_sets(sets, powerset[i])

for k, v in scores.items():
    print("{:<15} {:<7}".format(str(k), str(v)))

