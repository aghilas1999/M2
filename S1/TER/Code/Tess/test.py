# import random

# def select_hyperedge(H_i, n):
#     """Sélectionne aléatoirement n% des éléments de l'hyper-arrête H_i."""
#     H_i_list = list(H_i)  # Convertit l'ensemble en liste
#     size = max(1, int(len(H_i_list) * n / 100))
#     return set(random.sample(H_i_list, size))  # Convertit le résultat en ensemble, si nécessaire


# def reduce_hypergraph(HG, n):
#     """Réduit l'hypergraphe HG en sélectionnant n% de chaque hyper-arrête."""
#     return [select_hyperedge(H_i, n) for H_i in HG]

# def calculate_min_transversals(Hr):
#     """Calculer les transversaux minimaux d'un hypergraphe réduit Hr.
#        Placeholder pour un algorithme de calcul des transversaux minimaux."""
#     # Implémentation simplifiée / fictive
#     return random.randint(1, 3)  # Renvoie une valeur fictive comme mesure TM

# def update_TM(HG, n, k):
#     """Calcule et met à jour la mesure TM pour k réductions de l'hypergraphe HG."""
#     TM_OLD = 0
#     min_TM = float('inf')  # Initialise min_TM à l'infini
    
#     for _ in range(k):
#         Hr = reduce_hypergraph(HG, n)
#         TM_i = calculate_min_transversals(Hr)
#         TM_OLD += TM_i  # Mise à jour de TM en additionnant TM_i à TM_OLD
        
#         if TM_i < min_TM:
#             min_TM = TM_i  # Mise à jour de min_TM si TM_i est plus petit
    
#     return TM_OLD, min_TM

# # Exemple d'utilisation
# HG = [{9, 10, 13}, {4, 5, 6}]  # Exemple d'hypergraphe
# n = 10  # Pourcentage pour la réduction
# k = 10  # Nombre de réductions à calculer

# TM_OLD, min_TM = update_TM(HG, n, k)
# print("TM_OLD:", TM_OLD, "min_TM:", min_TM)
'''from itertools import combinations

def find_minimal_transversals(HG):
    minimal_transversals = []
    vertices = set.union(*HG)

    def is_transversal(candidate):
        for hyperedge in HG:
            if not any(vertex in candidate for vertex in hyperedge):
                return False
        return True

    for r in range(1, len(vertices) + 1):
        for candidate in combinations(vertices, r):
            if is_transversal(candidate):
                minimal_transversals.append(set(candidate))

    return minimal_transversals

# Exemple d'utilisation
HG = [{1, 2, 3}, {2, 4}, {3, 5}]
minimal_transversals = find_minimal_transversals(HG)
print(minimal_transversals)
'''

import random
from itertools import combinations

def select_hyperedge(H_i, n):
    """Sélectionne aléatoirement n% des éléments de l'hyper-arrête H_i."""
    H_i_list = list(H_i)  # Convertit l'ensemble en liste
    size = max(1, int(len(H_i_list) * n / 100))
    return set(random.sample(H_i_list, size))  # Convertit le résultat en ensemble, si nécessaire

def reduce_hypergraph(HG, n):
    """Réduit l'hypergraphe HG en sélectionnant n% de chaque hyper-arrête."""
    return [select_hyperedge(H_i, n) for H_i in HG]

def find_minimal_transversals(HG):
    minimal_transversals = []
    vertices = set.union(*HG)

    def is_transversal(candidate):
        for hyperedge in HG:
            if not any(vertex in candidate for vertex in hyperedge):
                return False
        return True

    for r in range(1, len(vertices) + 1):
        for candidate in combinations(vertices, r):
            if is_transversal(candidate):
                minimal_transversals.append(set(candidate))

    return minimal_transversals

def update_TM(HG, n, k):
    """Calcule et met à jour la mesure TM pour k réductions de l'hypergraphe HG."""
    TM_OLD = 0
    min_TM = float('inf')  # Initialise min_TM à l'infini
    
    for _ in range(k):
        Hr = reduce_hypergraph(HG, n)
        minimal_transversals = find_minimal_transversals(Hr)
        TM_i = len(minimal_transversals)
        TM_OLD += TM_i  # Mise à jour de TM en additionnant TM_i à TM_OLD
        
        if TM_i < min_TM:
            min_TM = TM_i  # Mise à jour de min_TM si TM_i est plus petit
    
    return TM_OLD, min_TM

import random

# Générer un hypergraphe aléatoire avec un intervalle de 1 à 2952
n_vertices = 5  # Nombre de sommets dans l'hypergraphe
n_hyperedges = 20  # Nombre d'hyper-arêtes

HG = [set(random.sample(range(1, 200), random.randint(2, 10))) for _ in range(n_hyperedges)]

# Exemple d'utilisation
n = 10  # Pourcentage pour la réduction
k = 100  # Nombre de réductions à calculer

TM_OLD, min_TM = update_TM(HG, n, k)
print("TM_OLD:", TM_OLD, "min_TM:", min_TM)