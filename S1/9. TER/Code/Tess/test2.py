class Hypergraph:
    def __init__(self, vertices, edges):
        self.V = vertices
        self.E = edges

    def is_transversal(self, T):
        # Vérifie si T est une transversale
        return all(any(v in T for v in e) for e in self.E)

    def is_non_redundant(self, T):
        # Vérifie si T est non-redondant
        return not any(self.is_transversal(T - {v}) for v in T)

def MTMiner(H):
    MT = [{v} for v in H.V if {v} in H.E]  # Transversales initiales
    N = [set()] if not MT else [set.union(MT[0], *MT[1:])]  # Union des transversales initiales
    j = 1

    while N[j-1]:
        for P in powerset(H.V):  # powerset est une fonction qui génère tous les sous-ensembles
            for v1 in H.V:
                for v2 in H.V:
                    if v1 != v2 and not P.union({v1, v2}).issubset(N[j-1]):
                        W = P.union({v1, v2})
                        if H.is_non_redundant(W):
                            if H.is_transversal(W):
                                MT.append(W)
                            else:
                                N[j-1] = N[j-1].union(W)
                        # La mise à jour de j devrait se faire en dehors des boucles
        j += 1
    return MT



# Exemple d'utilisation
vertices = {1, 2, 3, 4}  # Ensemble des sommets
edges = [{1, 2}, {2, 3}, {3, 4}]  # Ensemble des arêtes
H = Hypergraph(vertices, edges)

transversales_minimales = MTMiner(H)
for t in transversales_minimales:
    print(t)
