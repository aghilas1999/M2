import itertools
import random
from typing import List, Set

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def minimal_transversal(hypergraph):
    """Returns a minimal transversal of an input hypergraph."""
    def is_transversal(candidate):
        nonlocal hypergraph
        return all((any(edge & candidate for edge in hg)) for hg in hypergraph)
    
    candidates = set(x for x in powerset(range(len(hypergraph))))
    transversal = next(c for c in candidates if is_transversal(c))
    return sorted(list(transversal))

def calculate_Hr(HG, r):
    """Calculate Hr based on input hypergraph HG."""
    # Hr = [[e for e in edge if r in e and isinstance(e, set)] for edge in HG]
    Hr = [[e for e in edge if isinstance(e, set) and r in e] for edge in HG]

    return Hr

def compute_TM(Hr):
    """Compute Minimum Transversals (TM) given Hr."""
    TMs = []
    for hr in Hr:
        transversal = minimal_transversal(hr)
        TMs.append(transversal)
    return TMs

def aggregate_TM(TMs):
    """Aggregate minimum transversals into STM."""
    tm_size = len(TMs[0])
    stm = [set() for _ in range(tm_size)]
    for tm in TMs:
        for idx, val in enumerate(tm):
            stm[idx].add(val)
    return stm

def select_smallest_TM(TMs):
    """Select smallest TMs out of all computed ones."""
    min_size = float('inf')
    selected_TMs = []

    for tm in TMs:
        size = len(tm)
        if size <= min_size:
            if size < min_size:
                selected_TMs = []
                min_size = size
            selected_TMs.append(tm)

    return selected_TMs

def sample_and_filter(TMs, num_samples):
    """Sample and filter TMs by comparing them against others."""
    filtered_TMs = []
    for _ in range(num_samples):
        sampled_TM = random.choice(TMs)
        if sampled_TM not in filtered_TMs:
            if not any(is_subset(sampled_TM, other_tm) for other_tm in filtered_TMs):
                filtered_TMs.append(sampled_TM)

    return filtered_TMs

def is_subset(smaller, larger):
    """Check if smaller subset is contained within larger."""
    return all(elem in larger for elem in smaller)
import random

def generate_random_set():
    return set([random.randint(1, 100), random.randint(1, 100)])



def main():
    HG = [generate_random_set() for _ in range(100)]

    k = 10
    m = 10

    TMs = []
    for r in range(1, k+1):
        Hr = calculate_Hr(HG, r)
        TMs.extend(compute_TM(Hr))

    min_TM = select_smallest_TM(TMs)

    if m > 0:
        min_TM = sample_and_filter(min_TM, m)

    print("Matroïde Transversal Stochastique (MTS):")
    print(min_TM)

if __name__ == "__main__":
    main()