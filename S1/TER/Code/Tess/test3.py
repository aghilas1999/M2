def minimal_transversal(hypergraph):
    # Initialize the transversal and the set of available vertices
    transversal = []
    avail_vertices = set(range(len(hypergraph[0])))
    
    while avail_vertices:
        # Find an edge not intersecting the current transversal
        unused_edge = None
        for edge in hypergraph:
            if used := set(edge) & set(transversal):
                break
            else:
                unused_edge = edge
        
        # Check whether we have found an unused edge
        if unused_edge is None:
            continue
        
        # Choose a vertex from the found edge which isn't present in the transversal
        vtx = next((x for x in unused_edge if x not in transversal), None)
        
        # Update the sets
        transversal.append(vtx)
        avail_vertices -= {vtx}
        for i, edge in enumerate(hypergraph):
            if vtx in edge:
                del hypergraph[i]
                break
            
    return transversal
# Example usage
hypergraph = [
    [0, 1],
    [0, 1, 2]
]
print("Minimal Transversal:", minimal_transversal(hypergraph))