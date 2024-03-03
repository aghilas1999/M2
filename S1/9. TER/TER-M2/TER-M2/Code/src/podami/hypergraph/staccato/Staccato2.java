package podami.hypergraph.staccato;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.StringTokenizer;

import podami.common.CoupleBitSet;



/**
 * Implementation de l'algorithme STACCATO modifie
 * pour le calcul de transversaux minimaux dans un
 * cadre general
 *  
 * @author Ning Deng
 * @author Nicolas Durand
 * 
 * @version 0.1
 */
public class Staccato2 {

	public static boolean affichage = false;


	/**
	 * Nombre de resultats (= nombre de transversaux)
	 */
	private int L;


	/**
	 * Proportion de sommets (une valeur entre 0 et 1) a prendre en compte dans les tris
	 */
	private double lambda;


	/**
	 * Nombre d'exceptions admises (= nombre d'hyperaretes pouvant ne pas etre intersectees)
	 */
	private int delta;


	/**
	 * Nombre d'hyperaretes de l'hypergraphe
	 */
	private int nbHyperaretes;

	/**
	 * Nombre d'hyperaretes de l'hypergraphe
	 */
	private int nbSommets;


	/**
	 * Matrice representant l'hypergraphe
	 */
	public Boolean[][] hyper;



	/**
	 * Constructeur par defaut
	 */
	public Staccato2(int L, double lambda, int delta) {
		this.L = L;
		this.lambda = lambda;
		this.delta = delta;
		this.nbHyperaretes = 0;
		this.nbSommets = 0;
	}


	/**
	 * Tri des sommets en fonction du nombre d'occurrences (ordre decroissant)
	 * @param A Matrice (hypergraphe)
	 * @param M nombre de sommets
	 * @return Liste de sommets
	 */
	private ArrayList<Integer> rank(Boolean[][] A, HashMap<Integer, Integer> occurrence) {

		// parcours de la matrice A et calcul des nombres d'occurrence
		Integer sommet = null;
		for(int i=0; i<this.nbHyperaretes; i++) {
			for(int j=0; j<this.nbSommets; j++) {
				if(A[i][j] != null && A[i][j] == true) {
					sommet = new Integer(j+1);
					if(occurrence.containsKey(sommet))
						occurrence.put(sommet, occurrence.get(sommet)+1);
					else occurrence.put(sommet, 1);
				}
			}
		}

		if(affichage) System.out.println("Occurrences : "+occurrence.toString());

		// tri des sommets selon le nbre d'occurrences (ordre decroissant)
		ArrayList<Integer> R = new ArrayList<Integer>(occurrence.keySet());
		Collections.sort(R, new OccurrenceComparator(occurrence));

		if(affichage) System.out.println("R = "+R.toString());

		return R;
	}




	/**
	 * Desactive la colonne j d'une matrice
	 * @param A Matrice (l'hypergraphe)
	 * @param colj Sommet j (colonne j) a desactiver (mettre a null)
	 * @return Aprim Matrice avec la colonne j desactivee
	 */
	private Boolean[][] stripComponent(Boolean[][] A, int colj) {
		Boolean[][] Aprim = new Boolean[this.nbHyperaretes][this.nbSommets];

		for(int i=0; i<this.nbHyperaretes; i++) {
			for(int j=0; j<this.nbSommets; j++) {
				if(j == colj) Aprim[i][j] = null;
				else Aprim[i][j] = A[i][j];  
			}
		}

		if(affichage) {
			//afficher la matrice Aprim
			System.out.println("Nouvelle Matrice A = ");
			this.affichageMatrice(Aprim);
		}

		return Aprim;
	}



	/**
	 * Desactive la colonne j d'une matrice et desactive les lignes où j est present
	 * @param A Matrice (l'hypergraphe)
	 * @param colj Sommet j (colonne j)
	 * @return Aprim Matrice avec la colonne j desactivee et les lignes (où j est present) desactivees
	 */
	private Boolean[][] strip(Boolean[][] A, int colj) {
		Boolean[][] Aprim = new Boolean[this.nbHyperaretes][this.nbSommets];

		boolean ligneAdesactiver = false;

		for(int i=0; i<this.nbHyperaretes; i++) {
			ligneAdesactiver = false;
			if(A[i][colj] != null && A[i][colj] == true) ligneAdesactiver = true; // j est present sur la ligne i qui doit etre desactivee

			for(int j=0; j<this.nbSommets; j++) {
				if(ligneAdesactiver == true) {
					Aprim[i][j] = null;
				}
				if(j == colj) {
					Aprim[i][j] = null;
				}
				else if(ligneAdesactiver == false) Aprim[i][j] = A[i][j];
			}			
		}

		if(affichage) {
			System.out.println("\nMatrice Aprim = ");
			this.affichageMatrice(Aprim);
		}

		return Aprim;
	}




