#include <iostream>
#include "firstIA.h"


int main() {

	vector<vector<float>> entree = { {3.0f, 1.5f}, {2.0f, 1.0f}, {4.0f, 1.5f}, {3.0f, 1.0f}, {3.5f, 0.5f}, {2.0f, 0.5f}, {5.5f, 1.06f}, {3.2f, 1.4f} };
	vector<vector<float>> sortie = { {1.0f}, {0.0f}, {1.0f}, {0.0f}, {1.0f}, {0.0f}, {1.0f} };
	// vector<vector<float>> sortie = { {1.0f, 1.5f}, {0.0f, 0.3f}, {1.0f, 1.5f}, {0.0f, 0.4f}, {1.0f, 2.0f}, {0.0f, 0.5f}, {1.0f, 1.62f} };

	firstIA ia(2, 3, 1, 1, entree, sortie);
	ia.run(500000);

	std::cout << "end" << std::endl;
	std::cin.ignore();
	ia.clear();
	return 0;
}
