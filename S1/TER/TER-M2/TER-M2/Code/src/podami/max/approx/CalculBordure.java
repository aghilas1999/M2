package podami.max.approx;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.Iterator;
import java.util.StringTokenizer;

import podami.common.CoupleBitSet;
import podami.hypergraph.berge.Berge;
import podami.hypergraph.dl.DL;
import podami.hypergraph.mtminer.MTminerDelta;
import podami.hypergraph.reduction.HR;
import podami.hypergraph.staccato.Staccato2;


/**
 * <p>Calcul de bordures par dualisation et approximation (calcul de transversaux minimaux approchees d'un hypergraphe)</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Universite d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class CalculBordure {

	/**
	 * Nombre d'items
	 */
	private int nbItems;

	/**
	 * Nombre de transactions
	 */
	private int nbTrans;

	/**
	 * Type de bordure a calculer ("pos" ou "neg") 
	 */
	private String type;

	/**
	 * Nom du fichier contenant les donnees
	 */
	private String fichierDonnees;

	/**
	 * Donnees (ensemble de transactions)
	 */
	private ArrayList<CoupleBitSet> donnees;

	/**
	 * Bordure resultat
	 */
	private ArrayList<CoupleBitSet> bordureCalculee;

	/**
	 * Nom de l'algorithme utilise pour calculer les transversaux minimaux
	 */
	private String algo;

	/**
	 * Nombre d'exceptions tolerees (pour algo MTMiner)
	 */
	private int delta;

	/**
	 * 
	 */
	private double lambda;

	/**
	 * 
	 */
	private int minsup;


	private boolean affichage;



	/**
	 * Constructeur 
	 * @param nomFichier Nom du fichier contenant les donnees
	 * @param type
	 * @param algo
	 * @param delta
	 */
	public CalculBordure(String nomFichier, String type, String algo, int delta, double lambda, int minsup) {
		this.fichierDonnees = nomFichier;
		this.nbItems = 0;
		this.nbItems = 0;
		this.type = type;
		this.algo = algo;
		this.delta = delta;
		this.lambda = lambda;
		this.minsup = minsup;
		this.donnees = new ArrayList<CoupleBitSet>();
		this.bordureCalculee = new ArrayList<CoupleBitSet>();
		this.affichage = false;
		//this.affichage = true;

		this.chargementDonnees();
	}



	/**
	 * Chargement des donnees (la bordure positive ou la bordure negative)
	 */
	public void chargementDonnees() {
		BufferedReader br;
		StringTokenizer st;
		String ligne = "";
		String item = ""; // numero de l'item lu
		int p = 0; // numero de la transaction lue
		int numitem;
		boolean fini = false;

		try {						
			br = new BufferedReader(new FileReader(this.fichierDonnees));
			p = 0;
			CoupleBitSet itemset = null;

			while(br.ready())
			{
				p++; // numero hyperarete (= numero de la ligne lue)
				item = "";
				ligne = br.readLine();
				st = new StringTokenizer(ligne, " \t\n\r");
				if(ligne.startsWith("#")==false) {
					itemset = new CoupleBitSet(); // l'hyperarete en cours de lecture
					fini = false;
					while(st.hasMoreTokens() && !fini)
					{
						item = st.nextToken();
						if(item.startsWith("(")==false) { // pour compatibilite avec sortie IBE et FPmax*
							if(item.startsWith("#")==false) {  // pour compatibilite avec sortie SPMF
							numitem = Integer.parseInt(item);
							if(numitem > this.nbItems) this.nbItems = numitem;
							itemset.addVertex(Integer.parseInt(item));
							}
							else
								fini = true;
						}
					}
					donnees.add(itemset);
				}
			}
			br.close();

			this.nbTrans = p;


			if(affichage) {
				System.out.println("\nDonnees ("+this.nbTrans+" transactions, "+this.nbItems+" items) ");
				//afficheListCoupleBitSetVertex(this.donnees);
				//System.out.print("\n");
			}
		}
		catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} 
	}




	/**
	 * 
	 */
	public void calculBordure() {
		if(this.type.equals("pos"))
			this.calculBordurePositive();
		else if(this.type.equals("neg"))
			this.calculBordureNegative();
		else System.out.println("Type non reconnu");
	}







	/**
	 * Calcul exact ou approche de transversaux minimaux d'un hypergraphe
	 * @param hyper
	 * @return
	 */
	public ArrayList<CoupleBitSet> calculTrMin(ArrayList<CoupleBitSet> hyper) {

		ArrayList<CoupleBitSet> mintr = null;
	
		System.err.println(this.fichierDonnees+" "+this.algo+" "+this.minsup);

		long START = 0;
		long END = 0;
		double tempsexecution = 0;
		
		switch (this.algo) {
		case "berge": // Algo de Berge
			START = 0;
			END = 0;
			Berge algoBerge = new Berge("");
			START = System.currentTimeMillis();
			mintr = algoBerge.berge(hyper);
			END = System.currentTimeMillis();
			tempsexecution = END - START;
			System.err.println("berge= "+tempsexecution+" ms");
			break;
		case "dl": // Algo de Dong & Li (BorderDiff)
			START = 0;
			END = 0;
			DL algoDL = new DL();
			START = System.currentTimeMillis();
			algoDL.dl(hyper, false);
			END = System.currentTimeMillis();
			tempsexecution = END - START;
			System.err.println("dl= "+tempsexecution+" ms");
			mintr = algoDL.getMintr();
			break;
		case "mt": // Algo MTminer
			START = 0;
			END = 0;
			MTminerDelta mt = new MTminerDelta("", this.delta, (int)this.lambda);
			START = System.currentTimeMillis();
			mintr = mt.mtminer(hyper, this.delta, (int)this.lambda);
			END = System.currentTimeMillis();
			tempsexecution = END - START;
			System.err.println("mt= "+tempsexecution+" ms");
			break;
		case "sta": // Algo Staccato
			START = 0;
			END = 0;
			int L = Integer.MAX_VALUE;
			Staccato2 sta = new Staccato2(L, this.lambda, this.delta);
			sta.chargeDonnees(hyper);
			START = System.currentTimeMillis();
			mintr = sta.staccato2(sta.hyper);
			END = System.currentTimeMillis();
			tempsexecution = END - START;
			System.err.println("staccato= "+tempsexecution+" ms");
			break;
		case "red": // Algo AMTHR
			START = 0;
			END = 0;
			HR sp = new HR();
			//sp.setCalculMin(false);
			sp.setCalculMin(true);
			sp.hyper = hyper;
			START = System.currentTimeMillis();
			sp.computeReduction();
			END = System.currentTimeMillis();
			double tempsreduction = END - START;
			System.err.println("reduction= "+tempsreduction+" ms");		
			System.err.println("hypergraphe= "+sp.nbSommets+" sommets ; "+sp.nbHyperaretes+" hyperaretes");
			System.err.println("hypreduit= "+sp.nbSommetsReduc+" sommets ; "+sp.nbHyperaretesReduc+" hyperaretes");
			System.err.println("hypreduit est min ? "+sp.getCalculMin());
			
			ArrayList<CoupleBitSet> hyperreduit = sp.hyperReduit;
			sp = null;
			START = 0;
			END = 0;
			DL algoDL2 = new DL(); //TODO utilisation de DL mais peut etre un autre algo plus efficace de calcul exact tr min
			START = System.currentTimeMillis();
			algoDL2.dl(hyperreduit, false);
			END = System.currentTimeMillis();
			double tempsreddl = END - START;
			System.err.println("dlReduc= "+tempsreddl+" ms");
			mintr = algoDL2.getMintr();
			System.err.println("REDetDL= "+(tempsreduction+tempsreddl)+" ms");
			break;
		default: 
			System.out.println("Algorithme inconnu");
			break;
		}
		//TODO ajouter autres algorithmes : genetique, partiel, ...
				
		return mintr;
	}





	/**
	 * Calcul de la bordure positive a partir de la bordure negative.
	 * Bd+(S) = complement(MinTr(Bd-(S)))
	 */
	public void calculBordurePositive() {

		if(this.affichage) {
			System.out.println("Bordure negative =");
			afficheListCoupleBitSetVertex(this.donnees);
		}

		//calcul des transversaux minimaux de l'hypergraphe "donnees"
		if(this.affichage) 	System.out.println("Calcul des tr min avec "+this.algo);

		ArrayList<CoupleBitSet> mintr = this.calculTrMin(this.donnees);

		if(this.affichage) {
			System.out.println("\ntransversaux minimaux :");
			afficheListCoupleBitSetVertex(mintr);
		}

		// calcul des complementaires des tr min trouvees
		if(this.affichage) System.out.println("Calcul des complementaires");

		this.bordureCalculee = complements(mintr);

		if(this.affichage) {
			System.out.println("\nbordure positive :");
			afficheListCoupleBitSetVertex(this.bordureCalculee);
		}
	}




	/**
	 * Calcul de la bordure negative a partir de la bordure positive.
	 * Bd-(S) = MinTr(complement(Bd+(S)))
	 */
	public void calculBordureNegative() {

		// calcul des complementaires de la bordure positive
		if(this.affichage) System.out.println("Calcul des complementaires");

		ArrayList<CoupleBitSet> lescomplem = complements(this.donnees);

		if(this.affichage) {
			System.out.println("\ncomplements de la bordure positive :");
			afficheListCoupleBitSetVertex(lescomplem);
		}

		//calcul des transversaux minimaux de l'hypergraphe "lescomplem"
		if(this.affichage) 	System.out.println("Calcul des tr min avec "+this.algo);

		ArrayList<CoupleBitSet> mintr = this.calculTrMin(lescomplem);

		this.bordureCalculee = mintr;

		if(this.affichage) {
			System.out.println("\nbordure negative :");
			afficheListCoupleBitSetVertex(this.bordureCalculee);
		}
	}




	/**
	 * Calcul de la liste des complementaires
	 * @param listeC
	 * @return
	 */
	public ArrayList<CoupleBitSet> complements(ArrayList<CoupleBitSet> listeC) {
		ArrayList<CoupleBitSet> complem = new ArrayList<CoupleBitSet>();

		if(listeC.isEmpty()) {
			//si listeC est vide, alors un seul element (motif complet i.e. ayant tous les items)
			CoupleBitSet cbs = new CoupleBitSet();
			cbs.remplirVertexSet(1, this.nbItems + 1);
			complem.add(cbs);
		}
		else
		{
			// cas general, pour chaque element de listeC, calcul du complementaire (sur nbItems)
			CoupleBitSet compl;
			for(CoupleBitSet c : listeC) {
				compl = new CoupleBitSet((BitSet) c.vertexSet.clone()); 
				compl.vertexSet.flip(1, this.nbItems + 1);
				complem.add(compl);
			}
		}

		return complem;
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
		System.out.println("}");
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
	 * @param bw
	 * @throws IOException
	 */
	public void save(BufferedWriter bw, ArrayList<CoupleBitSet> liste) throws IOException {
		CoupleBitSet cbs = null;
		for(Iterator<CoupleBitSet> i = liste.iterator(); i.hasNext();) {
			cbs = (CoupleBitSet)i.next();
			cbs.save(bw, null);
		}
	}





	/**
	 * Chargement des donnees (la bordure positive ou la bordure negative)
	 */
	public void chargementDonnees(String nomFichierEntree, ArrayList<CoupleBitSet> ensemble) {
		BufferedReader br;
		StringTokenizer st;
		String ligne = "";
		String item = "";
		boolean fini = false;
		
		try {						
			br = new BufferedReader(new FileReader(nomFichierEntree));
			CoupleBitSet itemset = null;

			while(br.ready())
			{
				item = "";
				ligne = br.readLine();
				st = new StringTokenizer(ligne, " \t\n\r");
				if(ligne.startsWith("#")==false) {
					fini = false;
					itemset = new CoupleBitSet(); // l'hyperarete en cours de lecture
					while(st.hasMoreTokens() && !fini)
					{
						item = st.nextToken();
						if(item.startsWith("(")==false) {// pour compatibilite avec sortie IBE et FPmax*
							if(item.startsWith("#")==false) {  // pour compatibilite avec sortie SPMF	
							 itemset.addVertex(Integer.parseInt(item));
							}
							else
								fini = true;
						}
					}
					ensemble.add(itemset);
				}
			}
			br.close();

			if(affichage) {
				System.out.println("\nDonnees chargees :");
				afficheListCoupleBitSetVertex(ensemble);
				System.out.print("\n");
			}
		}
		catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} 
	}



	/**
	 * Calcul de stats sur une bordure (ensemble de motifs)
	 * @param bordure
	 */
	public Stats calculStats(ArrayList<CoupleBitSet> bordure) {
		Stats s = new Stats();
		s.nbMotifs = bordure.size();
		int nbi = 0;
		double totaltaille = 0;
		for(CoupleBitSet cbs : bordure) {
			nbi = cbs.getNbVertexes(); // nombre d'items
			if(nbi > s.tailleMax) s.tailleMax = nbi;
			if(nbi < s.tailleMin) s.tailleMin = nbi;
			totaltaille = totaltaille + nbi;
		}
		s.tailleMoy = totaltaille / s.nbMotifs;	
		return s;
	}




