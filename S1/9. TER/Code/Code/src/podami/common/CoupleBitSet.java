package podami.common;

import java.io.BufferedWriter;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.Hashtable;
import java.util.Iterator;



/**
 * <p>Regroupement de deux BitSet (un pour l'ensemble de sommets, un autre pour l'ensemble d'hyperaretes)</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Université d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class CoupleBitSet {

	/**
	 * Ensemble de sommets (i.e. attributs, items)
	 */
	public BitSet vertexSet;

	/**
	 * Ensemble d'hyperaretes (i.e. objets, transactions) 
	 */
	public BitSet edgeSet;


	public float value;
	
	
	
	/**
	 * Constructeur par defaut
	 */
	public CoupleBitSet()
	{
		this.vertexSet = new BitSet();
		this.edgeSet = new BitSet();
	}

	/**
	 * Constructeur avec un ensemble de sommets
	 * @param vertexes L'ensemble de sommets
	 */
	public CoupleBitSet(BitSet vertexes)
	{
		this.vertexSet = vertexes;
		this.edgeSet = new BitSet();
	}

	/**
	 * Constructeur avec un ensemble de sommets
	 * @param vertexes L'ensemble de sommets
	 * @param edges L'ensemble d'hyperaretes
	 */
	public CoupleBitSet(BitSet vertexes, BitSet edges)
	{
		this.vertexSet = vertexes;
		this.edgeSet = edges;
	}

	
	/**
	 * Clonage du CoupleBitSet
	 */
	public CoupleBitSet clone()
	{
		CoupleBitSet newcbs = new CoupleBitSet();
		newcbs.vertexSet = (BitSet) this.vertexSet.clone();
		newcbs.edgeSet = (BitSet) this.edgeSet.clone();
		return newcbs;
	}
	

	/**
	 * Ajout d'un sommet
	 * (positionne le bit correspondant a 1)
	 * @param n Le numero du sommet a ajouter
	 */
	public void addVertex(int n)
	{
		this.vertexSet.set(n, true);
	}

	/**
	 * Ajout d'une hyperarete
	 * (positionne le bit correspondant a 1)
	 * @param n Le numero de l'hyperarete a ajouter
	 */
	public void addEdge(int n)
	{
		this.edgeSet.set(n, true);
	}

	/**
	 * Suppression d'un sommet
	 * (positionne le bit correspondant a 0)
	 * @param n Le numero du sommet a supprimer
	 */
	public void removeVertex(int n)
	{
		this.vertexSet.set(n, false);
	}

	/**
	 * Suppression d'une hyperarete
	 * (positionne le bit correspondant a 0)
	 * @param n Le numero de l'hyperarete a supprimer
	 */
	public void removeEdge(int n)
	{
		this.edgeSet.set(n, false);
	}

	/**
	 * Nombre de sommets
	 * @return Le nombre de bit a 1 de l'ensemble des sommets
	 */
	public int getNbVertexes()
	{
		return this.vertexSet.cardinality();
	}

	/**
	 * Nombre d'hyperaretes
	 * @return Le nombre de bit a 1 de l'ensemble des hyperaretes
	 */
	public int getNbEdges()
	{
		return this.edgeSet.cardinality();
	}

	/**
	 * Test si l'ensemble des sommets est vide
	 * @return Vrai si vide, faux sinon
	 */
	public boolean emptyVertexSet()
	{
		if(this.vertexSet.cardinality() == 0) return true;
		else return false;
	}

	/**
	 * Test si l'ensemble des hyperaretes est vide
	 * @return Vrai si vide, faux sinon
	 */
	public boolean emptyEdgeSet()
	{
		if(this.edgeSet.cardinality() == 0) return true;
		else return false;
	}


	/**
	 * Recuperation de l'ensemble des sommets
	 * @return L'ensemble des sommets
	 */
	public BitSet getVertexes()
	{
		return this.vertexSet;
	}

	/**
	 * Affectation de l'ensemble des hyperaretes
	 */
	public void setEdges(BitSet edges)
	{
		this.edgeSet = edges;
	}

	/**
	 * Affectation de l'ensemble des sommets
	 */
	public void setVertexes(BitSet vertexes)
	{
		this.vertexSet = vertexes;
	}

	/**
	 * Recuperation de l'ensemble des hyperaretes
	 * @return L'ensemble des hyperaretes
	 */
	public BitSet getEdges()
	{
		return this.edgeSet;
	}

	/**
	 * Test d'egalite entre l'ensemble des sommets et un bitset
	 * @param bs Le bitset a comparer
	 * @return Vrai si egaux, faux sinon
	 */
	public boolean equalsVertexSet(BitSet bs)
	{
		return this.vertexSet.equals(bs);
	}

	/**
	 * Test d'egalite entre l'ensemble des hyperaretes et un BitSet
	 * @param bs Le bitset a comparer
	 * @return Vrai si egaux, faux sinon
	 */
	public boolean equalsEdgeSet(BitSet bs)
	{
		return this.edgeSet.equals(bs);
	}

	/**
	 * Test d'egalite de l'ensemble des sommets avec celui d'un autre CoupleBitSet
	 * @param cpbs Le CoupleBitSet a comparer
	 * @return Vrai si egaux, faux sinon
	 */
	public boolean equalsVertexSet(CoupleBitSet cpbs)
	{
		return this.vertexSet.equals(cpbs.getVertexes());
	}

	/**
	 * Test d'egalite de l'ensemble des hyperaretes avec celui d'un autre CoupleBitSet
	 * @param cpbs Le CoupleBitSet a comparer
	 * @return Vrai si egaux, faux sinon
	 */
	public boolean equalsEdgeSet(CoupleBitSet cpbs)
	{
		return this.edgeSet.equals(cpbs.getEdges());
	}

	/**
	 * Union de l'ensemble de sommets avec celui d'un autre CoupleBitSet 
	 * @param i Un CoupleBitSet
	 * @return Le BitSet correspondant a l'union
	 */
	public BitSet unionVertexSet(CoupleBitSet i)
	{
		BitSet bs = (BitSet)this.vertexSet.clone();
		bs.or(i.getVertexes());
		return bs;
	}

	/**
	 * Union de l'ensemble d'hyperaretes avec celui d'un autre CoupleBitSet 
	 * @param i Un CoupleBitSet
	 * @return Le BitSet correspondant a l'union
	 */
	public BitSet unionEdgeSet(CoupleBitSet i)
	{
		BitSet bs = (BitSet)this.edgeSet.clone();
		bs.or(i.getEdges());
		return bs;
	}

	/**
	 * Intersection de l'ensemble de sommets avec celui d'un autre CoupleBitSet
	 * @param i Un CoupleBitSet
	 * @return Le BitSet correspondant a l'intersection
	 */
	public BitSet intersectionVertexSet(CoupleBitSet i)
	{
		BitSet bs = (BitSet)this.vertexSet.clone();
		bs.and(i.getVertexes());
		return bs;
	}

	/**
	 * Intersection de l'ensemble d'hyperaretes avec celui d'un autre CoupleBitSet
	 * @param i Un CoupleBitSet
	 * @return Le BitSet correspondant a l'intersection
	 */
	public BitSet intersectionEdgeSet(CoupleBitSet i)
	{
		BitSet bs = (BitSet)this.edgeSet.clone();
		bs.and(i.getEdges());
		return bs;
	}

	/**
	 * Teste si un sommet correspondant a la valeur n appartient a l'ensemble de sommets
	 * @param n La valeur du sommet a tester
	 * @return Vrai si appartient, faux sinon
	 */
	public boolean belongsVertexSet(int n)
	{
		return this.vertexSet.get(n);
	}

	/**
	 * Teste si une hyperarete correspondant a la valeur n appartient a l'ensemble des hyperaretes
	 * @param n La valeur de l'hyperarete a tester
	 * @return Vrai si appartient, faux sinon
	 */
	public boolean belongsEdgeSet(int n)
	{
		return this.edgeSet.get(n);
	}


	/**
	 * Teste si l'ensemble des commets est inclu dans un autre  
	 * @param tr L'autre ensemble de sommets
	 * @return Booleen
	 */
	public boolean isIncluded(CoupleBitSet tr)
	{
		BitSet bs = tr.getVertexes();
		
		int i = 0;
		int index = -1;

		while(i <= this.vertexSet.size())
		{
			index = this.vertexSet.nextSetBit(i);
			if(index == -1) break;
			if(bs.get(index) == false) return false;
			i = index + 1;
		}
		return true;
	}


	/**
	 * Retire de l'ensemble des sommets ceux contenus dans un autre ensemble de sommets d'un CoupleBitSet
	 * @param ens L'autre CoupleBitSet
	 */
	public void minusVertexes(CoupleBitSet ens)
	{
		//affiche(null,false);
		//System.out.print("\n");
		//ens.affiche(null,false);
		//System.out.print("\n");
		int i = 0;
		int index = -1;
		BitSet sommets = ens.getVertexes();

		while(i <= sommets.size())
		{
			index = sommets.nextSetBit(i);
			if(index == -1) break;
			this.vertexSet.set(index, false);
			i = index + 1;
		}

		//System.out.print("res= "); affiche(null,false);
	}

	/**
	 * Teste si l'ensemble de sommets est inclu dans un autre ensemble 
	 * @param bs L'autre ensemble
	 * @return Booleen
	 */
	public boolean includedVertexSet(BitSet bs)
	{
		//
		//i.getItems().intersects(v);
		//
		//System.out.println(i.ferme);
		int i = 0;
		int index = -1;

		while(i <= this.vertexSet.size())
		{
			index = this.vertexSet.nextSetBit(i);
			if(index == -1) break;
			if(bs.get(index) == false) return false;
			i = index + 1;
		}
		return true;
	}

	
	
	
	public boolean includedVertexSet(BitSet bs, int delta) {
		//
		//i.getItems().intersects(v);
		//
		//System.out.println(i.ferme);
		int i = 0;
		int index = -1;
		int erreurs = 0;
		
		while(i <= this.vertexSet.size())
		{
			index = this.vertexSet.nextSetBit(i);
			if(index == -1) break;
			if(bs.get(index) == false) 
				{
					erreurs += 1;
					if(erreurs > delta) return false;
				}
			i = index + 1;
		}
		return true;
	}
	
	
	
	
	/**
	 * Retourne les sous-ensembles de longueur k-1 de l'ensemble de sommets (de taille k)
	 * @return Liste de CoupleBitSet
	 */
	public ArrayList<CoupleBitSet> subVertexSet()
	{
		ArrayList<CoupleBitSet> resultat = new ArrayList<CoupleBitSet>();
		// un element de résultat correspond a l'itemset auquel on a enleve un item
		int i = 0;
		int index = -1;

		while(i <= this.vertexSet.size())
		{
			index = this.vertexSet.nextSetBit(i);
			if(index == -1) break;
			CoupleBitSet it = new CoupleBitSet((BitSet)this.vertexSet.clone()); // on copie l'itemset
			(it.getVertexes()).set(index, false); // on enlève l'item de l'itemset copié
			resultat.add(0,it);
			i = index + 1;
		}
		return resultat;
	}



	/**
	 * Affiche l'ensemble de sommets
	 * @param h Table de hachage contenant les noms des sommets
	 */
	public void displayVertexSet(Hashtable<Integer,String> h)
	{
		try
		{
			String s = ""; // chaine de caractères à afficher
			int i = 0;
			int index = -1;
			boolean premier = true;

			while(i <= this.vertexSet.size())
			{
				index = this.vertexSet.nextSetBit(i);
				if(index == -1) break;

				if(!premier) s = s+",";
				if(h != null) 
				{
					// on récupère le nom de l'item, et on l'ajoute à s
					s = s+(h.get(new Integer(index)));
				}
				else 
				{
					// si h n'existe pas, on ajoute la valeur de l'item (nombre) à s
					s = s+(index);
				}
				premier = false;

				i = index + 1;
			}

			System.out.print(s);
		}
		catch(Exception e)
		{
			System.out.println(e.getMessage()+"\n\nErreur lors de l'affichage de l'itemset");
		}
	}

	/**
	 * Affiche l'ensemble des hyperaretes 
	 */
	public void displayEdgeSet()
	{
		String s = "";
		int i = 0;
		int index = -1;
		boolean premier = true;

		while(i <= edgeSet.size())
		{
			index = edgeSet.nextSetBit(i);
			if(index == -1) break;

			if(!premier) s = s+",";

			s = s+(index);

			premier = false;

			i = index + 1;
		}

		System.out.print(s);
		//System.out.print("\n");
	}


	/**
	 * Affiche l'ensemble des sommets et l'ensemble des hyperaretes
	 * @param h Table de hachage contenant les noms des sommets
	 */
	public void displayAll(Hashtable<Integer,String> h)
	{
		try
		{
			String s = ""; // chaine de caractères à afficher
			int i = 0;
			int index = -1;
			boolean premier = true;

			while(i <= vertexSet.size())
			{
				index = vertexSet.nextSetBit(i);
				if(index == -1) break;

				if(!premier) s = s+",";
				if(h != null) 
				{
					// on récupère le nom de l'item, et on l'ajoute à s
					s = s+(h.get(new Integer(index)));
				}
				else 
				{
					// si h n'existe pas, on ajoute la valeur de l'item (nombre) à s
					s = s+(index);
				}
				premier = false;

				i = index + 1;
			}		

			System.out.print(s + " ; ");
			displayEdgeSet();
		}
		catch(Exception e)
		{
			System.out.println(e.getMessage()+"\n\nErreur lors de l'affichage du ferme");
		}
	}




	/**
	 * Enregistre l'ensemble des somemts et l'ensemble des hyperaretes dans un fichier (en remplaçant le numero de sommets par leur nom)
	 * @param fichierResultat Nom du fichier contenant les resultats
	 * @param h Table de hachage contenant les noms des sommets
	 */
	public void save(BufferedWriter fichierResultat, Hashtable<Integer,String> h)
	{
		try
		{
			String s = "";
			int i = 0;
			int index = -1;
			boolean premier = true;

			while(i <= this.vertexSet.size())
			{
				index = this.vertexSet.nextSetBit(i);
				if(index == -1) break;

				if(!premier) s = s+" ";
				if(h != null) 
				{
					// on récupère le nom de l'item, et on l'ajoute à s
					s = s+(h.get(new Integer(index)));
				}
				else 
				{
					// si h n'existe pas, on ajoute la valeur de l'item (nombre) à s
					s = s+(index);
				}
				premier = false;

				i = index + 1;
			}

//			i = 0;
//			index = -1;
//			premier = true;
//
//			while(i <= edgeSet.size())
//			{
//				index = edgeSet.nextSetBit(i);
//				if(index == -1) break;
//
//				if(!premier) s = s+" ";
//				s = s+(index);
//				premier = false;
//
//				i = index + 1;
//			}

			fichierResultat.write(s+" ");
			fichierResultat.write("\n");
		}
		catch(Exception e)
		{
			System.err.println(e.getMessage()+"\n\nErreur lors de l'écriture de l'itemset dans le fichier résultat");
		}
	}




	/**
	 * Remplissage du vertexSet entre deux indices
	 * @param from Indice inclu
	 * @param to Indice exclu
	 */
	public void remplirVertexSet(int from, int to) {
		this.vertexSet.set(from,to);
	}
	

	/**
	 * Affichage
	 * @param listcbs
	 */
	public static void afficheListCoupleBitSetVertex(ArrayList<CoupleBitSet> listcbs) {
		CoupleBitSet cbs = null;
		System.out.println("{");
		for(Iterator<CoupleBitSet> i = listcbs.iterator(); i.hasNext();) {
			cbs = (CoupleBitSet)i.next();
			cbs.displayVertexSet(null);
			System.out.print("\n");
		}
		System.out.println("}");
	}



	/**
	 * @param args
	 */
	public static void main(String[] args) {

		CoupleBitSet it1 = new CoupleBitSet();
		it1.addVertex(1);
		it1.addVertex(2);
		it1.addVertex(5);

		it1.addEdge(2);
		it1.addEdge(3);
		it1.addEdge(11);

		System.out.println("Itemset1 = ");
		it1.displayAll(null);
		System.out.println("\n");

		System.out.println("transactions de Itemset1 = ");
		it1.displayEdgeSet();
		System.out.println("\n");


		CoupleBitSet it2 = new CoupleBitSet();
		it2.addVertex(1);
		it2.addVertex(3);
		it2.addVertex(5);
		it2.addVertex(10);

		it2.addEdge(3);
		it2.addEdge(11);
		it2.addEdge(9);

		System.out.println("Itemset2 = ");
		it2.displayAll(null);
		System.out.println("\n");



		System.out.println("2 appartient à itemset1 ? "+it1.belongsVertexSet(2)+ "\n3 appartient à itemset1 ? "+it1.belongsVertexSet(3));

		System.out.println("\nintersection = ");
		new CoupleBitSet(it1.intersectionVertexSet(it2)).displayAll(null);

		System.out.println("\n"+it1.intersectionVertexSet(it2).toString()+"\n");
		
		System.out.println("\nunion = ");
		new CoupleBitSet(it1.unionVertexSet(it2)).displayAll(null);


		System.out.println("\n\nItemset1 inclus dans Itemset2 ? "+it1.includedVertexSet(it2.getVertexes()));


		CoupleBitSet it3 = new CoupleBitSet();
		it3.addVertex(3);
		it3.addVertex(5);
		it3.addVertex(10);

		it3.addEdge(3);
		it3.addEdge(11);
		it3.addEdge(9);
		it3.addEdge(4);

		System.out.println("Itemset3 = ");
		it3.displayAll(null);
		System.out.println("\n");

		System.out.println("\nItemset3 inclus dans Itemset2 ? "+it3.includedVertexSet(it2.getVertexes()));

		System.out.println("\nItemset1 egal a Itemset2 ? "+it1.equalsVertexSet(it2.getVertexes()));

		it3.addVertex(1);
		System.out.println("\nItemset3 = ");
		it3.displayAll(null);

		System.out.println("\nItemset2 egal a Itemset3 ? "+it2.equalsVertexSet(it3.getVertexes()));


		System.out.println("\nItemset2 moins Itemset1 = ");
		it2.minusVertexes(it1);
		it2.displayAll(null);
		System.out.print("\n");


		System.out.print("\n(k-1)sous-ensembles de Itemset1 (");
		it1.displayVertexSet(null);
		System.out.print(") = \n");
		ArrayList<CoupleBitSet> liste = it1.subVertexSet();
		CoupleBitSet itemset;
		for(Iterator<CoupleBitSet> i = liste.iterator(); i.hasNext();)
		{
			itemset = (CoupleBitSet) i.next();
			itemset.displayVertexSet(null);
			System.out.print("\n");

		}


		System.out.println("\n\nItemset3 = ");
		it3.displayAll(null);
		System.out.println("\n");
		
		CoupleBitSet it4 = new CoupleBitSet();
		it4.addVertex(3);
		it4.addVertex(5);
		it4.addVertex(6);
		it4.addVertex(10);
		it4.addVertex(11);
		
		System.out.println("\nItemset4 = ");
		it4.displayAll(null);
		System.out.println("\n");
		
		System.out.println("\nItemset4 inclus dans Itemset3 ? "+it4.includedVertexSet(it3.getVertexes()));
	
		System.out.println("\nItemset4 inclus dans Itemset3 a 1 pres? "+it4.includedVertexSet(it3.getVertexes(),1));
		
		System.out.println("\nItemset4 inclus dans Itemset3 a 2 pres? "+it4.includedVertexSet(it3.getVertexes(),2));
		
	}

	



}
