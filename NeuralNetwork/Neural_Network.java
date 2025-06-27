import java.time.Clock;
import java.util.*;

public class Neural_Network {

    float[] max_value1;
    float[] max_value2;
    ArrayList<ArrayList<Float>> tab_input = new ArrayList<>();
    ArrayList<ArrayList<Float>> tab_output = new ArrayList<>();
    ArrayList<ArrayList<Float>> Prediction = new ArrayList<>();
    int inputSize;
    int outputSize;
    int hiddenSize;
    int coucheHidden;
    ArrayList<ArrayList<ArrayList<Float>>> AllWeight = new ArrayList<>();
    ArrayList<ArrayList<ArrayList<Float>>> Synapses = new ArrayList<>();

    protected float[] Start(int iter) {

        long t0 = Clock.systemUTC().millis();
        for (int i = 0; i < iter; i++) {
            ArrayList<ArrayList<Float>> forward = Forward(tab_input);
            Backward(tab_input, tab_output, forward);
        }
        long t1 = Clock.systemUTC().millis();

        System.out.println(coucheHidden + "/" + hiddenSize + "\t\t" + (float) (t1-t0)/1000 + "s");
        // System.out.println(Forward(tab_input));
        ArrayList<ArrayList<Float>> input = Forward(tab_input);
        float score_input = 0;
        for (int i = 0; i < input.size(); i++) {
            for (int j = 0; j < input.get(i).size(); j++) {
                score_input += Math.abs(input.get(i).get(j) - tab_input.get(i).get(j));
            }
        }
        System.out.println(score_input);
        ArrayList<ArrayList<Float>> resultat = Forward(Prediction);
        ArrayList<ArrayList<Float>> print = new ArrayList<>();
        for (int i = 0; i < resultat.size(); i++) {
            print.add(new ArrayList<>());
            for (int j = 0; j < resultat.get(i).size(); j++) {
                print.get(i).add(resultat.get(i).get(j) * max_value2[j]);
            }
        }
        System.out.println(print);
        System.out.println();
        return new float[] {score_input, (float) (t1-t0)/1000};
    }

    private void Clear() {
        tab_input = new ArrayList<>();
        tab_output = new ArrayList<>();
        Prediction = new ArrayList<>();
        AllWeight = new ArrayList<>();
        Synapses = new ArrayList<>();
    }

    protected void initialisation(float[][] entree, float[][] sortie, float[] prediction, int coucheCachee, int neuroneCache) {
        Clear();
        coucheHidden = coucheCachee;
        hiddenSize = neuroneCache;

        max_value1 = new float[entree[0].length];
        max_value2 = new float[sortie[0].length];
        for (float[] floats : entree) {
            for (int j = 0; j < floats.length; j++) {
                if (floats[j] > max_value1[j]) {
                    max_value1[j] = floats[j];
                }
            }
        }
        for (int j = 0; j < prediction.length; j++) {
            if (prediction[j] > max_value1[j]) {
                max_value1[j] = prediction[j];
            }
        }
        for (float[] floats : sortie) {
            for (int j = 0; j < floats.length; j++) {
                if (floats[j] > max_value2[j]) {
                    max_value2[j] = floats[j];
                }
            }
        }
        for (int i = 0; i < entree.length; i++) {
            tab_input.add(new ArrayList<>());
            for (int j = 0; j < entree[i].length; j++) {
                tab_input.get(i).add(entree[i][j] / max_value1[j]);
            }
        }
        for (int i = 0; i < sortie.length; i++) {
            tab_output.add(new ArrayList<>());
            for (int j = 0; j < sortie[i].length; j++) {
                tab_output.get(i).add(sortie[i][j] / max_value2[j]);
            }
        }

        Prediction.add(new ArrayList<>());
        for (int i = 0; i < prediction.length; i++) {
            Prediction.get(0).add(prediction[i] / max_value1[i]);
        }

        inputSize = tab_input.get(0).size();
        outputSize = tab_output.get(0).size();

        for (int i = 0; i < coucheHidden + 1; i++) {
            int e = hiddenSize;
            int s = hiddenSize;
            if (i == 0) {
                e = inputSize;
            }
            if (i == coucheHidden) {
                s = outputSize;
            }
            AllWeight.add(new ArrayList<>());
            for (int j = 0; j < e; j++) {
                AllWeight.get(i).add(new ArrayList<>());
                for (int k = 0; k < s; k++) {
                    AllWeight.get(i).get(j).add((float) Math.random());
                }
            }
        }
    }

