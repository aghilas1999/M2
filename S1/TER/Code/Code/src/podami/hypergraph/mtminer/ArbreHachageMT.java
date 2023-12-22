package podami.hypergraph.mtminer;

import java.util.ArrayList;
import java.util.BitSet;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Iterator;

import podami.common.CoupleBitSet;




/**
 * <p>Arbre de hachage :<br>
 * Structure de données pour stocker un ensemble de CoupleBitSet selon les ensembles de sommets (vertexSets).<br>
 * Un arbre de hachage contient des vertexSets de taille identique.<br>
 * k est la profondeur de l'arbre (k est aussi la taille des vertexSets stockes)</p>
 * <p>Implémentation de l'algorithme MTminer de Céline Hébert</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Université d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class ArbreHachageMT
{
	/**
	 * Racine de l'arbre de hachage
	 */
	private Noeud racine;

	/**
	 * Nombre de feuilles de l'arbre de hachage
	 */
	public int nbfeuilles;


	/**
	 * Constructeur
	 */
	public ArbreHachageMT()
	{
		racine = new Noeud();
	}

	
	/**
	 * Recuparation de la racine de l'arbre
	 * @return
	 */
	public Noeud getRacine() {
		return this.racine;
	}


	/**
	 * Ajoute un itemset à l'arbre de hachage
	 * @param it L'itemset a ajouter
	 */
	public void ajoute(CoupleBitSet it)
	{
		Noeud courant = racine;
		int i = 0;
		int index = -1;
		BitSet lesitems = it.getVertexes();
		int nbitems = it.getNbVertexes();
		int compteur = 0;

		while(i <= lesitems.size())
		{
			index = lesitems.nextSetBit(i);
			if(index == -1) break;

			compteur++;
			Integer cle = new Integer(index);
			if(courant.h.containsKey(cle)) 
			{
				// l'item est une clé du noeud courant
				courant = (Noeud)courant.h.get(cle);
			}
			else
			{
				if(compteur < nbitems)
				{
					// ce n'est pas le dernier item, 
					// il faut ajouter un nouveau noeud (interne) pour la cle item
					Noeud nouveau = new Noeud();
					courant.h.put(cle,nouveau);
					courant = nouveau;
				} 
				else 
				{
					// c'est le dernier item, on met l'itemset dans une feuille
					Noeud nouveau = new Noeud(it);
					courant.h.put(cle,nouveau);
					this.nbfeuilles++;
				}
			}

			i = index + 1;
		}

	}


	/**
	 * Teste si l'arbre de hachage est vide
	 * @return Un booléen indiquant si l'arbre de hachage est vide()
	 */
	public boolean estVide()
	{
		if((racine.h == null) && (racine.it == null)) return true;
		if((racine.h != null) && racine.h.isEmpty()) return true;
		if((racine.h == null) && (racine.it.emptyVertexSet())) return true;
		return false;
	}


	/**
	 * Fonction auxiliaire pour la methode selectFrequent
	 * @param lesitems Les items de l'itemset a supprimer
	 * @param courant Le noeud courant dans le parcours de l'arbre de hachage
	 * @param pere Le noeud pere dans le parcours
	 * @param cle La clé du noeud courant dans la table de hachage du noeud père
	 */
	public void supprimeAux(CoupleBitSet it, Noeud courant, Noeud pere, Object cle)
	{
		if(courant.feuille) 
		{
			// on a atteint l'itemset à supprimer
			pere.h.remove(cle);
		}
		else
		{
			BitSet lesitems = it.getVertexes();
			Integer lacle = new Integer(lesitems.nextSetBit(0));
			Noeud n = (Noeud)courant.h.get(lacle);
			it.removeVertex(lacle.intValue());
			supprimeAux(it,n,courant,lacle);
		}
	}


	/**
	 * Supprime de l'arbre de hachage l'itemset i
	 * @param i L'itemset à supprimer
	 */
	public void supprime(CoupleBitSet i)
	{
		supprimeAux(i,racine,racine,null);
	}


