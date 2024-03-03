package podami.hypergraph.berge;

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
 * <p>Implémentation de l'algorithme de Berge pour le calcul de transversaux minimaux d'un hypergraphe</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Université d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class Berge {

	/**
	 * Nom du fichier contenant les donnees (l'hypergraphe)
	 */
	private String fichierDonnees;

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
	public Berge(String nomFichier) {
		this.fichierDonnees = nomFichier;
		this.nbSommets = 0;
		this.mintr = new ArrayList<CoupleBitSet>();
		this.affichage = false;
	}

	
	/**
	 * Berge
	 */
	public void berge() {
		BufferedReader br;
		StringTokenizer st;
		String ligne = "";
		String sommet = ""; // numero du sommet lu
		int p = 0; // numero de l'hyperarete lu
		//Integer n = 0;
		int numsommet;


		try {
			br = new BufferedReader(new FileReader(this.fichierDonnees));			

			// calcul du nombre de sommets et d'hyperaretes
			while(br.ready())
			{
				p++;
				sommet = "";
				ligne = br.readLine();
				st = new StringTokenizer(ligne, " \t\n\r"); 
				while(st.hasMoreTokens())
				{
					sommet = st.nextToken();
					numsommet = Integer.parseInt(sommet);
					if(numsommet > this.nbSommets) this.nbSommets = numsommet;
				}
			}
			br.close();

			if(affichage) System.out.println(this.nbSommets+" sommets et "+(int)p+" hyperaretes");




			br = new BufferedReader(new FileReader(this.fichierDonnees));
			p = 0;

			CoupleBitSet cbs = null;
			CoupleBitSet cbs2 = null;
			ArrayList<Integer> listeSommets = null;
			ArrayList<CoupleBitSet> ensemble = null;
			ArrayList<CoupleBitSet> asupprimer = new ArrayList<CoupleBitSet>();

			while(br.ready())
			{
				p++; // numero hyperarete (= numero de la ligne lue)
				sommet = "";
				listeSommets = new ArrayList<Integer>();
				ensemble = new ArrayList<CoupleBitSet>();
				ligne = br.readLine();
				st = new StringTokenizer(ligne, " \t\n\r");
				//hyperarete = new CoupleBitSet(); // l'hyperarete a ajouter 
				while(st.hasMoreTokens())
				{
					sommet = st.nextToken();
					if(p == 1) {
						cbs = new CoupleBitSet();
						cbs.addVertex(Integer.parseInt(sommet));
						mintr.add(cbs);
					}
					else listeSommets.add(Integer.parseInt(sommet));
				}

				//System.out.print("\r\r"+p+" eme hyperarete ajoutee");
				//System.out.print("\nAjout de l'hyperarete "+listeSommets.toString()+"\n");

				if(p > 1)
				{
					// calcul des nouveaux transversaux minimaux en considerant la nouvelle hyperarete
					// Pour chaque transversal minimal de mintr :
					// - pour chaque sommet de la nouvelle hyperarete,
					// - creer un nouveau transversal
					for(Iterator<CoupleBitSet> i = mintr.iterator(); i.hasNext();)
					{
						cbs = (CoupleBitSet)i.next();
						//System.out.print(" mintr : "); cbs.displayVertexSet(null); System.out.print("\n");
						for(Iterator<Integer> k = listeSommets.iterator(); k.hasNext();)
						{
							numsommet = (Integer) k.next();
							//System.out.println(" -> sommet : "+numsommet);
							cbs2 = (CoupleBitSet)cbs.clone();
							cbs2.addVertex(numsommet);
							ensemble.add(cbs2);
							//System.out.print(" ==> "); cbs2.displayVertexSet(null); System.out.println("\n");
						}
					}

					//System.out.println("\nEnsemble des candidats pour mintr : ");
					//afficheListCoupleBitSetVertex(ensemble);

					// calculer le min de cet nouvel ensemble pour obtenir le nouveau mintr
					// si un cbs est inclus dans (ou egal a) un cbs2 de l'ensemble,
					// alors supprimet cbs2 (on ne garde que cbs, le min)
					for(int i=0; i<ensemble.size(); i++)
					{
						cbs = ensemble.get(i);
						for(int j=i+1; j<ensemble.size(); j++)
						{
							cbs2 = ensemble.get(j);
							//							System.out.println("\nTest de :");
							//							cbs.displayVertexSet(null);
							//							System.out.print("\n");
							//							cbs2.displayVertexSet(null);
							if(cbs.equalsVertexSet(cbs2))
							{
								// doublon
								asupprimer.add(cbs2);
							}
							else {
								if(cbs.includedVertexSet(cbs2.vertexSet))
								{
									// cbs est inclus dans cbs2, on supprime alors cbs2
									asupprimer.add(cbs2);
									//									System.out.print(" -> ");
									//									cbs2.displayVertexSet(null);
									//									System.out.print(" est a supprimer\n");
								}
								if(cbs2.includedVertexSet(cbs.vertexSet))
								{
									// cbs2 est inclus dans cbs, on supprime alors cbs
									asupprimer.add(cbs);
									//									System.out.print(" -> ");
									//									cbs.displayVertexSet(null);
									//									System.out.print(" est a supprimer");
								}
							}
						}
					}

					for(Iterator<CoupleBitSet> i = asupprimer.iterator(); i.hasNext();)
					{
						cbs = (CoupleBitSet)i.next();
						ensemble.remove(cbs);
					}

					mintr = ensemble;
					ensemble = null;
					listeSommets = null;

					//System.out.println("Ensemble des mintr (temporaire) : ");
					//afficheListCoupleBitSetVertex(mintr);

				}
				//else afficheListCoupleBitSetVertex(mintr);
			}
			br.close();

			if(affichage) System.out.print("\n");

//			BufferedWriter bw = new BufferedWriter(new FileWriter(fichierDonnees+".berge.tr"));
//			saveMinimalTransversals(bw);
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

	
	
	

////////////////////////////////////////////////////////////////////////////////////////////////////////
	/**
	 * Algorithme de Berge pour calculer les transversaux minimaux
	 */
	public ArrayList<CoupleBitSet> berge(ArrayList<CoupleBitSet> hypergraphe) {
		ArrayList<CoupleBitSet> mintr = new ArrayList<CoupleBitSet>();
		boolean init = true;
		int numsommet = -1;
		CoupleBitSet cbs = null;
		CoupleBitSet cbs2 = null;
		CoupleBitSet cbs3 = null;
		ArrayList<CoupleBitSet> ensemble = new ArrayList<CoupleBitSet>();
		ArrayList<CoupleBitSet> asupprimer = new ArrayList<CoupleBitSet>();

		for(Iterator<CoupleBitSet> it  = hypergraphe.iterator(); it.hasNext();) {
			cbs3 = (CoupleBitSet) it.next();

			if(this.affichage) {
				//System.out.println("mintr = "); afficheListCoupleBitSetVertex(mintr);
				System.out.print("Examen de ");	cbs3.displayVertexSet(null); System.out.print("\n");
			}

			if(init) {
				//on prend la premiere "hyperarete" de hypergraphe
				//on forme un transversal min pour chaque sommet singleton de cette hyperarete
				int i = 0;
				int index = -1;
				while(i <= cbs3.vertexSet.size())
				{
					index = cbs3.vertexSet.nextSetBit(i);
					if(index == -1) break;
					cbs2 = new CoupleBitSet();
					cbs2.addVertex(index);
					mintr.add(cbs2);
					i = index + 1;
				}
				init = false;
			}
			else {
				//cas general
				// calcul des nouveaux transversaux minimaux en considerant la nouvelle hyperarete
				// Pour chaque transversal minimal de mintr :
				// - pour chaque sommet de la nouvelle hyperarete,
				// - creer une nouveau transversal
				ensemble = new ArrayList<CoupleBitSet>();

				for(Iterator<CoupleBitSet> i = mintr.iterator(); i.hasNext();)
				{
					cbs = (CoupleBitSet)i.next();
					//System.out.print(" mintr : "); cbs.displayVertexSet(null); System.out.print("\n");

					int k = 0;
					numsommet = -1;
					while(k <= cbs3.vertexSet.size())
					{
						numsommet = cbs3.vertexSet.nextSetBit(k);
						if(numsommet == -1) break;
						//System.out.println(" -> sommet : "+numsommet);
						cbs2 = (CoupleBitSet)cbs.clone();
						cbs2.addVertex(numsommet);
						ensemble.add(cbs2);
						//System.out.print(" ==> "); cbs2.displayVertexSet(null); System.out.println("\n");
						k = numsommet + 1;
					}
				}

				//System.out.println("\nEnsemble des candidats pour mintr : ");
				//afficheListCoupleBitSetVertex(ensemble);

				// calculer le min de cet nouvel ensemble pour obtenir le nouveau mintr
				// si un cbs est inclus dans (ou egal a) un cbs2 de l'ensemble,
				// alors supprimet cbs2 (on ne garde que cbs, le min)
				for(int i=0; i<ensemble.size(); i++)
				{
					cbs = ensemble.get(i);
					for(int j=i+1; j<ensemble.size(); j++)
					{
						cbs2 = ensemble.get(j);
						//							System.out.println("\nTest de :");
						//							cbs.displayVertexSet(null);
						//							System.out.print("\n");
						//							cbs2.displayVertexSet(null);
						if(cbs.equalsVertexSet(cbs2))
						{
							// doublon
							asupprimer.add(cbs2);
						}
						else {
							if(cbs.includedVertexSet(cbs2.vertexSet))
							{
								// cbs est inclus dans cbs2, on supprime alors cbs2
								asupprimer.add(cbs2);
								//									System.out.print(" -> ");
								//									cbs2.displayVertexSet(null);
								//									System.out.print(" est a supprimer\n");
							}
							if(cbs2.includedVertexSet(cbs.vertexSet))
							{
								// cbs2 est inclus dans cbs, on supprime alors cbs
								asupprimer.add(cbs);
								//									System.out.print(" -> ");
								//									cbs.displayVertexSet(null);
								//									System.out.print(" est a supprimer");
							}
						}
					}
				}

				for(Iterator<CoupleBitSet> i = asupprimer.iterator(); i.hasNext();)
				{
					cbs = (CoupleBitSet)i.next();
					ensemble.remove(cbs);
				}

				mintr = ensemble;
				ensemble = null;
			}
		}

		return mintr;
	}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	
	
	

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		if(args.length<1)
			System.out.println("Usage : Berge fichier_hypergraphe\n");
		else
		{	
			long START = 0;
			long END = 0;
			Berge mt = new Berge(args[0]);
			START = System.currentTimeMillis();
			mt.berge();
			END = System.currentTimeMillis();
			double tempsexecution = END - START;
			System.out.print(tempsexecution+" ms");

			try {
				BufferedWriter bw = new BufferedWriter(new FileWriter(mt.fichierDonnees+".berge.tr"));
				bw.write("# "+tempsexecution+" ms\n");
				mt.saveMinimalTransversals(bw);
				bw.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

	}

}

