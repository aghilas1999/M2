package podami.hypergraph.reductionmulti;

import java.util.ArrayList;
import java.util.Iterator;


/**
 * Graphe value non-oriente 
 *
 */
public class GrapheMulti {

	int nbSommets;
	int nbAretes;
	ArrayList<Arete> aretes;
	
	/**
	 * tableau de listes d'aretes
	 * tab[i] correspond a la liste des aretes ayant le sommet i a une de ses extremites 	
	 */
	ArrayList<Arete>[] contientSommets; 
	
	
	/**
	 * 
	 * @param nbs
	 */
	@SuppressWarnings("unchecked")
	public GrapheMulti(int nbs) {
		this.nbSommets = nbs;
		this.nbAretes = 0;
		this.aretes = new ArrayList<Arete>(); 
		this.contientSommets = new ArrayList[nbs+1];
		for(int i=1; i<=nbs; i++) this.contientSommets[i] = new ArrayList<Arete>();
	}
	
	
	/**
	 * 
	 * @param s1
	 * @param s2
	 * @param val
	 */
	public synchronized void addEdge(int s1, int s2, float val) {
		Arete a = new Arete(s1,s2,val);
		this.aretes.add(a);
		this.contientSommets[s1].add(a);
		this.contientSommets[s2].add(a);
		this.nbAretes++;
	}

	
	/**
	 * 
	 * @return
	 */
	public boolean isEmpty() {
		if(this.aretes.size() == 0) return true;
		return false;
		
		//TODO
//		for(Arete e : this.aretes)
//			if(e.estActif()) return false;
//		return true;
	} 
	
	
	/**
	 * 
	 * @return
	 */
	public int getNbAretes() {
		int nb = 0;
		for(Arete e : this.aretes)
			if(e.estActif()) nb++;
		return nb;
	}
	
	
	/**
	 * 
	 * @return
	 */
	public Arete getMax() {
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
		
//		Arete e = null;
//		for(int i=0; i<this.aretes.size(); i++) {
//			e = this.aretes.get(i);
//			if(e.estActif()) return e;
//		}
//		return e;
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
		
		/*
		ArrayList<Arete> asupprimer1 = this.contientSommets[ei];
		ArrayList<Arete> asupprimer2 = this.contientSommets[ej];
		
		//TODO
		//int compteur = 0;
		//System.out.println("Suppression aretes "+ei+" ou "+ej+" ("+(asupprimer1.size()+asupprimer2.size()-1)+") ");
		
		//System.out.println(asupprimer1);
		//System.out.println(asupprimer2);
			
		for(Arete e1 : asupprimer1) {
			//compteur += 1;
			//System.out.print("\r"+compteur);
		
			e1.desactive();
			
			//this.aretes.remove(e1); // trop long! ////////////////////////
		}
		
		for(Arete e2 : asupprimer2) {
			//compteur += 1;
			//System.out.print("\r"+compteur);
			
			e2.desactive();
			
			//this.aretes.remove(e2); // trop long! ////////////////////////
		}
		
		this.contientSommets[ei].clear();
		this.contientSommets[ej].clear();
		
		//System.out.print(" "+(asupprimer1.size()+asupprimer2.size())+" majContient");
		
		//TODO mise a jour des autres contientSommets[k] si arete k-ei ou k-ej
		for(int k=1; k<=this.nbSommets; k++) {
			ArrayList<Arete> l = (ArrayList<Arete>) this.contientSommets[k].clone();
			for(Arete e : l) {
				if(e.sommet1==ei || e.sommet2==ei || e.sommet1==ej || e.sommet2==ej)
					this.contientSommets[k].remove(e);
			}
		}
		*/
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
		/*
		String s = "";
		for(Iterator<Arete> i = this.aretes.iterator(); i.hasNext();) {
			Arete e = (Arete)i.next();
			if(e.estActif()) //TODO
					s = s + e.toString() + "\n";
		}
		return s;
		*/
	}


	
}
