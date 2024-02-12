
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
    
def calculate_TM(hyperedge):
    return len(hyperedge)

def calculate_min_TM(graph, N, m):
    min_TM = []

    for _ in range(m):
        random.shuffle(graph)
        random_hyperedge = random.choice(graph)
        TM_i = calculate_TM(random_hyperedge)
        min_TM.append(TM_i)

    #min_TM.sort()  # Triez les traverses
    #min_TM = min_TM[:min(N**2, len(min_TM))]  # Conservez seulement les N^2 plus petits traverses

    return min_TM

print("Phase 1 : reduction de graphe ")
chemin_fichier = r"C:\Users\aghil\OneDrive\Bureau\Master-2-SID-\S1\TER\Hypergraphes_Datasets_Expes\kosarak\kosarak.dat.3960.pos.su.compl.hyp"
seuil = 10
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
m = 5

min_TM_result = calculate_min_TM(graphe_reduit, N, m)
# Afficher le résultat
print("Min_TM:", min_TM_result)