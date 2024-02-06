'''def is_transversal(transversal, hypergraph):
    for edge in hypergraph:
        if not any(v in edge for v in transversal):
            return False
    return True

# Exemple de graphe hyperédger
hypergraph = [{"A", "B"}, {"B", "C"}, {"C", "D"}, {"A", "D"}]

# Ensemble potentiellement transversal
potential_transversal = {"A", "C"}

resultat = is_transversal(potential_transversal, hypergraph)

if resultat:
    print("L'ensemble est un transversal.")
else:
    print("L'ensemble n'est pas un transversal.")'''
    

'''from collections import defaultdict
import itertools

def find_minimal_transversals(hypergraph):
    vertices = set()
    for edge in hypergraph:
        for v in edge:
            vertices.add(v)
    
    minimal_transversals = []

    for combination in itertools.combinations(sorted(list(vertices)), len(hypergraph)):
        is_transversal = all(any(vertex in edge for vertex in combination) for edge in hypergraph)
        
        if is_transversal and len(combination) <= len(vertices):
            minimal_transversals.append(tuple(combination))
            
    return minimal_transversals

# Test sur le graphe hyperédger fourni
hypergraph = [{"A", "B"}, {"B", "C"}, {"C", "D"}, {"A", "D","E"}]

print("Transversals minimaux :\n", find_minimal_transversals(hypergraph))'''


# ca marche pour des hyper graphe binaire 
'''from collections import defaultdict
from heapq import heappush, heappop

class HyperGraph:
    def __init__(self, edges):
        self.nodes = set()
        for edge in edges:
            self.nodes |= set(edge)
        self.adjacency_lists = {node: [] for node in self.nodes}
        for u, v in edges:
            self.adjacency_lists[u].append(v)

    def min_transversals(self):
        min_transversals = set()
        cut_queue = [(frozenset(self.nodes), frozenset())]

        while cut_queue:
            current_cut, current_transversal = heappop(cut_queue)

            if len(current_cut) == 1:
                min_transversals.add(tuple(current_transversal))
                continue

            for node in current_cut - current_transversal:
                neighbors = self.adjacency_lists[node]
                for neighbor in neighbors:
                    if neighbor not in current_transversal:
                        new_cut = set(current_cut.copy())  # Utiliser un set au lieu d'un frozenset
                        new_cut.remove(node)
                        new_cut.discard(neighbor)
                        new_transversal = set(current_transversal.copy())
                        new_transversal.add(node)
                        heappush(cut_queue, (new_cut, new_transversal))

        return min_transversals

# Exemple d'utilisation
hypergraph = [{"A", "B"}, {"B", "C"}, {"C", "D"}, {"A", "D","E"}]
resultats = HyperGraph(hypergraph).min_transversals()
print("Transversals minimaux :\n", resultats)'''


#Maintenant on test une autre avec une list d'hyper-graphe.
'''
import networkx as nx
from collections import defaultdict

def create_hypergraph():
    hypergraph = defaultdict(list)
    
    # Liste de hyperarêtes (indices des sommets)
    hyperedges_str =   [
            "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
            "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
            # Ajoutez autant de chaînes que nécessaire pour représenter toutes vos hyperarêtes
        ]
    hypergraph_data = [[int(num) for num in hyperedge.split()] for hyperedge in hyperedges_str]

    for h in hypergraph_data:
        hypergraph[len(h)].append(sorted(h))
        
    return nx.DiGraph(hypergraph)

def min_transversals(hypergraph):
    G = nx.convert_node_labels_to_integers(hypergraph)
    H = nx.to_hypergraph(G)

    def min_cut(node):
        cut_set = set([node])
        for child in H[node]:
            if child not in cut_set:
                cut_set |= min_cut(child)
        return cut_set

    return set(nx.algorithms.dag.descendants(H, source=next(iter(H)))) - set(map(frozenset, filter(None, map(min_cut, nx.topological_sort(H)))))

# Création du hypergraphe
hypergraph = create_hypergraph()
print("Transversaux minimaux:", min_transversals(hypergraph))'''


