import random

# ca c'est ok, en a la methode prend en compte les hyper-arréte avec un % de n.
# ca doit marché
def select_hyperedge(H_i, n):
    """Sélectionne n% des éléments de l'hyper-arrête H_i."""
    size = max(1, int(len(H_i) * n / 100))
    return random.sample(H_i, size)

# def reduce_hypergraph(HG, n):
#     """Réduit l'hypergraphe HG en sélectionnant n% de chaque hyper-arrête."""
#     Hr = {}
#     for H_id, vertices in HG.items():
#         Hr[H_id] = select_hyperedge(vertices, n)
#     return Hr
# Avec cette fonction en essai de construire le graphe réduite avec les hyper-arrete a n %
def reduce_hypergraph(HG, n):
    Hr = []
    for vertices in HG:
        Hr.append(select_hyperedge(vertices,n))
    return Hr

def calculate_TM(Hr):
    """Calculer la matrice de traversée TM à partir du graphe réduit Hr.
    Cette fonction est un placeholder et doit être implémentée selon les spécifications du problème."""
    # Placeholder pour le calcul de TM
    return random.random()  # Exemple de sortie fictive

def global_algorithm(HG, n, m, k):
    min_TM = float('inf')
    for i in range(k):
        Hr = reduce_hypergraph(HG, n)
        TM_i = calculate_TM(Hr)
        if TM_i < min_TM:
            min_TM = TM_i
    return min_TM

# Exemple d'hypergraphe
HG = {
    'H1': {1, 2, 3, 4},
    'H2': {2, 3, 5},
    'H3': {4, 6}
}

# Paramètres
n, m, k = 50, 10, 5  # n% pour la sélection, m pour le tirage, k graphes réduits

min_TM_stoch = global_algorithm(HG, n, m, k)
print("Min TM stochastique:", min_TM_stoch)