Dans l'archive "fibad.zip", il y a :

Un fichier "podami.jar" contenant les fichiers sources (.java) et les fichiers binaires (.class) de l'implémentation. 
Les fichiers sources sont isolés dans une archive "src.zip" si besoin.

Le fichier "spmfmodif.jar" est une ressource externe utilisée pour le calcul de motifs fréquents maximaux (i.e., la bordure positive).

(remarque : FIBAD, Frequent Itemset Border Approximation by Dualization)

#############################################

Le script bash "fibad.sh" qui donne des exemples d'utilisation :

Partant d'un jeu de données et d'une valeur de minsup, les motifs fréquents maximaux sont déterminés (on a ainsi la bordure positive Bd+). 

On calcule la bordure négative Bd- à partir de Bd+ en appliquant le théorème (Bd-= MinTr(complements(Bd+))).

Juste pour vérifier que tout est ok, on retourne à la bordure positive en appliquant le second théorème (Bd+ = complements(MinTr(Bd-)))

La bordure négative approchée ~Bd- est calculée à partir de Bd+ avec la méthode proposée (réduction d'hypergraphe).

La bordure positive approchée ~Bd+ est calculée à partir de ~Bd- en appliquant le second théorème (Bd+ = complements(MinTr(Bd-)))


Dans chaque fichier de sortie, il y a en en-tête des informations sur les motifs (nombre, taille moyenne, ...) et la distance calculée avec une bordure de référence spécifiée lors de l'exécution.


D'autres indications sont dans le script fibad.sh sous la forme de commentaires.


#############################################

Organisation du code :
Package podami (Pattern Oriented DAta MIning)
3 sous-packages :
- common : structure de données utilisées (CoupleBitSet) pour représenter les motifs ou les hyperarêtes. (CoupleBitSet se base sur la classe BitSet)
- hypergraph : implémentation de différents algorithmes de calcul de transversaux minimaux d'hypergraphes, "berge.Berge", "dl.DL" (Dong & Li), "mtminer.MTminer", "staccato.Staccato2", "reduction.HR" (notre méthode)
- max : calcul de motifs fréquents maximaux FPmax et CharmMFI en utilisant la bibliothèque SPMF
- max.approx : calcul d'une bordure à partir d'une autre (CalculBordure), calcul de la distance entre deux ensembles de motifs (DistanceBordures).


#############################################

Le fichier "exemple.txt" et les autres fichiers "exemple..." correspondent à l'exemple de l'article.
Pour ré-exécuter cet exemple, il faut juste taper :
./fibad.sh exemple.txt 3

Le fichier "trace_exemple.txt" donne la trace d'exécution de l'exemple si tous les affichages sont activés (attributs booléens "en dur" dans les classes Calculbordure et HR).


Il y a aussi un autre jeu de données classique "chess".

