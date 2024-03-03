# test avec un hypergraphe d'entrée.
import time  # Importer le module time

from collections import defaultdict
from heapq import heappush, heappop


# Enregistrer le temps de début
start_time = time.time()

class HyperGraph:
    def __init__(self, edges):
        self.nodes = set()
        for edge in edges:
            self.nodes |= set(edge)
        self.adjacency_lists = defaultdict(list)
        for edge in edges:
            for node in edge:
                self.adjacency_lists[node].extend(edge - {node})

    def min_transversals(self):
        min_transversals = set()
        cut_queue = [(frozenset(self.nodes), frozenset())]

        while cut_queue:
            current_cut, current_transversal = heappop(cut_queue)

            if not current_cut:
                min_transversals.add(current_transversal)
                continue

            node = next(iter(current_cut))  # Choisissez un nœud arbitraire dans current_cut
            new_transversal_with_node = frozenset(current_transversal | {node})
            new_cut_with_node = frozenset(current_cut - {node} - set(self.adjacency_lists[node]))
            heappush(cut_queue, (new_cut_with_node, new_transversal_with_node))

            for neighbor in self.adjacency_lists[node]:
                if neighbor in current_cut:
                    new_transversal_without_node = frozenset(current_transversal | {neighbor})
                    new_cut_without_node = frozenset(current_cut - {node} - {neighbor} - set(self.adjacency_lists[neighbor]))
                    heappush(cut_queue, (new_cut_without_node, new_transversal_without_node))

        return min_transversals

# Convertir hypergraph_data en une liste de sets
file_path = r"C:\Users\aghil\OneDrive\Bureau\Master-2-SID-\S1\TER\Hypergraphes_Datasets_Expes\accidents\ac_200k.dat"  # Remplacez par le chemin de votre fichier
edges = []
with open(file_path, 'r') as file:
    for line in file:
        edge = set(map(int, line.strip().split()))
        edges.append(edge)
        

# Créer l'instance HyperGraph et trouver les transversaux minimaux
hypergraph = HyperGraph(edges)
resultats = hypergraph.min_transversals()

resultats_sans_frozenset = [tuple(transversal) for transversal in resultats]

print("Transversals minimaux :\n", resultats_sans_frozenset)

end_time = time.time()
elapsed_time = end_time - start_time  # Temps écoulé en secondes
elapsed_time_minutes = elapsed_time * 1000 # Convertir en minutes

print(f"Temps d'exécution du programme : {elapsed_time_minutes:.2f} ms")
