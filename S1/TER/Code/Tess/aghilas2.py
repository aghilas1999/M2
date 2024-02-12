import random
import time
from collections import defaultdict
from heapq import heappush, heappop

# Enregistrer le temps de début
start_time = time.time()

all_minimal_transversals = []

def min_transversals(hypergraphe):
    min_transversals = set()
    cut_queue = [(frozenset(hypergraphe), frozenset())]

    while cut_queue:
        current_cut, current_transversal = heappop(cut_queue)

        if not current_cut:
            min_transversals.add(current_transversal)
            continue

        node = next(iter(current_cut))  # Choisir un nœud arbitraire dans current_cut
        new_transversal_with_node = frozenset(current_transversal | {node})
        new_cut_with_node = frozenset(current_cut - {node} - set(hypergraphe[node]))
        heappush(cut_queue, (new_cut_with_node, new_transversal_with_node))

        for neighbor in hypergraphe[node]:
            if neighbor in current_cut:
                new_transversal_without_node = frozenset(current_transversal | {neighbor})
                new_cut_without_node = frozenset(current_cut - {node} - {neighbor} - set(hypergraphe[neighbor]))
                heappush(cut_queue, (new_cut_without_node, new_transversal_without_node))

    return min_transversals

    
      
      
def réduire_hypergraphe(chemin_fichier, seuil):
    # Lire le fichier .hyp et stocker les hyper-arêtes dans une liste
    
    with open(chemin_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    hypergraphe = [set(map(int, ligne.split())) for ligne in lignes]

    # Créer une liste vide pour stocker les arêtes du graphe réduit
    graphe_reduit = []

    # Parcourir chaque hyper-arête dans l'hypergraphe
    for hyperarête in hypergraphe:
        # Calculer le nombre d'éléments à tirer en fonction du seuil
        nombre_elements_a_tirer = int(len(hyperarête) * (seuil / 100))

        # Sélectionner aléatoirement un sous-ensemble de l'hyper-arête
        hyperarête_réduite = sélectionner(hyperarête, nombre_elements_a_tirer)

        # Convertir l'ensemble en liste et ajouter ses éléments à la liste des arêtes du graphe réduit
        graphe_reduit += list(hyperarête_réduite)

    return graphe_reduit

def sélectionner(ensemble, nombre_éléments):
    """Sélectionne aléatoirement un sous-ensemble d'une taille spécifique."""
    if len(ensemble) <= nombre_éléments:
        return list(ensemble)
    else:
        choix = random.sample(list(ensemble), nombre_éléments)
        return choix


# Le reste de votre code reste inchangé

# Convertir hypergraph_data en une liste de sets
file_path = r"C:\Users\aghil\OneDrive\Bureau\Master-2-SID-\S1\TER\Hypergraphes_Datasets_Expes\accidents\ac_200k.dat"
test = réduire_hypergraphe(file_path, 10)

#print(test)
test2 = min_transversals(test)
print(test2)
# reduced_results = reduced_hypergraph.min_transversals()

# resultats_sans_frozenset = [tuple(transversal) for transversal in reduced_results]

# print("Transversals minimaux :\n", resultats_sans_frozenset)

# end_time = time.time()
# elapsed_time = end_time - start_time  # Temps écoulé en secondes
# elapsed_time_minutes = elapsed_time * 1000  # Convertir en millisecondes

# print(f"Temps d'exécution du programme : {elapsed_time_minutes:.2f} ms")
