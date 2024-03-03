# def minimal_transversal(hypergraph):
#     # Initialize the transversal and the set of available vertices
#     transversal = []
#     avail_vertices = set(range(len(hypergraph[0])))
    
#     while avail_vertices:
#         # Find an edge not intersecting the current transversal
#         unused_edge = None
#         for edge in hypergraph:
#             if used := set(edge) & set(transversal):
#                 break
#             else:
#                 unused_edge = edge
        
#         # Check whether we have found an unused edge
#         if unused_edge is None:
#             continue
        
#         # Choose a vertex from the found edge which isn't present in the transversal
#         vtx = next((x for x in unused_edge if x not in transversal), None)
        
#         # Update the sets
#         transversal.append(vtx)
#         avail_vertices -= {vtx}
#         for i, edge in enumerate(hypergraph):
#             if vtx in edge:
#                 del hypergraph[i]
#                 break
            
#     return transversal
# # Example usage
# hypergraph = [
#     [0, 1],
#     [0, 1, 2]
# ]
# print("Minimal Transversal:", minimal_transversal(hypergraph))


def is_transversal(transversal, hypergraph):
    """Vérifie si un ensemble est un transversal pour l'hypergraphe."""
    for edge in hypergraph:
        if not any(v in edge for v in transversal):
            return False
    return True

def find_minimal_transversals(hypergraph):
    """Trouve tous les transversals minimaux d'un hypergraphe."""
    vertices = set(v for edge in hypergraph for v in edge)
    minimal_transversals = []

    def dfs(current, start):
        if is_transversal(current, hypergraph):
            for t in minimal_transversals:
                if set(t).issuperset(current):
                    return
            minimal_transversals.append(list(current))
            return

        for v in range(start, len(vertices)):
            dfs(current + [vertices[v]], v + 1)

    dfs([], 0)
    return minimal_transversals

# Exemple d'utilisation
hypergraph = [{'A', 'B'}, {'B', 'C'}, {'C', 'D'}, {'A', 'D'}]
print("Transversals minimaux:", find_minimal_transversals(hypergraph))
