
import random
import time
from collections import defaultdict
from heapq import heappush, heappop

# Enregistrer le temps de début
start_time = time.time()

class HyperGraph:
    def __init__(self, edges):
        self.nodes = set()
        self.edges = edges
        for edge in edges:
            self.nodes |= set(edge)
            
    def min_transversals(self):
        min_transversals = set()
        covered_edges = set()

        # Tant qu'il reste des arêtes non couvertes
        while len(covered_edges) != len(self.edges):
            # Sélectionner le sommet qui couvre le plus grand nombre d'arêtes non couvertes
            best_node = max(self.nodes, key=lambda node: len([edge for idx, edge in enumerate(self.edges) if idx not in covered_edges and node in edge]))
            # Ajouter ce sommet au transversal minimal
            transversal = {best_node}
            # Mettre à jour l'ensemble des arêtes couvertes
            for idx, edge in enumerate(self.edges):
                if best_node in edge:
                    covered_edges.add(idx)
            # Ajouter le transversal minimal trouvé à l'ensemble des transversaux minimaux
            min_transversals.add(frozenset(transversal))

        return min_transversals
    
      
    def reduce_hyperedges_improved(self, reduction_percentage=20):
        if reduction_percentage >= 100:
            raise ValueError("Reduction percentage must be less than 100.")
        
        reduced_edges = []
        for edge in self.edges:
            num_elements_to_keep = max(1, int(len(edge) * (reduction_percentage / 100)))
            reduced_edge = random.sample(list(edge), num_elements_to_keep)
            reduced_edges.append(set(reduced_edge))

        return HyperGraph(reduced_edges)

    def print_hyperedges(self):
        for edge in self.edges:
            print(edge)


# Le reste de votre code reste inchangé

# Convertir hypergraph_data en une liste de sets
file_path = r"C:\Users\aghil\OneDrive\Bureau\Master-2-SID-\S1\TER\Hypergraphes_Datasets_Expes\kosarak.dat"
edges = []
with open(file_path, 'r') as file:
    for line in file:
        edge = set(map(int, line.strip().split()))
        edges.append(edge)

# Créer l'instance HyperGraph et trouver les transversaux minimaux
hypergraph = HyperGraph(edges)

reduced_hypergraph = hypergraph.reduce_hyperedges_improved(reduction_percentage=5)
print("Le graphe reduit",reduced_hypergraph.edges)
# reduced_hypergraph.print_hyperedges()

reduced_results = reduced_hypergraph.min_transversals()

resultats_sans_frozenset = [tuple(transversal) for transversal in reduced_results]
print("Transversals minimaux :\n", resultats_sans_frozenset)

end_time = time.time()
elapsed_time = end_time - start_time  # Temps écoulé en secondes
elapsed_time_minutes = elapsed_time * 1000  # Convertir en millisecondes

print(f"Temps d'exécution du programme : {elapsed_time_minutes:.2f} ms")