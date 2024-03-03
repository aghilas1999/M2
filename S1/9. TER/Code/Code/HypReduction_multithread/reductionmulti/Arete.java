package podami.hypergraph.reductionmulti;


/**
 * Une arete d'un graphe
 */
public class Arete implements Comparable<Arete> {

	public int sommet1;
	public int sommet2;
	public float valeur;
	public boolean actif;
	
	public Arete(int s1, int s2) {
		this.sommet1 = s1;
		this.sommet2 = s2;
		this.valeur = 0;
		this.actif = true;
	}
	
	public Arete(int s1, int s2, float val) {
		this.sommet1 = s1;
		this.sommet2 = s2;
		this.valeur = val;
		this.actif = true;
	}

	public String toString() {
		return (this.sommet1+"-"+this.sommet2+"("+this.valeur+")");
	}

	public int compareTo(Arete a) {
	    if(this.valeur > a.valeur) return -1;
	    if(this.valeur < a.valeur) return 1;
	    return 0; // (this.valeur == a.valeur)
	}
	
	public void active() {
		this.actif = true;
	}
	
	public void desactive() {
		this.actif = false;
	}
	
	public boolean estActif() {
		return this.actif;
	}
	
}
