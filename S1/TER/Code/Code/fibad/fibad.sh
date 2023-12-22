#!/bin/bash

CHEMIN=$(pwd)

export CLASSPATH="$CHEMIN/spmfmodif.jar":$CLASSPATH
export CLASSPATH="$CHEMIN/podami.jar":$CLASSPATH

if [[ $# -ne 2 ]]
then
  echo "usage: $0 filename minsup"
  exit 1
fi

#arg1 dataset
DATASET=$1

#arg2 minsup
MINSUP=$2

echo $DATASET $MINSUP;


#forme generale :
#java podami.max.approx.CalculBordure fichier_donnees type_bordure_sortie algo_trmin_utilise delta fichier_resultat_reel minsupport lambda

#fichier_donnees : nom du fichier contenant les donnees

#type_bordure_sortie : bordure que l'on souhaite calculee, "pos" ou "neg"

#algo_trmin_utilise : algorithme que l'on souhaite utilise pour le calcul des transversaux minimaux, "br" (Berge), "dl" (Dong & Li), "mt" (MTminer), "sta" (Staccato), "red" (notre methode).

#delta : entier utilise pour la tolerance d'exceptions (pour mt et sta seulement)

#fichier_resultat_reel :

#minsupport : valeur du support minimum (en absolu, nbre de transactions)

#lambda : entier utilise pour la tolerance d'exceptions (pour mt et sta seulement)




# positive border (maximal frequent itemsets, MFI)
echo "Positive border";
java -Xmx2000m podami.max.FPmax $DATASET $MINSUP $DATASET.$MINSUP.pos
#fichier de sortie : $DATASET.$MINSUP.pos

#si utilisation de IBE pour determiner les MFI
#ibe $DATASET $MINSUP $DATASET.$MINSUP.pos


## negative border (minimal infrequent itemsets)
echo "Negative border";
echo "java -Xmx2000m podami.max.approx.CalculBordure $DATASET.$MINSUP.pos neg dl 0 $DATASET.$MINSUP.pos $MINSUP 0"
java -Xmx2000m podami.max.approx.CalculBordure $DATASET.$MINSUP.pos neg dl 0 $DATASET.$MINSUP.pos $MINSUP 0
#fichier de sortie : $DATASET.$MINSUP.pos.dl.neg.cb


## verification (retour a la bordure positive / MFI)
echo "Positive border (verif)"
echo "java -Xmx2000m podami.max.approx.CalculBordure $DATASET.$MINSUP.pos.dl.neg.cb pos dl 0 $DATASET.$MINSUP.pos $MINSUP 0"
java -Xmx2000m podami.max.approx.CalculBordure $DATASET.$MINSUP.pos.dl.neg.cb pos dl 0 $DATASET.$MINSUP.pos $MINSUP 0
#fichier de sortie : DATASET.$MINSUP.pos.dl.neg.cb.dl.pos.cb


# approx negative border (calculBordure de fibad)
echo "Approx Negative border";
echo "java -Xmx4000m podami.max.approx.CalculBordure $DATASET.$MINSUP.pos neg red 0 $DATASET.$MINSUP.pos.dl.neg.cd $MINSUP 0"
java -Xmx2000m podami.max.approx.CalculBordure $DATASET.$MINSUP.pos neg red 0 $DATASET.$MINSUP.pos.dl.neg.cb $MINSUP 0
#fichier de sortie : $DATASET.$MINSUP.pos.red.neg.cb


# approx positive border (calculBordure de fibad)
echo "Approx Positive border";
echo "java -Xmx2000m podami.max.approx.CalculBordure $DATASET.$MINSUP.pos.red.neg.cb pos dl 0 $DATASET.$MINSUP.pos $MINSUP 0"
java -Xmx2000m podami.max.approx.CalculBordure $DATASET.$MINSUP.pos.red.neg.cb pos dl 0 $DATASET.$MINSUP.pos $MINSUP 0
#fichier de sortie : $DATASET.$MINSUP.pos.red.neg.cb.dl.pos.cb