//	/**
//	 * Distance entre deux motifs
//	 * @param e1 Un motif
//	 * @param ee Un autre motif
//	 * @param type Type de distance
//	 * @return distance entre e1 et e2
//	 */
//	public double distance(CoupleBitSet e, CoupleBitSet ee, String type) {
//		double distance = Double.MAX_VALUE;
//
//		double te = e.getNbVertexes();
//		double tee = ee.getNbVertexes();
//
//		CoupleBitSet inter = new CoupleBitSet(e.intersectionVertexSet(ee));
//		double tinter = inter.getNbVertexes();
//
//		CoupleBitSet union = new CoupleBitSet(e.unionVertexSet(ee));
//		double tunion = union.getNbVertexes();
//		//union.minusVertexes(inter); // difference symetrique
//		//double tdiffsym = union.getNbVertexes();
//
//		double min = -1;
//		if(te <= tee) min = te;
//		else min = tee;
//
//		if(type.equals("jaccard"))
//			distance = 1 - (tinter / tunion);
//		else if(type.equals("dice"))
//			distance = 1 - ((2*tinter) / (te + tee));
//		else if(type.equals("cosine")) // aussi appele "ochiai"
//			distance = 1 - (tinter / (java.lang.Math.sqrt(te * tee)));
//		else if(type.equals("tanimoto"))
//			distance = 1 - (tinter / (te + tee - tinter));
//		else if(type.equals("overlap"))
//			distance = 1 - (tinter / min);
//		//distance = 1 - (tdiffsym / tunion);
//
//		return distance;
//	}