	/**
	 * Test si aucun transversal de l'ensemble D n'est inclus dans le transversal trjprim 
	 * @param D ensemble de transversaux
	 * @param trjprim le transversal a tester
	 * @return boolean
	 */
	private boolean isNotSubsumed(ArrayList<CoupleBitSet> D, CoupleBitSet trjprim) {
		for(CoupleBitSet tr : D) {
			if(affichage) {
				System.out.println("\ntr= ");
				tr.displayVertexSet(null);
				System.out.println("\ntrjprim= ");
				trjprim.displayVertexSet(null);
				System.out.println("\ntr.isIncluded(trjprim)= "+tr.isIncluded(trjprim));
			}
			if(tr.isIncluded(trjprim)) return false;
		}

		return true;
	}



	/**
	 * Compte le nombre de lignes actives d'une matrice A (nombre de lignes avec au moins une valeur not null)
	 * @param A la matrice
	 * @return int nombre de lignes
	 */
	private int compteNbLignesActives(Boolean[][] A) {
		int nb = 0;
		boolean ligneOK = false;

		for(int i=0; i<this.nbHyperaretes; i++) {
			ligneOK = false;
			for(int j=0; j<this.nbSommets; j++) {
				if(A[i][j] != null) {
					ligneOK = true;
					break;
				}
			}
			if(ligneOK == true) nb++;
		}

		return nb;
	}





	/**
	 * Fonction recursive staccato2
	 */
	public ArrayList<CoupleBitSet> staccato2(Boolean[][] A) {
		HashMap<Integer, Integer> occurrence = new HashMap<Integer, Integer>(); // n11[] (nombre d'occurrences de chaque sommet)
		ArrayList<Integer> R = this.rank(A, occurrence);
		double seen = 0;
		ArrayList<CoupleBitSet> D = new ArrayList<CoupleBitSet>();

		int M = R.size(); // nombre de sommets (components)
		int nbLignesActives = this.compteNbLignesActives(A);

		if(affichage) {
			System.out.println("->appel Staccato2 : "+nbLignesActives+" hyperaretes et "+M+" sommets");
		}

		int sommet = -1;
		for(int j=0; j<this.nbSommets; j++) {
			sommet = j + 1;
			if(occurrence.containsKey(sommet) && occurrence.get(sommet) == (nbLignesActives - delta)) { // nombre d'occurrence de j = nombre d'hyperaretes - delta
				// sommet j+1 est un transversal minimal
				CoupleBitSet tr = new CoupleBitSet();
				tr.addVertex(sommet);
				D.add(tr);

				occurrence.remove(sommet); // on enleve le sommet j+1

				seen = seen + ((double)1 / M);

				A = stripComponent(A,j);
			}
		}

		// nouvelle liste triee de sommets
		R = new ArrayList<Integer>(occurrence.keySet());
		Collections.sort(R, new OccurrenceComparator(occurrence));

		//TODO

		Integer j = null;
		Boolean[][] Aprim = null;
		ArrayList<CoupleBitSet> Dprim = null;
		CoupleBitSet trjprim = null;

		while(R.size() > 0 && seen <= this.lambda && D.size() < this.L) {
			j = R.get(0);
			R.remove(0);
			seen = seen + ((double)1 / M);
			Aprim = this.strip(A, j-1);
			Dprim = this.staccato2(Aprim);

			if(affichage) {
				System.out.println("\nDprim = ");
				this.afficheListeCoupleBitSets(Dprim);
				System.out.println("\n");
			}

			while(Dprim.size() > 0)  {
				trjprim = Dprim.get(0);
				Dprim.remove(0);
				trjprim.addVertex(j.intValue()); //TODO

				if(affichage) {
					System.out.print("\nD= ");
					this.afficheListeCoupleBitSets(D);
					System.out.print("trjprim= ");
					trjprim.displayVertexSet(null);
					System.out.println("\nisnotsubsumed= "+isNotSubsumed(D, trjprim));
				}

				if(isNotSubsumed(D, trjprim)) {
					D.add(trjprim);
				}
			}
		}

		return D;
	}





