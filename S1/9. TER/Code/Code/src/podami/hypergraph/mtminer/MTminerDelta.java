package podami.hypergraph.mtminer;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.StringTokenizer;

import podami.common.CoupleBitSet;


// delta exceptions

/**
 * <p>Implémentation de l'algorithme MTminer de Céline Hébert (http://users.info.unicaen.fr/~chebert/)</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Université d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class MTminerDelta {

	/**
	 * Nom du fichier contenant les donnees (l'hypergraphe)
	 */
	private String fichierDonnees;

	/**
	 * Delta
	 */
	private int delta;
	
	/**
	 * Lambda
	 */
	private int lambda;

	/**
	 * Nombre de sommets de l'hypergraphe
	 */
	private int nbSommets;

	/**
	 * Ensemble des transversaux minimaux
	 */
	private ArrayList<CoupleBitSet> mintr;

	/**
	 * 
	 */
	private boolean affichage;


	/**
	 * Constructeur
	 * @param nomFichier Nom du fichier contenant les donnees (i.e. l'hypergraphe)
	 */
	public MTminerDelta(String nomFichier, int delt, int lamb) {
		this.fichierDonnees = nomFichier;
		this.nbSommets = 0;
		this.delta = delt;
		this.lambda = lamb;
		this.mintr = new ArrayList<CoupleBitSet>();
		this.affichage = false;
	}

		
	/**
	 * Recuperation de la liste des transversaux minimaux
	 * @return mintr
	 */
	public ArrayList<CoupleBitSet> getMintr() {
		return this.mintr;
	}
	
	
	
	
	/**
	 * MTminer
	 */
	public void mtminer() {
		BufferedReader br;
		StringTokenizer st;
		String ligne = "";
		String sommet = ""; // numero du sommet lu
		int p = 0; // numero de l'hyperarete lu
		Integer n = 0;
		int numsommet;


		try {
			br = new BufferedReader(new FileReader(this.fichierDonnees));			

			// calcul du nombre de sommets et d'hyperaretes
			while(br.ready())
			{
				p++;
				sommet = "";
				ligne = br.readLine();
				if(ligne.startsWith("#")==false) {
					st = new StringTokenizer(ligne, " \t\n\r"); 
					while(st.hasMoreTokens())
					{
						sommet = st.nextToken();
						numsommet = Integer.parseInt(sommet);
						if(numsommet > this.nbSommets) this.nbSommets = numsommet;
					}
				}
			}
			br.close();

			if(affichage) {
				System.out.println(this.nbSommets+" sommets et "+(int)p+" hyperaretes");
				System.out.println("delta= "+this.delta);
			}

			Hashtable<Integer,CoupleBitSet> h = new Hashtable<Integer,CoupleBitSet>();

			// pour chaque sommet v, creer un cbs et l'ajouter dans h
			for(int v=1; v<=this.nbSommets; v++)
			{
				CoupleBitSet cbs = new CoupleBitSet();
				cbs.addVertex(v);
				h.put(new Integer(v),cbs);
			}


			br = new BufferedReader(new FileReader(this.fichierDonnees));
			p = 0;
			n = 0;

			while(br.ready())
			{
				p++;
				sommet = "";
				ligne = br.readLine();
				if(ligne.startsWith("#")==false) {
					st = new StringTokenizer(ligne, " \t\n\r");
					CoupleBitSet hyperarete = new CoupleBitSet(); 
					while(st.hasMoreTokens())
					{
						sommet = st.nextToken();
						hyperarete.addVertex(Integer.parseInt(sommet));
					}
					// calcul de l'extension de chaque sommet
					// pour chaque sommet, test si absent de l'hyperarete courante
					for(Enumeration<Integer> e = h.keys(); e.hasMoreElements(); )
					{
						n = (Integer)e.nextElement();
						if(hyperarete.belongsVertexSet(n.intValue()) == false) {
							// ajouter l'hyperarete p dans le edgeSet du couplebitset de v
							h.get(n).addEdge(p);
						}						
					}
				}
			}
			br.close();


			CoupleBitSet cbs = null;
			ArbreHachageMT gen = new ArbreHachageMT(); // les generateurs

			// Initialisation de MT et de Gen1
			for(Enumeration<Integer> e = h.keys(); e.hasMoreElements(); )
			{
				n = (Integer)e.nextElement();
				cbs = h.get(n);
				//				if(cbs.getNbEdges() >= this.minsupp && cbs.getNbEdges() < (this.nbHyperaretes-delta)) {
				//					freeSet.add(cbs);
				//					if(cbs.getNbEdges() > (this.minsupp + this.delta)) gen.ajoute(cbs);
				//				}
				//TODO
				//if(cbs.getNbEdges() == 0) mintr.add(cbs);
				if(cbs.getNbEdges() <= this.delta) mintr.add(cbs);
				else gen.ajoute(cbs);
			}

			//h = null; // la tble de hachage devient inutile

			//System.out.println("MT initial = ");
			//afficheListCoupleBitSetAll(this.mintr);

			//System.out.println("\nGen1 = ");
			//gen.affiche(null);


			//			BufferedWriter bw = new BufferedWriter(new FileWriter(this.fichierDonnees+"_"+this.delta+".tr"));
			int k = 1;
			ArbreHachageMT genk = null;
			//ArbreHachage temp = null;

			//			bw.write("#delta="+this.delta+"\n");
			//			bw.flush();

			// BOUCLE
			while(gen.estVide() == false) // tant qu'il y a des generateurs
			{
				if(affichage) System.out.println("k="+k);

				genk = new ArbreHachageMT();

				// generation des candidats et calcul des extensions
				gen.fusion(k, this.mintr, gen, genk, this.delta, this.lambda); //TODO

				//System.out.println("\nGen = ("+listcbs.size()+" candidats)");
				//afficheListCoupleBitSetAll(listcbs);

				//				saveMinimalTransversals(bw); // save ici ou a la fin
				//				bw.flush();

				//System.out.println("MT = ");
				//afficheListCoupleBitSetVertex(this.mintr);

				//this.mintr = new ArrayList<CoupleBitSet>();

				//temp = gen;
				gen = genk;
				//temp = null;
				k = k + 1;
			}	

			//			bw.close();
			if(affichage) System.out.println("Fin.");
		}
		catch (FileNotFoundException e) {
			e.printStackTrace();
		} 
		catch (NumberFormatException e) {
			e.printStackTrace();
		} 
		catch (IOException e) {
			e.printStackTrace();
		}
	}


	/**
	 * 
	 * @param listcbs
	 */
	public void afficheListCoupleBitSetAll(ArrayList<CoupleBitSet> listcbs) {
		CoupleBitSet cbs = null;
		System.out.println("{");
		for(Iterator<CoupleBitSet> i = listcbs.iterator(); i.hasNext();) {
			cbs = (CoupleBitSet)i.next();
			cbs.displayAll(null);
			System.out.print("\n");
		}
		System.out.println("}\n");
	}

	/**
	 * 
	 * @param listcbs
	 */
	public void afficheListCoupleBitSetVertex(ArrayList<CoupleBitSet> listcbs) {
		CoupleBitSet cbs = null;
		System.out.println("{");
		for(Iterator<CoupleBitSet> i = listcbs.iterator(); i.hasNext();) {
			cbs = (CoupleBitSet)i.next();
			cbs.displayVertexSet(null);
			System.out.print("\n");
		}
		System.out.println("}\n");
	}
	

	

	/**
	 * 
	 * @param bw
	 * @throws IOException
	 */
	public void saveMinimalTransversals(BufferedWriter bw) throws IOException {
		CoupleBitSet cbs = null;
		for(Iterator<CoupleBitSet> i = this.mintr.iterator(); i.hasNext();) {
			cbs = (CoupleBitSet)i.next();
			cbs.save(bw, null);
		}
	}


	/**
	 * 
	 * @param nomFichier
	 * @param delta
	 * @param lambda
	 */
	public static void doJob(String nomFichier, int delta, int lambda) {
		long START = 0;
		long END = 0;
		MTminerDelta mt = new MTminerDelta(nomFichier, delta, lambda);
		START = System.currentTimeMillis();
		mt.mtminer();
		END = System.currentTimeMillis();
		double tempsexecution = END - START;
		System.out.print(tempsexecution+" ms");

		try {
			BufferedWriter bw = new BufferedWriter(new FileWriter(mt.fichierDonnees+"_"+mt.delta+"_"+mt.lambda+".tr"));
			bw.write("#delta="+mt.delta+"  lambda="+mt.lambda+"  "+tempsexecution+" ms\n");
			bw.flush();
			mt.saveMinimalTransversals(bw);
			bw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if(args.length<3)
			System.out.println("Usage : MTminer fichier_hypergraphe delta lambda\n");
		else
		{	
			doJob(args[0], Integer.parseInt(args[1]), Integer.parseInt(args[2]));
		}
	}

	
	
	
	
	
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	/**
	 * Algo MTMiner avec possibles delta erreurs (avec motifs lambda-libres).
	 * @param 
	 * @return
	 */
	public ArrayList<CoupleBitSet> mtminer(ArrayList<CoupleBitSet> leshyperaretes, int delta, int lambda) {
		ArrayList<CoupleBitSet> mintr = new ArrayList<CoupleBitSet>();
		ArrayList<CoupleBitSet> gen0 = new ArrayList<CoupleBitSet>();
		
		//compter le nombre de sommets de l'hypergraphe
		BitSet b = new BitSet();
		for(CoupleBitSet cb : leshyperaretes) {
			b.or(cb.getVertexes());
		}
		this.nbSommets = b.length() - 1; //TODO
		
		if(this.affichage) System.out.println("NbSommets= "+this.nbSommets);
		
		
		// pour chaque sommet v, creer un cbs et l'ajouter dans h
		for(int v=1; v<=this.nbSommets; v++)
		{
			CoupleBitSet cbs = new CoupleBitSet();
			cbs.addVertex(v);
			gen0.add(cbs);
			//h.put(new Integer(v),cbs);
		}

		// parcours des hyperaretes pour determiner les anti-supports
		int numTrans = 0;
		for(CoupleBitSet cbsdata : leshyperaretes) {
			numTrans++;
			for(CoupleBitSet cbs : gen0) {
				if(cbs.includedVertexSet(cbsdata.vertexSet) == false) {
					cbs.addEdge(numTrans);
				}
			}
		}


		if(affichage) {
			System.out.println("\nMTMINER\ngen0 :");
			this.afficheListCoupleBitSetAll(gen0);
		}


		//CoupleBitSet cbs = null;
		ArbreHachageMT gen = new ArbreHachageMT(); // les generateurs

		// Initialisation de MT et de Gen1
		//for(Enumeration<Integer> e = h.keys(); e.hasMoreElements(); )
		for(CoupleBitSet cbs0 : gen0)
		{
			//n = (Integer)e.nextElement();
			//cbs = h.get(n);
			//				if(cbs.getNbEdges() >= this.minsupp && cbs.getNbEdges() < (this.nbHyperaretes-delta)) {
			//					freeSet.add(cbs);
			//					if(cbs.getNbEdges() > (this.minsupp + this.delta)) gen.ajoute(cbs);
			//				}
			//if(cbs.getNbEdges() == 0) mintr.add(cbs);
			if(cbs0.getNbEdges() <= delta) mintr.add(cbs0);
			else gen.ajoute(cbs0);
		}

		gen0 = null;
		
		//h = null; // la tble de hachage devient inutile

		//System.out.println("MT initial = ");
		//afficheListCoupleBitSetAll(this.mintr);

		//System.out.println("\nGen1 = ");
		//gen.affiche(null);


		//			BufferedWriter bw = new BufferedWriter(new FileWriter(this.fichierDonnees+"_"+this.delta+".tr"));
		int k = 1;
		ArbreHachageMT genk = null;
		//ArbreHachageMT temp = null;

		//			bw.write("#delta="+this.delta+"\n");
		//			bw.flush();

		// BOUCLE
		while(gen.estVide() == false) // tant qu'il y a des generateurs
		{
			if(affichage) System.out.println("k="+k);

			genk = new ArbreHachageMT();

			// generation des candidats et calcul des extensions
			gen.fusion(k, mintr, gen, genk, delta, lambda);

			if(this.affichage) {
				System.out.println("\nMintr actuelles = ");
				this.afficheListCoupleBitSetAll(mintr);
			}

			//System.out.println("MT = ");
			//afficheListCoupleBitSetVertex(this.mintr);

			//this.mintr = new ArrayList<CoupleBitSetMT>();
			
			//temp = gen;
			gen = genk;
			//temp = null;
			k = k + 1;
		}	

		//			bw.close();
		if(affichage) System.out.println("Fin.");

		this.mintr = mintr;
		
		return mintr;
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
}
