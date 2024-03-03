package podami.hypergraph.reduction;


/**
 * Une arete d'un graphe
 */
public class Arete implements Comparable<Arete> {

	public int sommet1;
	public int sommet2;
	public float valeur;
	
	public Arete(int s1, int s2) {
		this.sommet1 = s1;
		this.sommet2 = s2;
		this.valeur = 0;
	}
	
	public Arete(int s1, int s2, float val) {
		this.sommet1 = s1;
		this.sommet2 = s2;
		this.valeur = val;
	}

	public String toString() {
		return (this.sommet1+"-"+this.sommet2+"("+this.valeur+")");
	}

	public int compareTo(Arete a) {
	    if(this.valeur > a.valeur) return -1;
	    if(this.valeur < a.valeur) return 1;
	    return 0; // (this.valeur == a.valeur)
	}
	
}