	/**
	 * Affichage d'une matrice (un hypergraphe)
	 * @param A
	 */
	public void affichageMatrice(Boolean[][] A) {
		for(int i=0; i<this.nbHyperaretes; i++) {
			for(int j=0; j<this.nbSommets; j++) {
				if(A[i][j] == null) System.out.print((j+1)+":null ");
				else if(A[i][j] == true) System.out.print((j+1)+" ");
			}
			System.out.print("\n");
		}
		System.out.print("\n");
	}



	/**
	 * Affichage d'une liste de CoupleBitSets
	 * @param listtr
	 */
	public void afficheListeCoupleBitSets(ArrayList<CoupleBitSet> listtr) {
		CoupleBitSet tr = null;
		System.out.println("{");
		for(Iterator<CoupleBitSet> i = listtr.iterator(); i.hasNext();) {
			tr = (CoupleBitSet)i.next();
			tr.displayVertexSet(null);
			System.out.print("\n");
		}
		System.out.println("}\n");
	}



	/**
	 * Enregistrement d'une liste de transversaux dans un fichier
	 * @param mintr Liste de transversaux
	 * @param bw Fichier de sortie
	 * @throws IOException
	 */
	public void saveTransversals(ArrayList<CoupleBitSet> mintr, BufferedWriter bw) throws IOException {
		CoupleBitSet tr = null;
		for(Iterator<CoupleBitSet> i = mintr.iterator(); i.hasNext();) {
			tr = (CoupleBitSet)i.next();
			tr.save(bw, null);
		}
	}




	/**
	 * 
	 * @param fichierDonnees
	 */
	private void initialisation(String fichierDonnees) {
		BufferedReader br;
		StringTokenizer st;
		String ligne = "";
		String sommet = "";
		int numsommet = -1; // numero du sommet lu
		int numhyperarete = 0; // numero de l'hyperarete lu

		try {
			br = new BufferedReader(new FileReader(fichierDonnees));			

			// calcul du nombre de sommets et d'hyperaretes
			while(br.ready())
			{
				numhyperarete++;
				sommet = "";
				ligne = br.readLine();
				st = new StringTokenizer(ligne, " \t\n\r"); 
				while(st.hasMoreTokens())
				{
					sommet = st.nextToken();
					numsommet = Integer.parseInt(sommet);
					
					////////////////////////////////
					//numsommet = numsommet + 1;//TODO
					////////////////////////////////
					
					if(numsommet > this.nbSommets) this.nbSommets = numsommet;
				}
			}
			br.close();

			this.nbHyperaretes = numhyperarete;

			if(affichage) System.out.println(this.nbSommets+" sommets et "+this.nbHyperaretes+" hyperaretes");



			// matrice A (l'hypergraphe)
			Boolean[][] A = new Boolean[this.nbHyperaretes][this.nbSommets];

			// initialisation de A
			for(int i=0; i<this.nbHyperaretes; i++) {
				for(int j=0; j<this.nbSommets; j++) {
					A[i][j] = new Boolean(false);
				}
			}


			// chargement de la matrice A
			br = new BufferedReader(new FileReader(fichierDonnees));
			numhyperarete = 0;

			while(br.ready())
			{
				numhyperarete++; // numero hyperarete (= numero de la ligne)
				sommet = "";
				numsommet = -1;
				ligne = br.readLine();
				st = new StringTokenizer(ligne, " \t\n\r"); 
				while(st.hasMoreTokens())
				{
					sommet = st.nextToken();
					numsommet = Integer.parseInt(sommet);
					
					////////////////////////////////
					//numsommet = numsommet + 1;//TODO
					////////////////////////////////
					
					A[numhyperarete-1][numsommet-1] = new Boolean(true); //ATTENTION decalage de 1 dans indice
				}
			}

			this.hyper = A;

			if(affichage) {
				//afficher la matrice A
				System.out.println("\nMatrice A = ");
				this.affichageMatrice(A);
			}

		}
		catch (IOException e) {
			e.printStackTrace();
		}
	}



