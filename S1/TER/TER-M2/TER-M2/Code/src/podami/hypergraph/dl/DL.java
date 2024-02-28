package podami.hypergraph.dl;

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



/**
 * <p>Implémentation de l'algorithme de Dong et Li pour le calcul de transversaux minimaux d'un hypergraphe</p>
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Université d'Aix-Marseille (AMU)
 * @version 1.0
 */
public class DL {

	/**
	 * Nom du fichier contenant les donnees (l'hypergraphe)
	 */
	private String fichierDonnees;

	/**
	 * Nombre de sommets de l'hypergraphe
	 */
	private int nbSommets;

	/**
	 * Nombre d'hyperaretes de l'hypergraphe
	 */
	private int nbHyperaretes;

	/**
	 * Ensemble des transversaux minimaux
	 */
	public ArrayList<CoupleBitSet> mintr;


	/**
	 * Affichage de la trace d'execution
	 */
	boolean affichage;


	/**
	 * Constructeur par defaut
	 */
	public DL() {
		this.fichierDonnees = "tmp";
		this.nbSommets = 0;
		this.mintr = new ArrayList<CoupleBitSet>();
		this.affichage = false;
	}


	/**
	 * Constructeur
	 * @param nomFichier Nom du fichier contenant les donnees (i.e. l'hypergraphe)
	 */
	public DL(String nomFichier) {
		this.fichierDonnees = nomFichier;
		this.nbSommets = 0;
		this.mintr = new ArrayList<CoupleBitSet>();
		this.affichage = false;
	}


	/**
	 * Retourne les transversaux minimaux
	 * @return mintr
	 */
	public ArrayList<CoupleBitSet> getMintr()
	{
		return this.mintr;
	}



