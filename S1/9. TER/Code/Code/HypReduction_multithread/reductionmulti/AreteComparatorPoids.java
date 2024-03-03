package podami.hypergraph.reductionmulti;

import java.util.Comparator;


// tri du poids max au min 

public class AreteComparatorPoids implements Comparator<Arete>{

	public AreteComparatorPoids(){
	}

	public int compare(Arete e1, Arete e2) {
		float e1poids = e1.valeur;
		float e2poids = e2.valeur;

		if(e1poids < e2poids) return 1;
			else if(e1poids > e2poids) return -1;
				else {
					//meme poids, alors diff par rapport au numero de sommet
					int e1sommet1 = e1.sommet1;
					int e1sommet2 = e1.sommet2;

					int e2sommet1 = e2.sommet1;
					int e2sommet2 = e2.sommet2;
					
					if(e1sommet1 < e2sommet1) return -1;
					else {
						if(e1sommet1 == e2sommet1) {
							if(e1sommet2 < e2sommet2) return -1;
							if(e1sommet2 == e2sommet2) return 0;
							if(e1sommet2 > e2sommet2) return 1;
						} else //if(e1sommet1 > e2sommet1)
							return 1;
					}
					return 0;
				}

		//		Float val1 = lesEvals.get(o1);
		//		Float val2 = lesEvals.get(o2);
		//		//System.out.println("compare "+o1+" ("+val1+") "+o2+" ("+val2+") ");
		//		if(val1 < val2) return -1;
		//		else if(val1 > val2) return 1;
		//		else return 0;
		//		//return val2-val1;
	}

}
