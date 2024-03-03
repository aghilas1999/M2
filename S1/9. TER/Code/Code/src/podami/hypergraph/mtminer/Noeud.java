package podami.hypergraph.mtminer;

import java.util.Hashtable;

import podami.common.CoupleBitSet;


/**
 * <p>Noeud d'un arbre de hachage</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Université d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class Noeud
{
	/**
	 * Les cles sont des strings (représentant les valeurs des sommets), les valeurs sont des noeuds
	 */
	public Hashtable<Integer,Noeud> h;

	/**
	 * Une feuille contient un CoupleBitSet (la table de hachage est alors vide)
	 */
	public CoupleBitSet it;

	/**
	 * Indique si le noeud est une feuille
	 */
	public boolean feuille;


	/**
	 * Creation d'un noeud interne
	 */
	public Noeud()
	{
		h = new Hashtable<Integer,Noeud>();
		feuille = false;
	}

	/**
	 * Creation d'une feuille
	 * @param i Le CoupleBitSet contenu dans la feuille
	 */
	public Noeud(CoupleBitSet i)
	{
		it = i;
		feuille = true;
	}
	
}
