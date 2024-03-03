package podami.hypergraph.staccato;

import java.util.Comparator;
import java.util.Map;


/**
 * 
 * @author Nicolas Durand <nicolas.durand@univ-amu.fr><br>https://pageperso.lis-lab.fr/nicolas.durand/<br>
 * LSIS CNRS UMR 7296<br>Université d'Aix-Marseille (AMU)
 *
 */
public class OccurrenceComparator implements Comparator<Integer>{
    private Map<Integer, Integer> occurrence;//pour garder une copie du Map que l'on souhaite traiter
    
    public OccurrenceComparator(Map<Integer, Integer> occurrence){
        this.occurrence = occurrence; //stocker la copie pour qu'elle soit accessible dans compare()
    }

	public int compare(Integer o1, Integer o2) {
        Integer val1 = occurrence.get(o1);
        Integer val2 = occurrence.get(o2);
		//return val1-val2;
        return val2-val1;
	}
	
}
