package podami.max.approx;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.StringTokenizer;

import podami.common.CoupleBitSet;



/**
 * <p>Calcul de la distance entre deux bordures (ensembles de motifs)</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Université d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class DistanceBordures {



	/**
	 * 
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



	//	/**
	//	 * 
	//	 * @param bw
	//	 * @throws IOException
	//	 */
	//	public void save(BufferedWriter bw, ArrayList<CoupleBitSet> liste) throws IOException {
	//		CoupleBitSet cbs = null;
	//		for(Iterator<CoupleBitSet> i = liste.iterator(); i.hasNext();) {
	//			cbs = (CoupleBitSet)i.next();
	//			cbs.save(bw, null);
	//		}
	//	}





	/**
	 * Chargement des donnees (la bordure positive ou la bordure negative)
	 */
	public static void chargementDonnees(String nomFichierEntrre, ArrayList<CoupleBitSet> ensemble) {
		BufferedReader br;
		StringTokenizer st;
		String ligne = "";
		String item = "";
		boolean fini = false;
		
		try {						
			br = new BufferedReader(new FileReader(nomFichierEntrre));
			CoupleBitSet itemset = null;

			while(br.ready())
			{
				item = "";
				ligne = br.readLine();
				if(ligne.trim().equals("") == false) {
					if(ligne.startsWith("#")==false) {
						st = new StringTokenizer(ligne, " \t\n\r");
						itemset = new CoupleBitSet(); // l'hyperarete en cours de lecture
						fini = false;
						while(st.hasMoreTokens() && !fini)
						{
							item = st.nextToken();
							if(item.startsWith("(")==false) { // pour compatibilite avec sortie IBE et FPmax*
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
			}
			br.close();

			//			if(affichage) {
			//				System.out.println("\nDonnees chargees :");
			//				afficheListCoupleBitSetVertex(ensemble);
			//				System.out.print("\n");
			//			}
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
	public static Stats calculStats(ArrayList<CoupleBitSet> bordure) {
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




	/**
	 * Distance entre deux motifs
	 * @param e1 Un motif
	 * @param ee Un autre motif
	 * @param type Type de distance
	 * @return distance entre e1 et e2
	 */
	public static double distance(CoupleBitSet e, CoupleBitSet ee, String type) {
		double distance = Double.MAX_VALUE;

		double te = e.getNbVertexes();
		double tee = ee.getNbVertexes();

		CoupleBitSet inter = new CoupleBitSet(e.intersectionVertexSet(ee));
		double tinter = inter.getNbVertexes();

		CoupleBitSet union = new CoupleBitSet(e.unionVertexSet(ee));
		double tunion = union.getNbVertexes();
		//union.minusVertexes(inter); // difference symetrique
		//double tdiffsym = union.getNbVertexes();

		double min = -1;
		if(te <= tee) min = te;
		else min = tee;

		if(type.equals("jaccard"))
			distance = 1 - (tinter / tunion);
		else if(type.equals("dice"))
			distance = 1 - ((2*tinter) / (te + tee));
		else if(type.equals("cosine")) // aussi appele "ochiai"
			distance = 1 - (tinter / (java.lang.Math.sqrt(te * tee)));
		else if(type.equals("tanimoto"))
			distance = 1 - (tinter / (te + tee - tinter));
		else if(type.equals("overlap"))
			distance = 1 - (tinter / min);
		//distance = 1 - (tdiffsym / tunion);

		return distance;
	}



	/**
	 * Distance entre deux ensembles de motifs (distance basee sur la distance de Hausdorff)
	 * @param reel
	 * @param calcule
	 * @return
	 */
	public static double distance(ArrayList<CoupleBitSet> reel, ArrayList<CoupleBitSet> calcule, String type) {
		double d = 0;

		double max1 = 0;
		for(CoupleBitSet e : reel) {
			double min1 = Double.MAX_VALUE;
			double distance = Double.MAX_VALUE;
			for(CoupleBitSet ee : calcule) {				
				//distance entre e et ee
				distance = distance(e,ee,type);				
				if(distance < min1) min1 = distance;
			}
			if(min1 > max1) max1 = min1;
		}

		double max2 = 0;
		for(CoupleBitSet e1 : calcule) {
			double min2 = Double.MAX_VALUE;
			double distance = Double.MAX_VALUE;
			for(CoupleBitSet ee1 : reel) {
				//distance entre e1 et ee1
				distance = distance(e1,ee1,type);				
				if(distance < min2) min2 = distance;
			}
			if(min2 > max2) max2 = min2;
		}

		//System.out.println("max1= "+max1+" max2= "+max2);
		//System.out.println("moyenne= "+((max1+max2)/2));

		//		if(max1 > max2) d = max1;
		//		else if(max2 > max1) d = max2;
		//		else d = max1;//cas max1==max2

		double moyenne = (max1+max2) / 2;
		d = moyenne;

		return d;
	}





	/**
	 * Test si un motif est present dans un ensemble de motifs
	 * @param bd l'ensemble exact des motifs
	 * @param transversal
	 * @return
	 */
	public static boolean contientTraverse(ArrayList<CoupleBitSet> bd, CoupleBitSet motif) {
		for(CoupleBitSet cbs : bd) {
			if(cbs.equalsVertexSet(motif.vertexSet) == true) 
				return true;
		}
		return false;
	}



	/**
	 * Comptage des motifs communs entre deux bordures 
	 * @param mintr
	 * @param mintrapprox
	 * @return
	 */
	public static int nbreMotifsCommuns(ArrayList<CoupleBitSet> bd, ArrayList<CoupleBitSet> bdapprox) {
		int nb = 0;
		for(CoupleBitSet cbs : bdapprox) {
			if(contientTraverse(bd, cbs) == true) 
				nb++;
		}
		return nb;
	}








	//	/**
	//	 * 
	//	 * @param ensemble
	//	 * @param numero
	//	 * @return
	//	 */
	//	public static boolean contient(ArrayList<Integer> ensemble, Integer numero) {
	//		for(Integer i : ensemble) {
	//			if(i.intValue()==numero.intValue()) return true;
	//		}
	//		return false;
	//	}



	//	/**
	//	 * Copie d'une liste de CoupleBitSet
	//	 * @param couvertes
	//	 * @return
	//	 */
	//	public static ArrayList<CoupleBitSet> copie(ArrayList<CoupleBitSet> couvertes) {
	//		ArrayList<CoupleBitSet> res = new ArrayList<CoupleBitSet>();
	//		for(CoupleBitSet cbs : couvertes) {
	//			res.add(cbs.clone());
	//		}
	//		return res;
	//	}






	/**
	 * @param args
	 */
	public static void main(String[] args) {	

		if(args.length<3)
			System.out.println("Usage : DistanceBordures fichierBordureExacte fichierBordureApprox minsup\n");
		else
		{	
			String nomfichierbordurereelle = args[0];
			String nomfichierbordurapprox = args[1];
			String minsup = args[2];

			// bordure reelle
			ArrayList<CoupleBitSet> bordureReelle = new ArrayList<CoupleBitSet> ();
			chargementDonnees(nomfichierbordurereelle, bordureReelle);
			Stats statreelle = calculStats(bordureReelle);
			//System.out.println("Stats bordure reelle : "+statreelle);

			// bordure approchee
			ArrayList<CoupleBitSet> bordureApprox = new ArrayList<CoupleBitSet> ();
			chargementDonnees(nomfichierbordurapprox, bordureApprox);
			Stats statapprox =calculStats(bordureApprox);
			//System.out.println("Stats bordure approx : "+statapprox);


			// distance de Hausdorff entre la bordure calculee et la bordure reelle
			//double distance1 = distance(bordureApprox, bordureReelle, "jaccard");
			//System.out.println("\nDistance jaccard = \n"+distance1);
			//double distance2 = distance(bordureApprox, bordureReelle, "dice");
			//System.out.println("\nDistance2 dice = \n"+distance2);

			double distance3 = distance(bordureApprox, bordureReelle, "cosine");
			//System.out.println("\nDistance3 cosine = "+distance3);

			//double distance4 = distance(bordureApprox, bordureReelle, "tanimoto");
			//System.out.println("\nDistance4 tanimoto = \n"+distance4);
			//double distance5 = distance(bordureApprox, bordureReelle, "overlap");
			//System.out.println("\nDistance5 overlap = \n"+distance5);

			//System.out.println(distance1+" "+distance2+" "+distance3+" "+distance4+" "+distance5);

			int nbmotifscommuns = nbreMotifsCommuns(bordureReelle, bordureApprox);
			//System.out.println("\nNb motifs communs = "+nbmotifscommuns);

			double precision = 0.0;
			double rappel = 0.0;

			precision = (double)nbmotifscommuns / bordureApprox.size();

			rappel = (double)nbmotifscommuns / bordureReelle.size();

			//System.out.println("\nPrecision = "+precision);
			//System.out.println("Rappel = "+rappel);

			//TODO
			System.out.println(minsup+" "+distance3);


			try {
				String fsortie = nomfichierbordurapprox+".stats0";
				BufferedWriter bw = new BufferedWriter(new FileWriter(fsortie));
				bw.write("# Stats bordure reelle : "+statreelle+"\n");
				bw.write("# Stats bordure approx : "+statapprox+"\n");
				bw.write("# distance3 cosine = "+distance3+"\n");
				bw.write("# Nb motifs communs = "+nbmotifscommuns+"\n");
				bw.write("# Precision = "+precision+"\n");
				bw.write("# Rappel = "+rappel+"\n");
				bw.write("# "+statapprox.nbMotifs+" & "+nbmotifscommuns+" & "+(Double.toString(distance3)).replace('.', ',')+" \\\\"+"\n");
				bw.close();
			} catch (IOException e) {
				e.printStackTrace();
			}

		}

	}



}

