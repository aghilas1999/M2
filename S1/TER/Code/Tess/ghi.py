import random

# Générer un hypergraphe aléatoire avec un intervalle de 1 à 2952
n_vertices = 30  # Nombre de sommets dans l'hypergraphe
n_hyperedges = 100  # Nombre d'hyper-arêtes

HG = [set(random.sample(range(1, 2953), random.randint(1, 10))) for _ in range(n_hyperedges)]

# Exemple d'utilisation
n = 10  # Pourcentage pour la réduction
k = 10  # Nombre de réductions à calculer

TM_OLD, min_TM = update_TM(HG, n, k)
print("TM_OLD:", TM_OLD, "min_TM:", min_TM)
