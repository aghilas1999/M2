import random

def select_hyperedge(H_i, n):
    """Sélectionne aléatoirement n% des éléments de l'hyper-arrête H_i."""
    H_i_list = list(H_i)  # Convertit l'ensemble en liste
    size = max(1, int(len(H_i_list) * n / 100))
    return set(random.sample(H_i_list, size))  # Convertit le résultat en ensemble, si nécessaire


def reduce_hypergraph(HG, n):
    """Réduit l'hypergraphe HG en sélectionnant n% de chaque hyper-arrête."""
    return [select_hyperedge(H_i, n) for H_i in HG]

def calculate_min_transversals(Hr):
    """Calculer les transversaux minimaux d'un hypergraphe réduit Hr.
       Placeholder pour un algorithme de calcul des transversaux minimaux."""
    # Implémentation simplifiée / fictive
    return random.randint(1, 10)  # Renvoie une valeur fictive comme mesure TM

def update_TM(HG, n, k):
    """Calcule et met à jour la mesure TM pour k réductions de l'hypergraphe HG."""
    TM_OLD = 0
    min_TM = float('inf')  # Initialise min_TM à l'infini
    
    for _ in range(k):
        Hr = reduce_hypergraph(HG, n)
        TM_i = calculate_min_transversals(Hr)
        TM_OLD += TM_i  # Mise à jour de TM en additionnant TM_i à TM_OLD
        
        if TM_i < min_TM:
            min_TM = TM_i  # Mise à jour de min_TM si TM_i est plus petit
    
    return TM_OLD, min_TM

# Exemple d'utilisation
HG = [{1, 2, 3}, {2, 3, 4}, {4, 5}]  # Exemple d'hypergraphe
n = 10  # Pourcentage pour la réduction
k = 10  # Nombre de réductions à calculer

TM_OLD, min_TM = update_TM(HG, n, k)
print("TM_OLD:", TM_OLD, "min_TM:", min_TM)
