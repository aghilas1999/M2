#### \- Lire l'article avec un __l'objectif premier__ de refaire l'exemple en comprenant les notions associées et la méthode proposée.

#### Préparer des __questions__ si. besoin.

#### On en reparlera à la prochaine __réunion__ !

---

##### Continuer la lecture/compréhension de la méthode

##### Se concentrer sur la réduction d'un hypergraphe

##### Expérimenter/tester la réduction : HR et HRmulti

Pour plusieurs hypergraphes/datasets :

\- calcul de l'hypergraphe réduit avec HR et avec HRmulti, afin de comparer les temps d'exécution (et vérification mêmes résultats)

Pour la vérif : utiliser DistanceBordures hyp.red hyp.redmulti 0 (dans package max.approx), cela produit un fichier .stats

Pour la comparaison : mettre les résultats dans des tableaux, des figures, ...

Quelques hypergraphes : **ac (accidents), ...**

##### Détail de l'expé :

###### Protocole d'expérimentation

Des datasets sont dans le dossier "Hypergraphes_Datasets_Expes". Vous pouvez aussi utiliser d'autres datasets plus gros, cela dépendra de la puissance de votre machine (par exemple, avec un minsup plus bas : ac_90k.dat, bms2_100.dat, ...).

Chaque dataset est un hypergraphe correspondant au complément des motifs fréquents maximaux (Bd+) obtenus avec une certaine valeur minimale de support (indiquée dans le nom du fichier).

Pour chaque dataset :  
\- Générer l'hypergraphe réduit avec HR (podami.hypergraph.reduction.HR nom_dataset true)  
\- Générer l'hypergraphe réduit avec HRmulti (podami.hypergraph.reductionmulti.HRmulti nom_dataset true nb_threads)  
\- Calculer la distance entre les 2 hypergraphes réduits (podami.max.approx.DistanceBordures nom_dataset.red nom_dataset.redmulti 0)

Pour HRmulti, il faut fixer le nombre de threads utilisés. Ce nombre doit être inférieur ou égale au nombre de coeurs du processeur (par exemple, si processeur 4 core, alors fixer nb_threads à 4).

Pour éviter des problèmes de "out of memory" à l'exécution, mettez dès le début l'option "-Xmx" à la machine virtuelle java afin de définir une quantité de RAM max pour la JVM.  
Exemple si 2Go : java -Xmx2000m podami...  
A adapter selon la quantité de RAM de votre machine.

Autre remarque : l'idéal serait de faire toutes les exécutions sur une seule et même machine et de ne rien faire d'autre sur cette machine pendant les exécutions. Ce n'est pas évident mais c'est le mieux.  
Au pire, vous pouvez faire des exécutions sur vos deux machines mais chacune doit s'occuper d'une "famille" entière de datasets (par exemple "ac/accident" ou "bms:BMS-WebVeiw2", ...).

###### Présentation des résultats

\- Il faut penser à indiquer les caractéristiques de la (ou les) machine(s) utilisée(s) (processeur, quantité de RAM, OS) dans le récapitulatif des résultats.  
Si deux machines sont utilisées, quelle machine s'est occupée de telle famille de datasets.

\- Dans un ou plusieurs tableaux (peut-être un par "famille" de datasets), on aura avoir : nom dataset, temps exécution HR, temps execution HRmulti, distance entre les hypergraphes générés.

\- On peut aussi avoir des figures (une figure par "famille" de datasets) avec en abscisse la valeur qui différencie les datasets (valeur de minsup ou nbre d'hyperarêtes ou ...) et en ordonnée le temps d'exécution. Il y a alors 2 courbes sur une figure (une pour HR et une pour HRmulti).