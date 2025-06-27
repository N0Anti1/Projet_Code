#include <iostream>
#include <string>
#include <ctime>
#include <vector>

using namespace std;

class firstIA {
public:
	// Fonctions de la classe :
	vector<vector<vector<float>>> CreerTableau(int input, int hidden, int nb_hidden, int output); // Créer un tableau qui stock tout les poids du système
	void DisplayArray3D(vector<vector<vector<float>>> grid); // Affiche les poids du tableau
	float sigmoid(float x); // Calcule la sigmoid d'un nombre (valeur entre 0 et 1)
	float sigmoidPrime(float x); // Dérivée de la sigmoid (sensé)
	struct Neurone { // Neurone qui comporte des valeurs qui changent avec les entrées et les poids
		float value;
	};
	vector<vector<float>> ReduceValues(vector<vector<float>> entree, int nbInput);
	vector<vector<float>> Forward(vector<vector<float>> entree, bool predict);
	vector<vector<float>> ProduitMatriciel(vector<vector<float>> T1, vector<vector<float>> T2);
	vector<vector<float>> TSwap(vector<vector<float>> T1);
	void Backward(vector<vector<float>> obtenu, vector<vector<float>> attendu);
	vector<Neurone> updateInput(int iteration, bool predict) { // Remet les valeurs des Neurones à 0 ou sur la valeur d'entrée
		vector<Neurone> vec;
		vec.resize(inputSize + outputSize + nbHidden * hiddenSize, Neurone());
		for (int i = 0; i < vec.size(); i++) {
			if (i < inputSize) {
				if (predict) {
					vec[i].value = valeurPrediction[iteration][i];
				}
				else {
					vec[i].value = valeurEntree[iteration][i];
				}
			} else {
				vec[i].value = 0;
			}
		}
		return vec;
	}

	// Fonctions d'initialisation et de fin de programme
	void init() {
		srand(time(nullptr));
		cout << "creer tableau" << endl;
		AllWeight = CreerTableau(inputSize, hiddenSize, nbHidden, outputSize);
		cout << "display tableau" << endl;
		DisplayArray3D(AllWeight);
		valeurEntree = ReduceValues(valeurEntree, inputSize);
		vector<vector<float>> newEntree;
		newEntree.resize(valeurEntree.size() - 1, vector<float>(inputSize));
		for (int i = 0; i < valeurEntree.size(); i++) {
			if (i + 1 == valeurEntree.size()) {
				valeurPrediction.resize(1, vector<float>(inputSize));
				valeurPrediction[0].resize(inputSize, 0);
				for (int j = 0; j < inputSize; j++) {
					valeurPrediction[0][j] = valeurEntree[i][j];
				}
			}
			else {
				newEntree[i].resize(inputSize, 0);
				for (int j = 0; j < inputSize; j++) {
					newEntree[i][j] = valeurEntree[i][j];
				}
			}
		}
		valeurEntree = newEntree;
		cout << valeurEntree.size() << endl;

		valeurInput.resize(nbHidden, vector<vector<float>>(valeurEntree.size()));
		for (int i = 0; i < nbHidden; i++) {
			valeurInput[i].resize(valeurEntree.size(), vector<float>(hiddenSize));
			for (int j = 0; j < valeurEntree.size(); j++) {
				valeurInput[i][j].resize(hiddenSize, 0.0f);
			}
		}
	}
	void run(int boucle) {
		for (int i = 0; i < boucle; i++) {
			if (i % 5000 == 0)
				cout << "# " << i << endl;
			Backward(Forward(valeurEntree, false), valeurSortie);
		}
		DisplayArray3D(AllWeight);
		cout << "Sortie actuelle :" << endl;
		for (int j = 0; j < valeurSortie.size(); j++) {
			for (int k = 0; k < valeurSortie[j].size(); k++) {
				cout << valeurSortie[j][k];
			}
			cout << endl;
		}
		vector<vector<float>> result;
		result = Forward(valeurEntree, false);
		cout << "Sortie predite :" << endl;
		for (int j = 0; j < result.size(); j++) {
			for (int k = 0; k < result[j].size(); k++) {
				if (result[j][k] > 0.5) {
					cout << result[j][k] << " " << 1;
				}
				else {
					cout << result[j][k] << " " << 0;
				}
			}
			cout << endl;
		}
		vector<vector<float>> prediction;
		prediction = Forward(valeurPrediction, true);
		cout << "Prediction :" << endl;
		for (int j = 0; j < prediction.size(); j++) {
			for (int k = 0; k < prediction[j].size(); k++) {
				if (prediction[j][k] > 0.5) {
					cout << prediction[j][k] << " " << 1;
				}
				else {
					cout << prediction[j][k] << " " << 0;
				}
			}
			cout << endl;
		}
	}
	void clear() {
		cout << "Bye Bye" << endl;
	}

	// Constructeur :
	firstIA(int input, int hidden, int nbHidden, int output, vector<vector<float>> entree, vector<vector<float>> sortie);

private:
	int inputSize;
	int hiddenSize;
	int nbHidden;
	int outputSize;

	vector<vector<float>> valeurEntree; // tableau de (x+1)*inputSize
	vector<vector<float>> valeurPrediction;
	vector<vector<float>> valeurSortie; // tableau de x*outputSize
	vector<vector<vector<float>>> valeurInput;

	vector<vector<vector<float>>> AllWeight;
	vector<Neurone> allNeurones;
};