	/**
	 * DL
	 */
	public void dl() {
		BufferedReader br;
		StringTokenizer st;
		String ligne = "";
		String sommet = ""; // numero du sommet lu
		int p = 0; // numero de l'hyperarete lu
		int numsommet;


		try {
			br = new BufferedReader(new FileReader(this.fichierDonnees));			

			// calcul du nombre de sommets et d'hyperaretes
			while(br.ready())
			{
				p++;
				sommet = "";
				ligne = br.readLine();
				if(ligne.startsWith("#")==false) { //TODO
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

			this.nbHyperaretes = (int)p;

			if(affichage) System.out.println(this.nbSommets+" sommets et "+this.nbHyperaretes+" hyperaretes");




			br = new BufferedReader(new FileReader(this.fichierDonnees));
			p = 0;

			CoupleBitSet cbs = null;
			CoupleBitSet cbs2 = null;
			CoupleBitSet cbs3 = null;
			CoupleBitSet hyperarete = null;
			BitSet sommetsCouverts = null;
			BitSet sommetsAutres = null;
			BitSet inter = null;
			ArrayList<CoupleBitSet> trGaranties = null;
			ArrayList<CoupleBitSet> trAutres = null;
			int index = -1;
			int i = 0;
			boolean ajout = false;


			while(br.ready())
			{
				ligne = br.readLine();
				if(ligne.startsWith("#")==false) { //TODO

					p++; // numero hyperarete (= numero de la ligne lue)
					sommet = "";
					sommetsCouverts = new BitSet();
					sommetsAutres = new BitSet();
					hyperarete = new CoupleBitSet();
					trGaranties = new ArrayList<CoupleBitSet>();
					trAutres = new ArrayList<CoupleBitSet>();

					st = new StringTokenizer(ligne, " \t\n\r"); 
					while(st.hasMoreTokens())
					{
						sommet = st.nextToken();
						if(p == 1) {
							cbs = new CoupleBitSet();
							cbs.addVertex(Integer.parseInt(sommet));
							mintr.add(cbs);
						}
						else {
							hyperarete.addVertex(Integer.parseInt(sommet));
						}
					}


					if(affichage) {
						System.out.print("\nAjout de l'hyperarete ");
						hyperarete.displayVertexSet(null);
						System.out.print("\n\n");
					}
					//else System.out.print("\r\r"+(int)p+" eme hyperarete ajoutee");


					if(p > 1)
					{
						// calcul des nouvelles transversaux minimaux en considerant la nouvelle hyperarete e

						// Traverses minimales garanties :
						// Pour chaque transversal minimal cbs de mintr, si cbs inter hyperarete est n'est pas vide, alors cbs est garantie (trGaranties) 
						// on stocke les autres cbs' dans une liste trAutres
						//
						// Sommets couverts
						//
						for(Iterator<CoupleBitSet> it = mintr.iterator(); it.hasNext();)
						{
							cbs = (CoupleBitSet)it.next();
							if(cbs.intersectionVertexSet(hyperarete).cardinality() != 0) 
							{
								trGaranties.add(cbs);

								inter = cbs.intersectionVertexSet(hyperarete);
								if(cbs.vertexSet.cardinality()==1 && inter.cardinality()>0)
									sommetsCouverts.or(inter);
							}
							else trAutres.add(cbs);
						}

						// Sommets autres
						i = 0;
						index = -1;
						while(i <= hyperarete.vertexSet.size())
						{
							index = hyperarete.vertexSet.nextSetBit(i);
							if(index == -1) break;
							if(sommetsCouverts.get(index)==false)
								sommetsAutres.set(index);
							i = index + 1;
						}


						if(affichage) {
							System.out.println("trGaranties : ");
							afficheListCoupleBitSetVertex(trGaranties);

							System.out.println("trAutres : ");
							afficheListCoupleBitSetVertex(trAutres);

							System.out.print("SommetsCouverts : ");
							(new CoupleBitSet(sommetsCouverts)).displayVertexSet(null);
							System.out.print("\n\n");

							System.out.print("SommetsAutres : ");
							(new CoupleBitSet(sommetsAutres)).displayVertexSet(null);
							System.out.print("\n\n");
						}



						//TODO TRIER trAutres selon cardinalite croissante de chaque tr ?



						// Pour chaque transversal minimal cbs de trAutres (TRIEE selon cardinalite croissante),
						// -- pour chaque sommet v de sommetsAutres,
						// ---- si cbs2={t' union v} n'est pas un surensemble d'un t de trGaranties, 
						//      alors ajouter cbs2 a trGaranties
						for(Iterator<CoupleBitSet> it = trAutres.iterator(); it.hasNext();)
						{
							cbs = (CoupleBitSet)it.next();
							i = 0;
							index = -1;
							while(i <= sommetsAutres.size())
							{
								index = sommetsAutres.nextSetBit(i);
								if(index == -1) break;
								cbs2 = cbs.clone();
								cbs2.addVertex(index);
								ajout = true;
								for(Iterator<CoupleBitSet> it2 = trGaranties.iterator(); it2.hasNext() && ajout;)
								{
									cbs3 = (CoupleBitSet)it2.next();
									if(cbs3.includedVertexSet(cbs2.vertexSet))
										ajout = false;
								}
								if(ajout) trGaranties.add(cbs2);
								i = index + 1;
							}
						}


						mintr = trGaranties;
						trGaranties = null;
						sommetsCouverts = null;
						sommetsAutres = null;
						trAutres = null;

						if(affichage) {
							System.out.println("Ensemble des mintr : ");
							afficheListCoupleBitSetVertex(mintr);
						}

					}
					else if(affichage) afficheListCoupleBitSetVertex(mintr);
				}
			}
			br.close();

			if(affichage) System.out.print("\n");

			//			BufferedWriter bw = new BufferedWriter(new FileWriter(fichierDonnees+".dl.tr"));
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






	/**
	 * Utilisee par l'algorithme BMR
	 * @param hyperaretes
	 * @return
	 */
	public void dl(ArrayList<CoupleBitSet> hyperaretes, boolean aff) {

		this.nbHyperaretes = hyperaretes.size();

		int p = 0; // numero de l'hyperarete
		CoupleBitSet cbs = null;
		CoupleBitSet cbs2 = null;
		CoupleBitSet cbs3 = null;
		BitSet sommetsCouverts = null;
		BitSet sommetsAutres = null;
		BitSet inter = null;
		ArrayList<CoupleBitSet> trGaranties = null;
		ArrayList<CoupleBitSet> trAutres = null;
		int index = -1;
		int i = 0;
		boolean ajout = false;


		for(CoupleBitSet hyperarete : hyperaretes)
		{
			p++; // numero de l'hyperarete
			sommetsCouverts = new BitSet();
			sommetsAutres = new BitSet();
			trGaranties = new ArrayList<CoupleBitSet>();
			trAutres = new ArrayList<CoupleBitSet>();

			if(aff) {
				System.out.print("\nTraitement de l'hyperarete ");
				hyperarete.displayVertexSet(null);
				System.out.print("\n\n");
			}
			else {
				//System.out.print("\r\r"+(int)p+" eme hyperarete en cours de traitement...");
			}


			// si 1er hyperarete 
			if(p == 1)
			{
				//parcours des sommets de hyperarete
				i = 0;
				index = -1;
				while(i <= hyperarete.getVertexes().size())
				{
					index = hyperarete.getVertexes().nextSetBit(i);
					if(index == -1) break;
					cbs = new CoupleBitSet();
					cbs.addVertex(index);
					mintr.add(cbs);
					i = index + 1;
				}
			}

			if(p > 1)
			{
				// calcul des nouvelles transversaux minimaux en considerant la nouvelle hyperarete e

				// Traverses minimales garanties :
				// Pour chaque transversal minimal cbs de mintr, si cbs inter hyperarete est n'est pas vide, alors cbs est garantie (trGaranties) 
				// on stocke les autres cbs' dans une liste trAutres
				//
				// Sommets couverts
				//
				for(Iterator<CoupleBitSet> it = mintr.iterator(); it.hasNext();)
				{
					cbs = (CoupleBitSet)it.next();
					if(cbs.intersectionVertexSet(hyperarete).cardinality() != 0) 
					{
						trGaranties.add(cbs);

						inter = cbs.intersectionVertexSet(hyperarete);
						if(cbs.vertexSet.cardinality()==1 && inter.cardinality()>0)
							sommetsCouverts.or(inter);
					}
					else trAutres.add(cbs);
				}

				// Sommets autres
				i = 0;
				index = -1;
				while(i <= hyperarete.vertexSet.size())
				{
					index = hyperarete.vertexSet.nextSetBit(i);
					if(index == -1) break;
					if(sommetsCouverts.get(index)==false)
						sommetsAutres.set(index);
					i = index + 1;
				}


				if(aff) {
					System.out.println("trGaranties : ");
					afficheListCoupleBitSetVertex(trGaranties);

					System.out.println("trAutres : ");
					afficheListCoupleBitSetVertex(trAutres);

					System.out.print("SommetsCouverts : ");
					(new CoupleBitSet(sommetsCouverts)).displayVertexSet(null);
					System.out.print("\n\n");

					System.out.print("SommetsAutres : ");
					(new CoupleBitSet(sommetsAutres)).displayVertexSet(null);
					System.out.print("\n\n");
				}



				//TODO TRIER trAutres selon cardinalite croissante de chaque tr ?



				// Pour chaque transversal minimal cbs de trAutres (TRIEE selon cardinalite croissante),
				// -- pour chaque sommet v de sommetsAutres,
				// ---- si cbs2={t' union v} n'est pas un surensemble d'un t de trGaranties, 
				//      alors ajouter cbs2 a trGaranties
				for(Iterator<CoupleBitSet> it = trAutres.iterator(); it.hasNext();)
				{
					cbs = (CoupleBitSet)it.next();
					i = 0;
					index = -1;
					while(i <= sommetsAutres.size())
					{
						index = sommetsAutres.nextSetBit(i);
						if(index == -1) break;
						cbs2 = cbs.clone();
						cbs2.addVertex(index);
						ajout = true;
						for(Iterator<CoupleBitSet> it2 = trGaranties.iterator(); it2.hasNext() && ajout;)
						{
							cbs3 = (CoupleBitSet)it2.next();
							if(cbs3.includedVertexSet(cbs2.vertexSet))
								ajout = false;
						}
						if(ajout) trGaranties.add(cbs2);
						i = index + 1;
					}
				}


				mintr = trGaranties;
				trGaranties = null;
				sommetsCouverts = null;
				sommetsAutres = null;
				trAutres = null;

				if(aff) {
					System.out.println("Ensemble des mintr : ");
					afficheListCoupleBitSetVertex(mintr);
				}

			}
			else if(aff) afficheListCoupleBitSetVertex(mintr);
		}

	}



	/**
	 * 
	 * @param nomFichier
	 */
	public static void doJob(String nomFichier) {
		long START = 0;
		long END = 0;
		DL dl = new DL(nomFichier);
		START = System.currentTimeMillis();
		dl.dl();
		END = System.currentTimeMillis();
		double tempsexecution = END - START;
		System.out.print(tempsexecution+" ms");

		try {
			BufferedWriter bw = new BufferedWriter(new FileWriter(dl.fichierDonnees+".dl.tr"));
			bw.write("# "+tempsexecution+" ms\n");
			dl.saveMinimalTransversals(bw);
			bw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}


	/**
	 * @param args
	 */
	public static void main(String[] args) {

		if(args.length<1)
			System.out.println("Usage : DL fichier_hypergraphe\n");
		else
		{	
			doJob(args[0]);
		}

	}


}


