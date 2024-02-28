import random
import time
import itertools

def reduire_hypergraphe(chemin_fichier, seuil):
    # Lire le fichier .hyp et stocker les hyper-arêtes dans une liste
    with open(chemin_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    hypergraphe = [list(map(int, ligne.split())) for ligne in lignes]

    # Créer une liste vide pour stocker les arêtes du graphe réduit
    graphe_reduit = []

    # Parcourir chaque hyper-arête dans l'hypergraphe
    for hyperarête in hypergraphe:
        # Calculer le nombre d'éléments à tirer en fonction du seuil
        nombre_elements_a_tirer = int(len(hyperarête) * (seuil / 100))

        # Sélectionner aléatoirement un sous-ensemble de l'hyper-arête
        hyperarête_réduite = selectionner(hyperarête, nombre_elements_a_tirer)

        # Ajouter le sous-ensemble à la liste des arêtes du graphe réduit
        graphe_reduit.append(hyperarête_réduite)

    return graphe_reduit

def selectionner(ensemble, nombre_elements):
    # Assurez-vous que le nombre d'éléments à tirer n'est pas supérieur à la taille de l'ensemble
    nombre_elements = min(nombre_elements, len(ensemble))

    # Tirage aléatoire du sous-ensemble
    sous_ensemble = random.sample(ensemble, nombre_elements)

    return sous_ensemble
''''
def calculate_TM(hyperedge):
    return len(hyperedge)

def calculate_min_TM(graph, N, m):
    min_TM = []

    for _ in range(m):
        random.shuffle(graph)
        random_hyperedge = random.choice(graph)
        TM_i = calculate_TM(random_hyperedge)
        min_TM.append(TM_i)

    min_TM.sort()  # Triez les traverses
    min_TM = min_TM[:min(N**2, len(min_TM))]  # Conservez seulement les N^2 plus petits traverses

    return min_TM
'''
#########################################


def calculate_TM(hypergraph, N, m):
    def is_vertex_cover(candidate_set, hyperedge):
        return any(vertex in candidate_set for vertex in hyperedge)

    def get_edges_covered(candidate_set, hyperedges):
        covered_edges = set()
        for hyperedge in hyperedges:
            if is_vertex_cover(candidate_set, hyperedge):
                covered_edges.update(itertools.combinations(hyperedge, 2))
        return covered_edges

    def calculate_Hr(hypergraph, N):
        return [set(random.sample(hyperedge, N)) for hyperedge in hypergraph]

    def calculate_TM_i(Hr, hyperedges):
        return set.union(*(get_edges_covered(candidate_set, hyperedges) for candidate_set in Hr))

    TM_old = set()

    for i in range(1, m + 1):
        Hr_i = calculate_Hr(hypergraph, N)
        TM_i = calculate_TM_i(Hr_i, hypergraph)
        TM_old = TM_old.union(TM_i)

    min_TM = min(TM_old, key=len) if TM_old else set()

    return list(min_TM)


 




'''print("Phase 1 : reduction de graphe ")
chemin_fichier = "Code\Hypergraphes_Datasets_Expes\Hypergraphes_Datasets_Expes\kosarak\kosarak.dat.39600.pos.su.compl.hyp"
seuil = 20
temps_debut = time.time()
graphe_reduit = reduire_hypergraphe(chemin_fichier, seuil)
# Enregistrez le temps de fin
temps_fin = time.time()

# Calculez la différence pour obtenir le temps d'exécution
temps_execution = temps_fin - temps_debut

print(f"Temps d'exécution : {temps_execution} secondes")
# Affichez le graphe réduit
print(graphe_reduit)
print("################################################################################## ")
print("Phase 2 : Calcule des transvers min  ")

N = 21
m = 10
k = 20
temps_debut = time.time()
min_TM_result = calculate_TM(graphe_reduit, N, m)
# Afficher le résultat
print("Min_TM:", min_TM_result)
temps_fin = time.time()


temps_execution = temps_fin - temps_debut
print(f"Temps d'exécution : {temps_execution} secondes")
Tms = all_TMs(graphe_reduit,N,m,k)
print("Min_Tms = :", min_TM_result)'''
print("Phase 1: réduction de graphe")

chemin_fichier = "Code\Hypergraphes_Datasets_Expes\Hypergraphes_Datasets_Expes\kosarak\kosarak.dat.39600.pos.su.compl.hyp"
N = 21
m = 10
k = 25  


seuil2 = 30
seuil1 = 20
All_Tms_10 = []
All_Tms_20 = []
min_Tms_10 = []
min_Tms_20 = [] 
temp = 0
for _ in range(k):
    temps_debut = time.time()
    graph_reduit1 = reduire_hypergraphe(chemin_fichier, seuil1)
    graph_reduit2 = reduire_hypergraphe(chemin_fichier, seuil2)
    min_Tms_10 = calculate_TM(graph_reduit1,N,m)
    All_Tms_10.append(min_Tms_10)
    min_Tms_20 = calculate_TM(graph_reduit2,N,m)
    All_Tms_20.append(min_Tms_20)
    temps_fin = time.time()
    temps_execution = temps_fin - temps_debut
    temp = temp + temps_execution
    
print ("temps totale : ",temp)

print("10% = ",All_Tms_10)
print("20% = ",All_Tms_20)
# Convertir les listes en ensembles
ensemble_10 = set(tuple(element) for element in All_Tms_10)
ensemble_20 = set(tuple(element) for element in All_Tms_20)

# Trouver l'intersection des ensembles
elements_communs = ensemble_10.intersection(ensemble_20)
print("common minima Transverals",elements_communs)
print("probable gain : ",len(elements_communs)/len(ensemble_20))
elements_non_communs = ensemble_10.difference(elements_communs)
updated_Tms = ensemble_10.union(elements_non_communs)
print("updated Tm_Min : ",updated_Tms)






