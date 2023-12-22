package podami.hypergraph.reductionmulti;

import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashMap;

import podami.common.CoupleBitSet;


/**
 * <p>Thread pour la reduction d'un hypergraphe</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Universite d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class HRthread extends Thread {

	/**
	 * L'hypergraphe (ensemble d'hyperaretes)
	 */
	public ArrayList<CoupleBitSet> hyper;
	
	/**
	 * Table des occurrences des sommets dans l'ensembles des hyperaretes
	 */
	private HashMap<Integer, Integer> occurrences;

	
	private GrapheMulti graphe;
	
	
	
	private boolean affichage;

	private boolean affichage2;
	
	
	
	private int idebut;
	
	private int ifin;
	
	
	public static boolean aucuneintersection;
	
	private int id;
	
	
	/**
	 * 
	 */
	public HRthread(GrapheMulti graphe, int k, ArrayList<CoupleBitSet> h, HashMap<Integer, Integer> occ, int debut, int fin) {
		this.graphe = graphe;
		this.hyper = h;
		this.occurrences = occ;
		this.idebut = debut;
		this.ifin = fin;
		this.id = k;
		
		this.affichage = false;
		this.affichage2 = false;
	}
	
	
	/**
	 * Activite.
	 */
	public void run() {
				
		//System.out.println("\nThread intersections et poids : "+this.idebut+" -> "+this.ifin);
		
		if(affichage) System.out.println("\nThread "+this.id+" : "+this.idebut+" -> "+this.ifin);
		CoupleBitSet cbs = null;
		CoupleBitSet cbs2 =null;
		BitSet inter = null;
		float poids = -1;
		//boolean aucuneintersection = true;
		int index = 0;
		
		for(int i=this.idebut; i<=this.ifin; i++)
		{
			cbs = this.hyper.get(i-1);
			for(int j=i+1; j<=this.hyper.size(); j++)
			{
				cbs2 = this.hyper.get(j-1);
				if(affichage2) {System.out.print("cbs= "); cbs.displayVertexSet(null); System.out.print("\n");}
				if(affichage2) {System.out.print("cbs2= "); cbs2.displayVertexSet(null); System.out.print("\n");}
				inter = cbs.intersectionVertexSet(cbs2);

				//poids = somme des occurrences des sommets presents dans l'intersection
				poids = 0;
				int l = 1;
				index = 0;
				while(l <= inter.size())
				{
					index = inter.nextSetBit(l);
					if(index == -1) break;
					poids = poids + this.occurrences.get(new Integer(index)).intValue();
					l = index + 1;
					aucuneintersection = false;
				}

				if(poids > 0) {
					this.graphe.addEdge(i, j, poids);
					if(affichage2) System.out.println("ajout arete : "+i+" "+j+" ("+poids+")");
				}

				if(affichage2) System.out.println("inter= "+inter+" ("+poids+")");
				if(affichage2) System.out.print("\n");
			}
		}
		
		if(affichage) System.out.println("\nThread "+this.id+" : fini");
		
	}
	
}