# Visualisation d'un hyperarret avec plot()
'''
import networkx as nx

def create_hypergraph():
    # Hyperarêtes définies comme des chaînes de caractères
    hyperedges_str = [
        "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
        "0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63",
        # Plus d'hyperarêtes si nécessaire
    ]

    # Création d'un graphe biparti pour représenter l'hypergraphe
    B = nx.Graph()
    
    # Ajout des nœuds et des arêtes à partir des hyperarêtes
    for index, hyperedge_str in enumerate(hyperedges_str):
        # Créer un identifiant unique pour chaque hyperarête
        hyperedge_id = f"hyperedge_{index}"
        
        # Ajouter le nœud de l'hyperarête
        B.add_node(hyperedge_id, bipartite=0)
        
        # Convertir la chaîne de caractères en une liste de sommets
        vertices = [int(num) for num in hyperedge_str.split()]
        
        # Ajouter les sommets et les lier à l'hyperarête
        for vertex in vertices:
            B.add_node(vertex, bipartite=1)
            B.add_edge(hyperedge_id, vertex)
    
    return B

# Création de l'hypergraphe
B = create_hypergraph()

# Visualisation du graphe (nécessite matplotlib)
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

# Positionnement des nœuds pour la visualisation
pos = {node:[0, i] for i, node in enumerate([n for n in B.nodes if B.nodes[n]['bipartite']==0])}
pos.update({node:[1, i] for i, node in enumerate([n for n in B.nodes if B.nodes[n]['bipartite']==1])})

# Dessin du graphe
nx.draw(B, pos, with_labels=True, node_color=['lightblue' if B.nodes[n]['bipartite'] == 0 else 'lightgreen' for n in B.nodes])
plt.show()
'''


# test avec un hypergraphe d'entrée.

from collections import defaultdict
from heapq import heappush, heappop

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
hypergraph_data = """
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 29 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 21 22 23 24 25 26 28 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 22 23 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 25 26 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 21 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 22 23 24 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 16 19 20 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 18 19 20 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 21 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 16 19 20 21 22 23 24 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 18 19 20 21 22 23 24 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 22 23 24 25 26 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 16 19 20 21 22 23 24 25 26 28 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 21 22 23 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 29 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 22 23 24 25 26 27 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 21 22 23 24 25 26 27 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 22 23 24 25 26 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 25 26 27 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 21 22 23 24 25 26 27 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 18 19 20 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 21 22 23 24 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 18 19 20 21 22 23 24 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 28 29 30 32 33 34 35 36 37 38 39 40 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 21 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 29 30 32 33 34 35 36 37 38 39 40 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 26 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 19 20 21 22 23 24 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 26 27 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 21 22 23 24 26 27 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 18 19 20 22 23 24 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 22 23 24 25 26 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 21 22 23 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 16 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 21 22 23 24 25 26 27 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 60 61 62 63
0 1 2 3 4 5 6 7 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 9 10 11 13 14 15 19 20 21 22 23 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 9 10 11 13 14 15 19 20 22 23 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 9 10 11 13 14 15 19 20 21 22 23 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 9 10 11 13 14 15 16 19 20 21 22 23 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 21 22 23 24 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 2 3 4 5 6 7 8 9 10 11 13 14 15 18 19 20 21 22 23 24 25 26 27 28 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 16 19 20 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 18 19 20 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 17 18 19 20 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62
0 1 2 3 4 5 6 7 8 9 10 11 13 15 19 20 21 22 23 24 25 26 27 28 29 30 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
0 1 2 3 4 5 6 7 8 9 10 11 13 14 15 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63

"""

edges = [set(map(int, line.split())) for line in hypergraph_data.strip().split('\n')]

# Créer l'instance HyperGraph et trouver les transversaux minimaux
hypergraph = HyperGraph(edges)
resultats = hypergraph.min_transversals()

resultats_sans_frozenset = [tuple(transversal) for transversal in resultats]

print("Transversals minimaux :\n", resultats_sans_frozenset)