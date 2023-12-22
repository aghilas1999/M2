package podami.max;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

//import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowth;
import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPMax;

/**
 * Calcul de la bordure positive de motifs frequents avec FPMAX (SPMF)
 */
public class FPmax {

	public static void main(String [] args) throws FileNotFoundException, IOException{
		
		// the file paths
		String input = args[0];  // the database
		String output = args[2];  // the path for saving the frequent itemsets found
		
		// minimum support
		int minsup = Integer.parseInt(args[1]); // minsup
		
		// Applying the FPMax algorithm
		AlgoFPMax algo = new AlgoFPMax();
		algo.runAlgorithm(input, output, minsup);
		algo.printStats();
	}
	
	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = FPmax.class.getResource(filename);
		 return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}
}