    private ArrayList<ArrayList<Float>> Forward(ArrayList<ArrayList<Float>> Ventree) {
        Synapses = new ArrayList<>();
        for (int poids = 0; poids < AllWeight.size(); poids++) {
            ArrayList<ArrayList<Float>> e = Ventree;
            ArrayList<ArrayList<Float>> s = AllWeight.get(poids);
            if (poids != 0) {
                e = Synapses.get(poids - 1);
            }
            Synapses.add(SigmoidArray(Produit_Matriciel(e, s)));
        }
        return Synapses.get(Synapses.size()-1);
    }

    private void Backward(ArrayList<ArrayList<Float>> Ventree, ArrayList<ArrayList<Float>> Vobjectif, ArrayList<ArrayList<Float>> Vobtenue) {

        ArrayList<ArrayList<ArrayList<Float>>> addWeight = new ArrayList<>();
        ArrayList<ArrayList<Float>> outputError = new ArrayList<>();

        for (int i = 0; i < Vobjectif.size(); i++) {
            outputError.add(new ArrayList<>());
            for (int j = 0; j < Vobjectif.get(i).size(); j++) {
                outputError.get(i).add(Vobjectif.get(i).get(j) - Vobtenue.get(i).get(j));
            }
        }
        for (int i = 0; i < AllWeight.size(); i++) {
            addWeight.add(new ArrayList<>());
            ArrayList<ArrayList<Float>> erreur = outputError;
            ArrayList<ArrayList<Float>> sortie = Synapses.get(Synapses.size() - 1 - i);
            if (i != 0) {
                erreur = Produit_Matriciel(addWeight.get(i-1), TSwap(AllWeight.get(AllWeight.size()-i)));
            }
            for (int j = 0; j < erreur.size(); j++) {
                addWeight.get(i).add(new ArrayList<>());
                for (int k = 0; k < erreur.get(j).size(); k++) {
                    addWeight.get(i).get(j).add(erreur.get(j).get(k) * sigmoidPrime(sortie.get(j).get(k)));
                }
            }
        }

        for (int i = 0; i < AllWeight.size(); i++) {
            ArrayList<ArrayList<Float>> entree = Ventree;
            ArrayList<ArrayList<Float>> erreur = addWeight.get(addWeight.size()-1-i);
            if (i != 0) {
                entree = Synapses.get(i-1);
            }
            for (int y = 0; y < AllWeight.get(i).size(); y++) {
                for (int x = 0; x < AllWeight.get(i).get(y).size(); x++) {
                    AllWeight.get(i).get(y).set(x, AllWeight.get(i).get(y).get(x) + Produit_Matriciel(TSwap(entree), erreur).get(y).get(x));
                }
            }
        }
    }

    private static ArrayList<ArrayList<Float>> TSwap(ArrayList<ArrayList<Float>> tableau) {
        ArrayList<ArrayList<Float>> new_tab = new ArrayList<>();
        for (int A = 0; A < tableau.get(0).size(); A++) {
            new_tab.add(new ArrayList<>());
            for (ArrayList<Float> B : tableau) {
                new_tab.get(A).add(B.get(A));
            }
        }
        return new_tab;
    }

    private static ArrayList<ArrayList<Float>> Produit_Matriciel(ArrayList<ArrayList<Float>> T1, ArrayList<ArrayList<Float>>T2) {
        ArrayList<ArrayList<Float>> new_tab = new ArrayList<>();
        for (int N = 0; N < T1.size(); N++) {
            new_tab.add(new ArrayList<>());
            for (int J = 0; J < T2.get(0).size(); J++) {
                float count = 0;
                for (int X = 0; X < T1.get(0).size(); X++) {
                    count += T1.get(N).get(X) * T2.get(X).get(J);
                }
                new_tab.get(N).add(count);
            }
        }
        return new_tab;
    }

    private static float sigmoidPrime(float s) {
        return s * (1 - s);
    }

    private static ArrayList<ArrayList<Float>> SigmoidArray(ArrayList<ArrayList<Float>> tableau) {
        ArrayList<ArrayList<Float>> new_tab = new ArrayList<>();
        for (int y = 0; y < tableau.size(); y++) {
            new_tab.add(new ArrayList<>());
            for (float value: tableau.get(y)) {
                new_tab.get(y).add(sigmoid(value));
            }
        }
        return new_tab;
    }

    private static float sigmoid(float s) {
        return (1 / (1 + (float) Math.exp(-s)));
    }
}
