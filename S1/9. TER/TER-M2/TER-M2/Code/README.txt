## Mise en context
Ce script Python propose des fonctionnalités pour réduire les hypergraphes et calculer les transversaux minimaux. Ce qui constitue une premiere implémentation d'une nouvelle approche probabiliste .
Les principales fonctions sont :

1. `reduire_hypergraphe(chemin_fichier, seuil)`: Lit un hypergraphe depuis un fichier et le réduit en fonction d'un seuil spécifié.

2. `selectionner(ensemble, nombre_elements)`: Sélectionne de manière aléatoire un sous-ensemble d'éléments à partir d'un ensemble donné.

3. `calculate_TM(hypergraphe, N, m)`: Cette fonction implémente l'algorithme d'estimation stochastique de la transversale minimale.
Elle prend un hypergraphe, deux paramètres N et m en entrée et retourne une estimation de la transversale minimale.
L'algorithme fonctionne comme suit:
Calcul de Hr_i: Pour chaque itération i, N sommets sont tirés aléatoirement de chaque hyper-arête pour créer un ensemble Hr_i.
Calcul de TM_i: La transversale minimale de Hr_i est calculée et stockée dans TM_i.
Mise à jour de TM_old: TM_old est mis à jour en unionnant TM_old et TM_i.
Calcul de la transversale minimale: La liste des transversaux minimaux de TM_old est calculée et retournée.

l'hypergraphe est réduit à differents seuils. Pour chaque seuil, nous calculons k estimations de la transversale minimale et les stocke dans une liste ,le gain probable et la transversale minimale mise à jour.

## Utilisation

- `chemin_fichier`: Chemin vers le fichier d'hypergraphe.
- `N`: Nombre de sommets dans l'hypergraphe.
- `m`: Nombre d'itérations pour l'algorithme aléatoire.
- `k`: Nombre d'expériences à effectuer.
- `seuil1` et `seuil2`: Seuils pour la réduction d'hypergraphe.



## Applications:

- Analyse de réseaux complexes: Identifier des communautés ou des structures cachées dans les réseaux.
- Bioinformatique: Détecter des motifs dans les séquences d'ADN ou d'ARN.
- Apprentissage automatique: Sélectionner des caractéristiques importantes pour la construction de modèles.
- Fouille de données: Découvrir des structures et des relations cachées dans les ensembles de données.

## Collaborateurs: 
- Nicolas DURAND.
- Mohamed QUAFAFOU.
- Idriss FELLOUSSI.
- Aghilas SMAIL.