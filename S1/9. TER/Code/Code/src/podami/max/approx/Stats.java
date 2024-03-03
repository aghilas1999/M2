package podami.max.approx;


/**
 * Statistiques sur un ensemble de motifs 
 * @author Nicolas
 *
 */
public class Stats {
	
	public int nbMotifs;
	public int tailleMax;
	public int tailleMin;
	public double tailleMoy;
	
	
	/**
	 * Constructeur par defaut
	 */
	public Stats() {
		this.nbMotifs = 0;
		this.tailleMax = 0;
		this.tailleMin = Integer.MAX_VALUE;
		this.tailleMoy = 0;
	}
	
	
	/**
	 * Conversion en chaine de caracteres
	 */
	public String toString() {
		String s = "";
		s += "nbMotifs= "+this.nbMotifs+" ; taillemin = "+this.tailleMin+" ; taillemax = "+this.tailleMax+" ; taillemoy = "+this.tailleMoy;
		return s;
	}
	
}
