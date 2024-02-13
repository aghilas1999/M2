import random
import time
from collections import defaultdict
from heapq import heappush, heappop

# Enregistrer le temps de début
start_time = time.time()
#Classe HyperGraph
class HyperGraph:
    
    #Le constructeur de la classe HyperGraphe
    def __init__(self, edges):
        # Variable pour stocker tout les sommetes de l'hyper graphe et qui sont unique
        self.nodes = set()
        # Stocker les arret de l'hyper graphe
        self.edges = edges
        # Parcourir toutes le graphe et ajouter les sommet trouver dans la variable self.node
        for edge in edges:
            self.nodes |= set(edge)
            
    def min_transversals(self):
        #Variable pour stocker les transversaux minimaux
        min_transversals = set()
        covered_edges = set()

        # Tant qu'il reste des arêtes non couvertes
        while len(covered_edges) != len(self.edges):
            # Sélectionner le sommet qui couvre le plus grand nombre d'arêtes non couvertes
            best_node = min(self.nodes, key=lambda node: len([edge for idx, edge in enumerate(self.edges) if idx not in covered_edges and node in edge]))
            # Ajouter ce sommet au transversal minimal
            transversal = {best_node}
            # Mettre à jour l'ensemble des arêtes couvertes
            for idx, edge in enumerate(self.edges):
                if best_node in edge:
                    covered_edges.add(idx)
            # Ajouter le transversal minimal trouvé à l'ensemble des transversaux minimaux
            min_transversals.add(frozenset(transversal))

        return min_transversals
    
    # Fonction qui permet de réduire l'hyper graphe
    def reduce_hyperedges_improved(self, reduction_percentage=10):
        # Condition si le seuil est égale a 100 alors c'est faut 
        if reduction_percentage >= 100:
            raise ValueError("Reduction percentage must be less than 100.")
        # variable pour stocké les arret reduit
        reduced_edges = []
        # boucle pour parcourire tout les arret de l'hyer-arret
        for edge in self.edges:
            edfreduit = max(1, int(len(edge) * (reduction_percentage / 100)))
            # La fonction random pour prendre un random des arretes.
            reduced_edge = random.sample(list(edge), edfreduit)
            # Ajoute la valeur random dans la liste reduced_edges.
            reduced_edges.append(set(reduced_edge))

        # retourner un hyper graphe réduite.
        return HyperGraph(reduced_edges)

    # fonction pour afficher soit le graphe de base soit celui qui est réduit.  
    def print_hyperedges(self):
        for edge in self.edges:
            print(edge)



'''############ LE MAIN #############'''
'''########################'''

# Le chemin de dataset a utilisé
file_path = r"C:\Users\aghil\OneDrive\Bureau\Master-2-SID-\S1\TER\Hypergraphes_Datasets_Expes\accidents\ac_150k.dat"
'''Fonction qui permet de stocker tout les arret de graphe pour aprés les donnée comme parametre dans le contructeur __init__'''
edges = []
with open(file_path, 'r') as file:
    for line in file:
        edge = set(map(int, line.strip().split()))
        edges.append(edge)

# Créer l'instance HyperGraph et trouver les transversaux minimaux
hypergraph = HyperGraph(edges)

reduced_hypergraph = hypergraph.reduce_hyperedges_improved(reduction_percentage=5)
#print(reduced_hypergraph.edges)
# reduced_hypergraph.print_hyperedges()

reduced_results = reduced_hypergraph.min_transversals()

resultats_sans_frozenset = [tuple(transversal) for transversal in reduced_results]
print("Transversals minimaux :\n", resultats_sans_frozenset)

end_time = time.time()
elapsed_time = end_time - start_time  # Temps écoulé en secondes
elapsed_time_minutes = elapsed_time * 1000  # Convertir en millisecondes

print(f"Temps d'exécution du programme : {elapsed_time_minutes:.2f} ms")