//	/**
//	 * Distance entre deux ensembles de motifs (distance basee sur la distance de Hausdorff)
//	 * @param reel
//	 * @param calcule
//	 * @return
//	 */
//	public double distance(ArrayList<CoupleBitSet> reel, ArrayList<CoupleBitSet> calcule, String type) {
//		double d = 0;
//
//		double max1 = 0;
//		for(CoupleBitSet e : reel) {
//			double min1 = Double.MAX_VALUE;
//			double distance = Double.MAX_VALUE;
//			for(CoupleBitSet ee : calcule) {				
//				//distance entre e et ee
//				distance = distance(e,ee,type);				
//				if(distance < min1) min1 = distance;
//			}
//			if(min1 > max1) max1 = min1;
//		}
//
//		double max2 = 0;
//		for(CoupleBitSet e1 : calcule) {
//			double min2 = Double.MAX_VALUE;
//			double distance = Double.MAX_VALUE;
//			for(CoupleBitSet ee1 : reel) {
//				//distance entre e1 et ee1
//				distance = distance(e1,ee1,type);				
//				if(distance < min2) min2 = distance;
//			}
//			if(min2 > max2) max2 = min2;
//		}
//
//		if(max1 > max2) d = max1;
//		else if(max2 > max1) d = max2;
//		else d = max1;//cas max1==max2
//
//		//		double moyenne = (max1+max2) / 2;
//		//		d = moyenne;
//
//		return d;
//	}






	/**
	 * @param args
	 */
	public static void main(String[] args) {	

		if(args.length<7)
			System.out.println("Usage : CalculBordure fichier_donnees type_bordure_sortie algo_trmin_utilise delta fichier_resultat_reel minsupport lambda\n");
		else
		{	
			long START = 0;
			long END = 0;
			String type = args[1];
			String algo = args[2];
			int delta = Integer.parseInt(args[3]);

			String nomfichierbordurereelle = args[4];
			int minsup = Integer.parseInt(args[5]);

			double lambda = Double.parseDouble(args[6]);

			CalculBordure cb = new CalculBordure(args[0], type, algo, delta, lambda, minsup);

			START = System.currentTimeMillis();
			cb.calculBordure();
			END = System.currentTimeMillis();
			double tempsexecution = END - START;
			//System.out.println(tempsexecution+" ms");

			//long temps = System.currentTimeMillis();

			// stats sur la bordure calculee
			Stats s = cb.calculStats(cb.bordureCalculee);
			//System.out.println("\nStats bordure calculee : \n"+s);

			// stats sur la bordure reelle
			ArrayList<CoupleBitSet> bordureReelle = new ArrayList<CoupleBitSet> ();
			cb.chargementDonnees(nomfichierbordurereelle, bordureReelle);
			//Stats s2 = cb.calculStats(bordureReelle);
			//System.out.println("\nStats bordure reelle : \n"+s2);

			// distance de Hausdorff entre la bordure calculee et la bordure reelle
			//double distance1 = -1; //cb.distance(cb.bordureCalculee, bordureReelle, "jaccard");
			//System.out.println("\nDistance jaccard = \n"+distance1);
			//double distance2 = -1; //cb.distance(cb.bordureCalculee, bordureReelle, "dice");
			//System.out.println("\nDistance2 dice = \n"+distance2);
			
			double distance3 = DistanceBordures.distance(cb.bordureCalculee, bordureReelle, "cosine");
			//System.out.println("\nDistance3 cosine = \n"+distance3);
			
			//double distance4 = -1; //cb.distance(cb.bordureCalculee, bordureReelle, "tanimoto");
			//System.out.println("\nDistance4 tanimoto = \n"+distance4);
			//double distance5 = -1; //cb.distance(cb.bordureCalculee, bordureReelle, "overlap");
			//System.out.println("\nDistance5 overlap = \n"+distance5);

			System.out.println(cb.minsup+" "+tempsexecution+" "+distance3+" "+s.nbMotifs+" "+s.tailleMoy+" "+s.tailleMin+" "+s.tailleMax);
			
			try {
				String fsortie = cb.fichierDonnees+"."+algo;
				//if(algo.equals("approxalea")) fsortie+="."+temps;
				if(algo.equals("mt")) fsortie+="."+cb.delta+"."+((int)cb.lambda);
				if(algo.equals("sta")) fsortie+=".l"+(cb.lambda)+".d"+cb.delta;
				fsortie += "."+type+".cb";
				BufferedWriter bw = new BufferedWriter(new FileWriter(fsortie));
				bw.write("# "+tempsexecution+" ms\n");
				bw.write("# "+s+"\n");
				bw.write("# distance= "+distance3+"\n");
				cb.save(bw, cb.bordureCalculee);
				bw.close();
			} catch (IOException e) {
				e.printStackTrace();
			}

		}

	}




}
