package podami.common;

import java.util.BitSet;
import java.util.Comparator;


//TODO A verifier


public class CompareCoupleBitSet implements Comparator<CoupleBitSet>{ 

		public CompareCoupleBitSet() {
		}
		
		
		private int compareBitSet(BitSet a, BitSet b) {
			int compare = 0;
			//si identique
			if(a.equals(b)) {
				compare = 0;
			}
			else {
				//parcourir les bitsets, des que un element differe, stop
				//retourner elt a - elt b
				int i = 0;
				int indexa = -1;
				int indexb = -1;
				boolean fini = false;
				int taille = 0; // taille du plus petit
				
				if(a.size() > b.size()) taille = b.size();
				else taille = a.size();
				
				while(i <= taille && !fini)
				{
					indexa = a.nextSetBit(i);
					indexb = b.nextSetBit(i);
					//si les index sont identiques, ok
					if(indexa == indexb) {
						//ne rien faire
					}
					else { // index different
						fini = true;
						compare = indexa - indexb;
					}
					i = indexa + 1;
				}
			}			
			return compare;
		}
	
		
	    public int compare(CoupleBitSet a, CoupleBitSet b) 
	    {
	    	BitSet vsa = a.getVertexes(); //vertex set du premier CoupleBitSet
	    	BitSet vsb = b.getVertexes(); //vertex set du deuxieme CoupleBitSet
	        return this.compareBitSet(vsa, vsb);
	    } 
	    
	    
	    

		/**
		 * @param args
		 */
		public static void main(String[] args) {

			CompareCoupleBitSet comp = new CompareCoupleBitSet();
			
			CoupleBitSet it1 = new CoupleBitSet();
			it1.addVertex(1);
			it1.addVertex(2);
			it1.addVertex(5);

			System.out.println("Itemset1 = ");
			it1.displayVertexSet(null);
			System.out.println("\n");


			CoupleBitSet it2 = new CoupleBitSet();
			it2.addVertex(1);
			it2.addVertex(3);
			it2.addVertex(5);
			it2.addVertex(10);

			System.out.println("Itemset2 = ");
			it2.displayVertexSet(null);
			System.out.println("\n");


			System.out.println("compare Itemset1 et Itemset2 = " + comp.compare(it1, it2));

			System.out.println("compare Itemset2 et Itemset1 = " + comp.compare(it2, it1));


			System.out.println("\n");
			System.out.println("\n");
			
			
			CoupleBitSet it3 = new CoupleBitSet();
			it3.addVertex(3);
			it3.addVertex(5);
			it3.addVertex(6);

			System.out.println("Itemset3 = ");
			it3.displayVertexSet(null);
			System.out.println("\n");

						
			CoupleBitSet it4 = new CoupleBitSet();
			it4.addVertex(3);
			it4.addVertex(5);
			it4.addVertex(6);
			it4.addVertex(10);
			it4.addVertex(11);
			
			System.out.println("\nItemset4 = ");
			it4.displayVertexSet(null);
			System.out.println("\n");

			
			System.out.println("compare Itemset3 et Itemset4 = " + comp.compare(it3, it4));
			
			System.out.println("compare Itemset4 et Itemset3 = " + comp.compare(it4, it3));
			
		}

} 
