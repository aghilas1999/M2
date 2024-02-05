import random
from itertools import combinations
import time  # Importer le module time

# Enregistrer le temps de début
start_time = time.time()

# Fonction pour lire l'hypergraphe depuis un fichier
def read_hypergraph_from_file(file_path):
    hypergraph = []
    with open(file_path, 'r') as file:
        for line in file:
            hyperedge = set(map(int, line.strip().split()))
            hypergraph.append(hyperedge)
    return hypergraph

# Fonction pour sélectionner aléatoirement n% des éléments de l'hyper-arête
def select_hyperedge(H_i, n):
    H_i_list = list(H_i)
    size = max(1, int(len(H_i_list) * n / 100))
    return set(random.sample(H_i_list, size))

# Fonction pour réduire l'hypergraphe en sélectionnant n% de chaque hyper-arête
def reduce_hypergraph(HG, n):
    random.seed(42)  # Pour la reproductibilité
    return [select_hyperedge(H_i, n) for H_i in HG]

def minimal_transversals(HG, current_set=None, index=0):
    if current_set is None:
        current_set = set()

    if index >= len(HG):
        yield current_set
        return

    hyperedge = HG[index]
    for vertex in hyperedge:
        new_set = current_set.union({vertex})
        if all(new_set.intersection(h) for h in HG[:index + 1]):
            # Si new_set est une transversale jusqu'à présent, continuez récursivement
            yield from minimal_transversals(HG, new_set, index + 1)
        else:
            # Si l'ajout de ce sommet ne forme pas une transversale, passez au suivant
            continue

    # Vérifier si le current_set actuel est déjà une transversale pour tous les hyper-edges jusqu'à cet index
    if all(current_set.intersection(h) for h in HG[:index + 1]):
        yield current_set


# Fonction pour calculer et mettre à jour la mesure TM pour k réductions de l'hypergraphe
def update_TM(HG, n, k):
    TM_OLD = 0
    min_TM = float('inf')
    for _ in range(k):
        Hr = reduce_hypergraph(HG, n)
        minimal_transversals = minimal_transversals(Hr)
        TM_i = len(minimal_transversals)
        TM_OLD += TM_i
        if TM_i < min_TM:
            min_TM = TM_i
    return TM_OLD / k, min_TM  # Retourne la moyenne de TM_OLD

# # Chemin vers votre fichier
# file_path = 'ac_200k.dat'

# # Lire l'hypergraphe depuis le fichier
# hypergraph = read_hypergraph_from_file(file_path)

# # Paramètres
# n = 10  # Pourcentage pour la réduction
# k = 10  # Nombre de réductions à calculer

# # Calculer TM_OLD et min_TM
# TM_OLD, min_TM = update_TM(hypergraph, n, k)

# # Afficher les résultats
# print("TM_OLD (moyenne):", TM_OLD, "min_TM:", min_TM)

# # Remplacer cette section par le reste de votre code...
# # Lire l'hypergraphe, effectuer les calculs, etc.

# # Calculer et afficher le temps d'exécution à la fin du programme
# end_time = time.time()
# elapsed_time = end_time - start_time  # Temps écoulé en secondes
# elapsed_time_minutes = elapsed_time / 60  # Convertir en minutes

# Lire l'hypergraphe depuis un fichier
hypergraph = read_hypergraph_from_file("ac_200k.dat")

# Appeler la fonction reduce_hypergraph avec un pourcentage n
n = 10  # Par exemple, sélectionnez 50% de chaque hyper-arête
reduced_hypergraph = reduce_hypergraph(hypergraph, n)

# # Affichage de l'hypergraphe réduit
# for hyperedge in reduced_hypergraph:
#     print(hyperedge)

# Appeler la fonction find_minimal_transversals
minimal_transversals = minimal_transversals(hypergraph)

# Affichage des ensembles transversaux minimaux
for minimal_transversal in minimal_transversals:
    print(minimal_transversal)

    
end_time = time.time()
elapsed_time = end_time - start_time  # Temps écoulé en secondes
elapsed_time_minutes = elapsed_time / 60  # Convertir en minutes

print(f"Temps d'exécution du programme : {elapsed_time_minutes:.2f} minutes")

