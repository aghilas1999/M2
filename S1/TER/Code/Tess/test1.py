# Supposons que HG_lines représente les lignes de votre hypergraphe
HG_lines = [
    "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
    "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
    "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 29 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
    "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 21 22 23 24 25 26 28 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
    "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
    "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
    "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63"
]

# # Convertir chaque ligne en un ensemble d'entiers, représentant une hyper-arête
# HG = [set(map(int, line.split())) for line in HG_lines]
# print(HG)

# def is_transversal(transversal, HG):
#     """Vérifie si un ensemble est une transversale pour l'hypergraphe."""
#     return all(bool(transversal.intersection(edge)) for edge in HG)

# def find_minimal_transversal(HG, current_set=None, start=0):
#     """Trouve une transversale minimale de manière heuristique."""
#     if current_set is None:
#         current_set = set()
    
#     if is_transversal(current_set, HG):
#         return current_set
    
#     for vertex in range(start, max(max(HG))+1):
#         new_set = current_set.union({vertex})
#         if is_transversal(new_set, HG):
#             return find_minimal_transversal(HG, new_set, vertex+1)
    
#     return None  # Retourne None si aucune transversale n'est trouvée

# # Exemple d'utilisation
# minimal_transversal = find_minimal_transversal(HG)
# print("Une transversale minimale trouvée :", minimal_transversal)

def powerset(s):
    s = list(s)  # Convertit l'ensemble en liste
    x = len(s)
    masks = (1 << i for i in range(x))
    for i in range(1 << x):
        yield {s[j] for j, mask in enumerate(masks) if i & mask}

def is_transversal(transversal, hypergraph):
    return all(bool(transversal.intersection(edge)) for edge in hypergraph)

def find_minimal_transversals(hypergraph):
    vertices = set.union(*hypergraph)
    minimal_transversals = set()

    for subset in powerset(vertices):
        if is_transversal(subset, hypergraph):
            if not any(subset > other for other in minimal_transversals):
                minimal_transversals = {other for other in minimal_transversals if not other > subset}
                minimal_transversals.add(frozenset(subset))
                
    return [set(mt) for mt in minimal_transversals]

# Votre code pour définir HG ici, en utilisant HG_lines ou autre

# Exemple d'utilisation

HG = [set(map(int, line.split())) for line in HG_lines]
minimal_transversals = find_minimal_transversals(HG)
print("Transversales minimales:", minimal_transversals)