//	/**
//	 * Fonction auxiliaire pour la méthode fusion
//	 * @param courant Le noeud courant dans le parcours de l'arbre de hachage
//	 * @param resultat La liste des itemsets résultats
//	 * @param k La taille des itemsets stockés dans l'arbre
//	 * @param p La profondeur actuelle de l'arbre dans le parcours
//	 * @param genk 
//	 * @param mintr 
//	 */
//	public void fusionAux(Noeud courant, ArrayList<CoupleBitSet> resultat, int k, int p, ArrayList<CoupleBitSet> mintr, ArbreHachageMT gen, ArbreHachageMT genk)
//	{
//		if(p == (k-1))
//		{
//			// on extrait les itemsets contenus dans les feuilles du noeud courant (de profondeur k-1)
//			ArrayList<CoupleBitSet> v = new ArrayList<CoupleBitSet>();
//			for(Enumeration e = courant.h.elements(); e.hasMoreElements();)
//			{
//				CoupleBitSet i = ((Noeud)e.nextElement()).it;
//				v.add(i);
//			}
//			// on fusionne deux à deux ses itemsets
//			CoupleBitSet cbs1 = null;
//			CoupleBitSet cbs2 = null;
//			CoupleBitSet candidat = null;
//			for(int n = 0; n<=(v.size()-1); n++)
//			{
//				for(int j = n+1; j<=(v.size()-1); j++)
//				{
//					// on ajoute alors les itemsets résultats dans resultat
//					cbs1 = (CoupleBitSet)v.get(n);
//					cbs2 = (CoupleBitSet)v.get(j);
//					candidat = new CoupleBitSet(cbs1.unionVertexSet(cbs2), cbs1.intersectionEdgeSet(cbs2));
//
//					//TODO verif elagages
//					// elagage 1 : anti-monotonie minimalite :
//					// pour chaque candidat, test si son extension 
//					// est bien < a celle d'un de ses sous-ensembles
//					// ET elagage 2 : specialisation transversal minimal
//					ArrayList<CoupleBitSet> list = null;
//					int extcbs = -1;
//					int ext = -1;
//					int ii = -1;
//					list = candidat.subVertexSet();
//					extcbs = candidat.getNbEdges();
//					//
////					System.out.print("\n\nTEST minimalite : ");
////					cbs1.displayAll(null);
////					System.out.print("\n");
//					//
//					ii = 1;
//					for(Iterator c = list.iterator(); c.hasNext();) {
//						cbs2 = (CoupleBitSet)c.next();
//						ext = gen.getExtension(cbs2);
//						//
////						System.out.print("test : \t");
////						cbs2.displayAll(null);
////						System.out.print("\t / "+ext+"\n");
//						//
//						if(ext != -1 && extcbs < ext) ii = ii + 1;
//					}
//					//System.out.print("\t"+" "+ii+"\n");
//					// elagage specialisation transversal minimal
//					if(ii == (k + 2)) {
//						//if(liberte) {
//						if(extcbs == 0) {
//							//System.out.print("transversal minimal\n");
//							mintr.add(candidat);
//						}
//						else {
//							//System.out.print("generateur "+(k+1)+"\n");
//							genk.ajoute(candidat);
//						}
//					}
//
//					//resultat.add(candidat);
//				}
//			}
//		}
//		else
//		{
//			for(Enumeration e = courant.h.keys(); e.hasMoreElements();)
//			{
//				Noeud n = (Noeud)courant.h.get(e.nextElement());
//				fusionAux(n,resultat,k,p+1, mintr, gen, genk);
//			}
//		}
//	}
//
//
//	/**
//	 * Effectue la fusion des itemsets partageant leurs k-1 premiers items
//	 * On fusionne les itemsets issus d'un meme noeud
//	 * @param k La taille des itemsets stockés dans l'arbre
//	 * @param genk 
//	 * @param mintr 
//	 * @return Un arbre de hachage contenant les itemsets résultats de la fusion
//	 */
//	public void fusion(int k, ArrayList<CoupleBitSet> mintr, ArbreHachageMT gen, ArbreHachageMT genk)
//	{
//		ArrayList<CoupleBitSet> res = new ArrayList<CoupleBitSet>();
//		fusionAux(racine,res,k,0, mintr, gen, genk);
//	}


	/**
	 * fonction auxiliaire pour la méthode appartient
	 * @param courant Le noeud courant dans le parcours de l'arbre de hachage
	 * @param lesitems La liste des items de l'itemset à tester
	 */
	public boolean appartientAux(Noeud courant, BitSet lesitems)
	{
		// on hache les items de lesitems
		// si on a atteint une feuille, alors l'itemset correspondant à lesitems appartient à l'arbre de hachage
		if(courant.feuille)
		{
			return true;
		}
		else
		{
			if(lesitems.cardinality() > 0)
			{
				int index = -1;
				index = lesitems.nextSetBit(0);
				if(courant.h.containsKey(index))
				{
					Noeud n = (Noeud)courant.h.get(index);
					lesitems.set(lesitems.nextSetBit(0), false);
					return appartientAux(n,lesitems);
				}
				else return false;
			}
			else return false;
		}
	}


	/**
	 * Test si un itemset appartient à l'arbre de hachage
	 * @param i L'itemset à tester
	 * @return un booléen indiquant si i appartient à l'arbre de hachage
	 */
	public boolean appartient(CoupleBitSet i)
	{
		return appartientAux(racine,(BitSet)(i.getVertexes()).clone());
	}

	
	/**
	 * Fonction auxiliaire pour la recuperation de la taille de l'extension 
	 * (nombre d'hyperaretes) d'un candidat/generateur 
	 * @param courant Le noeud courant
	 * @param lesitems L'ensemble de sommets a rechercher dans l'arbre
	 * @return
	 */
	public int getExtensionAux(Noeud courant, BitSet lesitems)
	{
		// on hache les items de lesitems
		// si on a atteint une feuille, alors l'itemset correspondant à lesitems appartient à l'arbre de hachage
		if(courant.feuille)
		{
			return courant.it.getNbEdges();
		}
		else
		{
			if(lesitems.cardinality() > 0)
			{
				int index = -1;
				index = lesitems.nextSetBit(0);
				if(courant.h.containsKey(index))
				{
					Noeud n = (Noeud)courant.h.get(index);
					lesitems.set(lesitems.nextSetBit(0), false);
					return getExtensionAux(n,lesitems);
				}
				else return -1;
			}
			else return -1;
		}
	}


	/**
	 * Recuperation de la taille de l'extension (nombre d'hyperaretes) d'un candidat/generateur 
	 * @param i
	 * @return
	 */
	public int getExtension(CoupleBitSet i) {
		return getExtensionAux(racine,(BitSet)(i.getVertexes()).clone());
	}


	/**
	 * Retourne le nombre de feuille de l'arbre de hachage
	 * @return nombre de feuille
	 */
	public int nbFeuilles()
	{
		return this.nbfeuilles;
	}


	/**
	 * Fonction auxiliaire pour la méthode affiche
	 * @param debut Le noeud courant dans le parcours de l'arbre de hachage
	 * @param h La table de hachage contenant les noms des items
	 */
	public void afficheAux(Noeud debut, Hashtable<Integer,String> h)
	{
		if(debut.feuille) 
		{
			debut.it.displayAll(h); //displayVertexSet(h);
			System.out.print("\n"); 
		}
		else
		{
			for(Enumeration<Integer> e = debut.h.keys(); e.hasMoreElements();)
			{
				Noeud n = (Noeud)debut.h.get(e.nextElement());
				afficheAux(n,h);
			}
		}
	}


	/**
	 * Affiche les itemsets contenus dans l'arbre de hachage
	 * @param h Table de hachage contenant les noms des items
	 */
	public void affiche(Hashtable<Integer,String> h)
	{
		System.out.print("{\n");
		afficheAux(racine,h);
		System.out.print("}\n"); 
	}
	
	
	
	
	
	
	
	
	
	
	/**
	 * Fonction auxiliaire pour la méthode fusion
	 * @param courant Le noeud courant dans le parcours de l'arbre de hachage
	 * @param resultat La liste des itemsets résultats
	 * @param k La taille des itemsets stockés dans l'arbre
	 * @param p La profondeur actuelle de l'arbre dans le parcours
	 * @param genk 
	 * @param mintr 
	 * @param delta nombre max d'exception autorisees
	 */
	public void fusionAux(Noeud courant, ArrayList<CoupleBitSet> resultat, int k, int p, ArrayList<CoupleBitSet> mintr, ArbreHachageMT gen, ArbreHachageMT genk, int delta, int lambda)
	{
		if(p == (k-1))
		{
			// on extrait les itemsets contenus dans les feuilles du noeud courant (de profondeur k-1)
			ArrayList<CoupleBitSet> v = new ArrayList<CoupleBitSet>();
			for(Enumeration<Noeud> e = courant.h.elements(); e.hasMoreElements();)
			{
				CoupleBitSet i = ((Noeud)e.nextElement()).it;
				v.add(i);
			}
			// on fusionne deux à deux ses itemsets
			CoupleBitSet cbs1 = null;
			CoupleBitSet cbs2 = null;
			CoupleBitSet candidat = null;
			for(int n = 0; n<=(v.size()-1); n++)
			{
				for(int j = n+1; j<=(v.size()-1); j++)
				{
					// on ajoute alors les itemsets résultats dans resultat
					cbs1 = (CoupleBitSet)v.get(n);
					cbs2 = (CoupleBitSet)v.get(j);
					candidat = new CoupleBitSet(cbs1.unionVertexSet(cbs2), cbs1.intersectionEdgeSet(cbs2));

					//TODO verif elagages
					// elagage 1 : anti-monotonie minimalite :
					// pour chaque candidat, test si son extension 
					// est bien < a celle d'un de ses sous-ensembles
					// ET elagage 2 : specialisation transversal minimal
					ArrayList<CoupleBitSet> list = null;
					int extcbs = -1;
					int ext = -1;
					int ii = -1;
					list = candidat.subVertexSet();
					extcbs = candidat.getNbEdges();
					//
//					System.out.print("\n\nTEST minimalite : ");
//					cbs1.displayAll(null);
//					System.out.print("\n");
					//
					ii = 1;
					for(Iterator<CoupleBitSet> c = list.iterator(); c.hasNext();) {
						cbs2 = (CoupleBitSet)c.next();
						ext = gen.getExtension(cbs2);
						//
//						System.out.print("test : \t");
//						cbs2.displayAll(null);
//						System.out.print("\t / "+ext+"\n");
						//
						if(ext != -1 && (extcbs + lambda) < ext) //TODO
						//if(ext != -1 && extcbs < ext)
							ii = ii + 1;
					}
					//System.out.print("\t"+" "+ii+"\n");
					// elagage specialisation transversal minimal
					if(ii == (k + 2)) {
						//if(liberte) {
						//TODO
						//if(extcbs == 0) {
						if(extcbs <= delta) { //TODO
							//System.out.print("transversal minimal\n");
							mintr.add(candidat);
						}
						else {
							//System.out.print("generateur "+(k+1)+"\n");
							genk.ajoute(candidat);
						}
					}

					//resultat.add(candidat);
					
					
//					for(Iterator c = list.iterator(); c.hasNext();) {
//						cbs2 = (CoupleBitSet)c.next();
//						ext = gen.getExtension(cbs2);
//						if(ext != -1 && (extcbs+delta) < ext)  {
//							ii = ii + 1;
//						}
//					}
//					//System.out.print("\t"+liberte+" "+ii+"\n");
//					// elagage specialisation transversal minimal
//					if(ii == (k + 2)) {
//						freeSet.add(candidat);
//						if(extcbs > (minsupp+delta)) {
//							genk.ajoute(candidat);
//						}
//					}
					
					
				}
			}
		}
		else
		{
			for(Enumeration<Integer> e = courant.h.keys(); e.hasMoreElements();)
			{
				Noeud n = (Noeud)courant.h.get(e.nextElement());
				fusionAux(n,resultat,k,p+1, mintr, gen, genk, delta, lambda);
			}
		}
	}


	/**
	 * Effectue la fusion des itemsets partageant leurs k-1 premiers items
	 * On fusionne les itemsets issus d'un meme noeud
	 * @param k La taille des itemsets stockés dans l'arbre
	 * @param genk 
	 * @param mintr 
	 * @return Un arbre de hachage contenant les itemsets résultats de la fusion
	 */
	public void fusion(int k, ArrayList<CoupleBitSet> mintr, ArbreHachageMT gen, ArbreHachageMT genk, int delta, int lambda)
	{
		ArrayList<CoupleBitSet> res = new ArrayList<CoupleBitSet>();
		fusionAux(racine,res,k,0, mintr, gen, genk, delta, lambda);
	}
	
	
	
	


}
