#include "firstIA.h"
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
using namespace std;

firstIA::firstIA(int input, int hidden, int nbHidden, int output, vector<vector<float>> entree, vector<vector<float>> sortie) {
	this->inputSize = input;
	this->hiddenSize = hidden;
	this->nbHidden = nbHidden;
	this->outputSize = output;
	this->valeurEntree = entree;
	this->valeurSortie = sortie;
	this->init();
}

vector<vector<vector<float>>> firstIA::CreerTableau(int input, int hidden, int nb_hidden, int output) {
	vector<vector<vector<float>>> vec(1 + nb_hidden);
	vector<int> column(nb_hidden + 1, hidden);
	column[0] = input;
	// On a un tableau qui stock tous les poids :
	// tab = {						// tableau de nb_hidden (2) + 1 x entree (input ou hidden) x sortie (hidden ou output)
	//    {
	//       {0.3, 0.62, 0.53},		// Sur la premi�re couche il y a 2 entr�es et 3 neurones cach�s
	//       {0.08, 0.27, 0.17}		// tableau de 2x3
	//    },
	//    {
	//       {0.25, 0.15, 0.86},	// Sur la deuxi�me couche il y a 3 neurones cach�s puis 3 neurones cach�s
	//       {0.10, 0.50, 0.30},	// tableau de 3x3
	//       {0.96, 0.50, 0.41}
	//    },
	//    {
	//       {0.05},				// Sur la derni�re couche il y a 3 neurones cach�s et 1 neurone de sortie
	//       {0.54},				// tableau de 3x1
	//       {0.55}
	//    }
	// }

	for (int i = 0; i < 1 + nb_hidden; i++) {
		int col = column[i];

		vec[i] = vector<vector<float>>(col);
		for (int j = 0; j < col; j++) {
			if (i != nb_hidden) {
				vec[i][j] = vector<float>(hidden);
				for (int a = 0; a < hidden; a++) {
					float valeur = float(rand()) / float(RAND_MAX);
					vec[i][j][a] = valeur;
				}
			}
			else {
				vec[i][j] = vector<float>(output);
				for (int a = 0; a < output; a++) {
					float valeur = float(rand()) / float(RAND_MAX);
					vec[i][j][a] = valeur;
				}
			}
		}
	}
	return vec;
}

void firstIA::DisplayArray3D(vector<vector<vector<float>>> grid) {
	for (int i = 0; i < grid.size(); i++) { // Couche de poids
		for (int j = 0; j < grid[i].size(); j++) { // Nombre d'input
			for (int a = 0; a < grid[i][j].size(); a++) { // Nombre d'output
				cout << grid[i][j][a] << " " << i << " " << j << " " << a << endl;
			}
		}
	}
}
vector<vector<float>> firstIA::ReduceValues(vector<vector<float>> entree, int nbInput) {
	vector<float> maxValue;
	maxValue.resize(nbInput, 0);
	for (int i = 0; i < entree.size(); i++) {
		for (int j = 0; j < entree[i].size(); j++) {
			if (entree[i][j] > maxValue[j]) {
				maxValue[j] = entree[i][j];
			}
		}
	}
	vector<vector<float>> vec(entree.size());
	for (int i = 0; i < vec.size(); i++) {
		vec[i].resize(nbInput, 0);
		for (int j = 0; j < nbInput; j++) {
			vec[i][j] = entree[i][j] / maxValue[j];
		}
	}
	return vec;
}
float firstIA::sigmoid(float x) {
	return 1 / (1 + exp(-x));
}
float firstIA::sigmoidPrime(float x) {
	return x * (1 - x);
}