	/**
	 * 
	 * @param hyper
	 */
	public void chargeDonnees(ArrayList<CoupleBitSet> hyper) {

		if(affichage) {
			//afficher les hyperaretes
			System.out.println("\nHyperaretes = ");
			CoupleBitSet.afficheListCoupleBitSetVertex(hyper);
		}
		
		//compter le nombre de sommets de l'hypergraphe
		BitSet b = new BitSet();
		for(CoupleBitSet cb : hyper) {
			b.or(cb.getVertexes());
		}
		this.nbSommets = b.length() - 1; //TODO
		this.nbHyperaretes = hyper.size();
		
		if(affichage) System.out.println(this.nbSommets+" sommets et "+this.nbHyperaretes+" hyperaretes");
		
		
		// matrice A (l'hypergraphe)
		Boolean[][] A = new Boolean[this.nbHyperaretes][this.nbSommets];

		// initialisation de A
		for(int i=0; i<this.nbHyperaretes; i++) {
			for(int j=0; j<this.nbSommets; j++) {
				A[i][j] = new Boolean(false);
			}
		}


		BitSet sommets = null;
		int i = 0;
		int index = -1;
		int numerohyperarete = 0;
		for(CoupleBitSet cbs : hyper) {
			sommets = cbs.vertexSet;
			i = 0;
			index = -1;
			while(i <= sommets.size())
			{
				index = sommets.nextSetBit(i);
				if(index == -1) break;
				A[numerohyperarete][index-1] = new Boolean(true);
				i = index + 1;
			}
			numerohyperarete++;
		}
		
		this.hyper = A;

		if(affichage) {
			//afficher la matrice A
			System.out.println("\nMatrice A = ");
			this.affichageMatrice(A);
		}

	}




	/**
	 * @param nomFichier nom du fichier contenant l'hypergraphe
	 * @param lambda proportion de sommets (une valeur entre 0 et 1)
	 * @param L nombre de transversaux resultats
	 * @param delta nombre d'hyperaretes pouvant ne pas etre intersectees
	 */
	public static void main(String[] args) {

		if(args.length<4)
			System.out.println("Usage: Staccato2 fichier_hypergraphe lambda L delta\n");
		else
		{	
			String fichierDonnees = args[0];
			double lambda = Double.parseDouble(args[1]);
			int L = Integer.parseInt(args[2]);
			int delta = Integer.parseInt(args[3]);
			long START = 0;
			long END = 0;

			Staccato2 sta = new Staccato2(L, lambda, delta);

			sta.initialisation(fichierDonnees);

			//test de la fonction strip
			//A = sta.strip(A, 4); // test sommet 5 (colonne 4)

			START = System.currentTimeMillis();
			ArrayList<CoupleBitSet> resultats = sta.staccato2(sta.hyper); // STACCATO2
			END = System.currentTimeMillis();

			if(affichage) System.out.println("\n");

			double tempsexecution = END - START;
			System.out.println(tempsexecution+" ms");

			if(affichage) {
				System.out.println("lambda= "+lambda+" ("+(sta.nbSommets * lambda)+" sommets)");
				System.out.println("L= "+L);
				System.out.println("delta= "+delta);
			}

			if(affichage) {
				System.out.println("\n"+"Resultats = ");
				sta.afficheListeCoupleBitSets(resultats);
			}


			try {
				BufferedWriter bw = new BufferedWriter(new FileWriter(fichierDonnees+".staccato2.l"+lambda+".L"+L+".d"+delta+".tr"));
				bw.write("# "+tempsexecution+" ms\n");
				bw.write("# lambda= "+lambda+" ("+(sta.nbSommets * lambda)+" sommets)\n");
				bw.write("# L= "+L+"\n");
				bw.write("# delta= "+delta+"\n");
				bw.write("# "+(Double.toString(lambda)).replace('.', ',')+" ("+((int)(sta.nbSommets * lambda))+") & "+(Double.toString(tempsexecution)).replace('.', ',')+" & "+"\n");
				bw.flush();
				sta.saveTransversals(resultats, bw);
				bw.close();
			}
			catch (IOException e) {
				e.printStackTrace();
			}
		}
	}


}
