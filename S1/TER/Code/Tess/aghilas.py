import random
import time
from collections import defaultdict
from heapq import heappush, heappop

# Enregistrer le temps de début
start_time = time.time()

class HyperGraph:
    def __init__(self, edges):
        self.nodes = set()
        self.edges = edges  # Ajouter l'attribut edges pour stocker les hyper-arêtes originales
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

            node = next(iter(current_cut))
            new_transversal_with_node = frozenset(current_transversal | {node})
            new_cut_with_node = frozenset(current_cut - {node} - set(self.adjacency_lists[node]))
            heappush(cut_queue, (new_cut_with_node, new_transversal_with_node))

            for neighbor in self.adjacency_lists[node]:
                if neighbor in current_cut:
                    new_transversal_without_node = frozenset(current_transversal | {neighbor})
                    new_cut_without_node = frozenset(current_cut - {node} - {neighbor} - set(self.adjacency_lists[neighbor]))
                    heappush(cut_queue, (new_cut_without_node, new_transversal_without_node))
        
        
        return min_transversals
      
      
      
    def reduce_hyperedges(self, reduction_percentage=5):
        reduced_edges = set()
        for edge in self.edges:
            num_elements_to_keep = max(1, len(edge) * reduction_percentage // 100)
            edge_set = set(edge)  # Convertir l'ensemble en un autre ensemble (copie)
            edge_list = list(edge_set)  # Convertir edge_set en une liste
            reduced_edge_list = random.sample(edge_list, num_elements_to_keep)
            reduced_edge = set(reduced_edge_list)
            reduced_edges.add(frozenset(reduced_edge))

        return HyperGraph(list(reduced_edges))

    def print_hyperedges(self):
        for edge in self.edges:
            print(edge)


# Le reste de votre code reste inchangé

# Convertir hypergraph_data en une liste de sets
file_path = r"C:\Users\aghil\OneDrive\Bureau\Master-2-SID-\S1\TER\Hypergraphes_Datasets_Expes\accidents\ac_200k.dat"
edges = []
with open(file_path, 'r') as file:
    for line in file:
        edge = set(map(int, line.strip().split()))
        edges.append(edge)

# Créer l'instance HyperGraph et trouver les transversaux minimaux
hypergraph = HyperGraph(edges)
reduced_hypergraph = hypergraph.reduce_hyperedges(reduction_percentage=5)
reduced_hypergraph.print_hyperedges()

reduced_results = reduced_hypergraph.min_transversals()

resultats_sans_frozenset = [tuple(transversal) for transversal in reduced_results]

print("Transversals minimaux :\n", resultats_sans_frozenset)

end_time = time.time()
elapsed_time = end_time - start_time  # Temps écoulé en secondes
elapsed_time_minutes = elapsed_time * 1000  # Convertir en millisecondes

print(f"Temps d'exécution du programme : {elapsed_time_minutes:.2f} ms")