vector<vector<float>> firstIA::Forward(vector<vector<float>> entree, bool predict) { // Fonction qui va pour chaque valeur du tableau d'entr�e calculer la valeur qui en ressort :
	// cout << endl << endl << "forward :" << endl;
	vector<vector<float>> result;
	if (predict) {
		result.resize(this->valeurPrediction.size(), vector<float>());
	}
	else {
		result.resize(this->valeurSortie.size(), vector<float>());
	}
	for (int i = 0; i < result.size(); i++) {
		result[i].resize(this->outputSize, 0);
	}

	for (int iteration = 0; iteration < entree.size(); iteration++) {
		vector<Neurone> allNeurone;
		allNeurone = this->updateInput(iteration, predict);
		// On calcule pour chaque input la valeur de chaque hidden et on l'ajoute au Neurone hidden :
		for (int nbSortie = 0; nbSortie < this->outputSize; nbSortie++) {
			for (int couche = 0; couche < this->AllWeight.size(); couche++) {
				for (int input = 0; input < this->AllWeight[couche].size(); input++) {
					for (int output = 0; output < this->AllWeight[couche][input].size(); output++) {
						// input										 == neurone d'entr�e de la connexion (couche = 0)
						// input + inputSize + (couche - 1) * hiddenSize == neurone d'entr�e de la connexion (couche > 0)
						// output + inputSize						== neurone d'arriv� de la connexion (couche = 0)
						// output + inputSize + couche * hiddenSize == neurone d'arriv� de la connexion (couche > 0)
						// input + hiddenSize * couche == neurone d'arriv� de la connexion
						// this->AllWeight[couche][input][output] == poid de la connexion
						if (couche == 0) {
							allNeurone[output + this->inputSize].value +=
								this->sigmoid(allNeurone[input].value) * this->AllWeight[couche][input][output];
						}
						else {
							allNeurone[output + this->inputSize + couche * this->hiddenSize].value +=
								this->sigmoid(allNeurone[input + this->inputSize + (couche - 1) * this->hiddenSize].value) *
								this->AllWeight[couche][input][output];
						}
						// cout << allNeurone[input + this->hiddenSize * couche].value << " " << couche << input << output << endl;
					}
				}
			}
			for (int i = this->inputSize; i < allNeurone.size() - this->outputSize; i++) {
				// cout << (i - this->inputSize) / this->hiddenSize << " " << (i - this->inputSize) % this->hiddenSize << endl;
				this->valeurInput[(i - this->inputSize) / this->hiddenSize][iteration][(i - this->inputSize) % this->hiddenSize] =
					this->sigmoid(allNeurone[i].value);
			}
			// Le tableau allNeurone contient les valeurs de sorties.
			// cout << allNeurone[allNeurone.size() - 1].value << this->sigmoid(allNeurone[allNeurone.size() - 1].value) << endl;
			result[iteration][nbSortie] = this->sigmoid(allNeurone[allNeurone.size() - 1].value);
		}
	}
	return result;
}
vector<vector<float>> firstIA::ProduitMatriciel(vector<vector<float>> T1, vector<vector<float>> T2) {
	// T1 = [[A1, A2], [A3, A4], [A5, A6]] == N - X(N = inconnu, X = nombre d'entr�e)
	// T2 = [[B1, B2, B3], [B4, B5, B6]] == X - J(X = nombre d'entr�e, J = nb neurone �tape suivante)
	// R�sultat = [[A1 * B1 + A2 * B4, A1 * B2 + A2 * B5, A1 * B3 + A2 * B6], [A3 ET A4], [A5 ET A6]] = N * J
	int N = T1.size();
	int X = T2.size();
	int J = T2[0].size();
	bool Error = false;
	for (int n = 0; n < N; n++) {
		if (T1[n].size() != X)
			Error = true;
	}
	for (int x = 0; x < X; x++) {
		if (T2[x].size() != J)
			Error = true;
	}
	if (Error) {
		cout << "Erreur dans le Produit Matriciel, les tableaux ne correspondent pas." << endl;
		return vector<vector<float>>();
	}
	vector<vector<float>> vec(N);
	for (int i = 0; i < N; i++) {
		vec[i].resize(J, 0);
	}
	for (int n = 0; n < N; n++) { // 3
		for (int j = 0; j < J; j++) { // 3
			float count = 0;
			for (int x = 0; x < X; x++) { // 2
				count += T1[n][x] * T2[x][j];
			}
			vec[n][j] = count;
		}
	}
	return vec;
}
vector<vector<float>> firstIA::TSwap(vector<vector<float>> T1) {
	// T1 = [[A1, A2], [A3, A4], [A5, A6]] == N - X
	// R�sultat = [[A1, A3, A5], [A2, A4, A6]] = X - N
	int N = T1.size();
	int X = T1[0].size();
	bool Error = false;
	for (int n = 0; n < N; n++) {
		if (T1[n].size() != X)
			Error = true;
	}
	if (Error) {
		cout << "Erreur dans le Produit Matriciel, les tableaux ne correspondent pas." << endl;
		return vector<vector<float>>();
	}
	vector<vector<float>> vec(X);
	for (int i = 0; i < vec.size(); i++) {
		vec[i].resize(N);
	}
	for (int x = 0; x < X; x++) {
		for (int n = 0; n < N; n++) {
			vec[x][n] = T1[n][x];
		}
	}
	return vec;
}
void firstIA::Backward(vector<vector<float>> obtenu, vector<vector<float>> attendu) {
	// On part de la fin et on remonte dans le r�seau :
	for (int poids = this->nbHidden; poids >= 0; poids--) {
		// On calcul l'erreur Delta de la sortie des poids :
		vector<vector<float>> erreurDelta(this->valeurEntree.size());
		for (int i = 0; i < erreurDelta.size(); i++) {
			erreurDelta[i].resize(this->outputSize, 0.0f);
		}
		for (int iteration = 0; iteration < this->valeurEntree.size(); iteration++) {
			for (int sortie = 0; sortie < this->outputSize; sortie++) {
				erreurDelta[iteration][sortie] = (attendu[iteration][sortie] - obtenu[iteration][sortie]) * this->sigmoidPrime(obtenu[iteration][sortie]);
			}
		}
		if (poids != this->nbHidden) {
			for (int back = this->nbHidden; back > poids; back--) {
				erreurDelta = this->ProduitMatriciel(erreurDelta, this->TSwap(this->AllWeight[back]));
				for (int i = 0; i < erreurDelta.size(); i++) {
					for (int j = 0; j < erreurDelta[i].size(); j++) {
						erreurDelta[i][j] = erreurDelta[i][j] * this->sigmoidPrime(this->valeurInput[poids][i][j]);
					}
				}
			}
		}

		// Puis on fait le Produit Matriciel de l'erreur Delta avec les neurones d'entr�es :
		vector<vector<float>> calculAjoutPoid;
		if (poids != 0) {
			calculAjoutPoid = this->ProduitMatriciel(this->TSwap(this->valeurInput[poids - 1]), erreurDelta);
		}
		else {
			calculAjoutPoid = this->ProduitMatriciel(this->TSwap(this->valeurEntree), erreurDelta);
		}
		for (int i = 0; i < this->AllWeight[poids].size(); i++) {
			for (int j = 0; j < this->AllWeight[poids][i].size(); j++) {
				this->AllWeight[poids][i][j] += calculAjoutPoid[i][j];
			}
		}
	}
}
