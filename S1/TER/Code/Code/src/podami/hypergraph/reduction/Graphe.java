package podami.hypergraph.reduction;

import java.util.ArrayList;
import java.util.Iterator;


/**
 * Graphe value non-oriente 
 *
 */
public class Graphe {

	int nbSommets;
	int nbAretes;
	ArrayList<Arete> aretes;
	
	
	/**
	 * 
	 * @param nbs
	 */
	public Graphe(int nbs) {
		this.nbSommets = nbs;
		this.nbAretes = 0;
		this.aretes = new ArrayList<Arete>(); 
	}
	
	/**
	 * 
	 * @param s1
	 * @param s2
	 * @param val
	 */
	public void addEdge(int s1, int s2, float val) {
		Arete a = new Arete(s1,s2,val);
		this.aretes.add(a);
		this.nbAretes++;
	}

	/**
	 * 
	 * @return
	 */
	public boolean isEmpty() {
		if(this.aretes.size() == 0) return true;
		return false;
	} 
	
	/**
	 * Recherche arete de valeur max
	 * @return
	 */
	public Arete valMax() {
		float max = 0;
		Arete rep = null;
		for(Iterator<Arete> i = this.aretes.iterator(); i.hasNext();) {
			Arete e = (Arete)i.next();
			if(e.valeur > max) {
				rep = e;
				max = e.valeur;
			}
		}
		return rep;
	}
	
	/**
	 * Suppression des aretes ayant pour sommet ei ou ej
	 * @param ei
	 * @param ej
	 */
	public void cleanGraphe(int ei, int ej) {
		ArrayList<Arete> asupprimer = new ArrayList<Arete>();
		for(Iterator<Arete> i = this.aretes.iterator(); i.hasNext();) {
			Arete e = (Arete)i.next();
			if(e.sommet1==ei || e.sommet2==ei || e.sommet1==ej || e.sommet2==ej)
				asupprimer.add(e);
		}
		for(Iterator<Arete> i2 = asupprimer.iterator(); i2.hasNext();) {
			Arete e2 = (Arete)i2.next();
			this.aretes.remove(e2);
		}
	}
	
	/**
	 * 
	 */
	public String toString() {
		String s = "";
		for(Iterator<Arete> i = this.aretes.iterator(); i.hasNext();) {
			Arete e = (Arete)i.next();
			s = s + e.toString() + " ";
		}
		s = s + "\n";
		return s;
	}
	
}
