#include <stdio.h>
#include <stdlib.h>
#include <SDL.h>

int** create_matrice(int largeur, int hauteur) {

	int i;
	int** mat;

	mat = (int**)malloc(sizeof(int*) * hauteur);
	for (i = 0; i < hauteur; i++) {
		mat[i] = (int*)malloc(sizeof(int) * largeur);
	}

	return mat;
}

void initialisation_matrice(int** mat, int largeur, int hauteur) {
	int i, j;
	for (i = 0; i < hauteur; i++) {
		for (j = 0; j < largeur; j++) {
			mat[i][j] = rand() % 256;
		}
	}
}

SDL_Renderer* draw(SDL_Renderer* renderer, int** mat, int largeur, int hauteur, int size) {
	// Effacer l'écran avec une couleur noire
	SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
	SDL_RenderClear(renderer);

	int i, j, color;
	for (i = 0; i < hauteur; i++) {
		for (int j = 0; j < largeur; j++) {
			color = mat[i][j];
			SDL_SetRenderDrawColor(renderer, color, color, color, 255);
			SDL_Rect rect = { j * size, i * size, size, size };
			SDL_RenderFillRect(renderer, &rect);
		}
	}

	return renderer;
}

int valeurCase(int** mat, int largeur, int hauteur, int x, int y) {
	int somme = 0;
	int Xm1 = (x - 1 + largeur) % largeur;
	int Xp1 = (x + 1 + largeur) % largeur;
	int Ym1 = (y - 1 + hauteur) % hauteur;
	int Yp1 = (y + 1 + hauteur) % hauteur;

	somme += mat[Ym1][Xm1] + mat[Ym1][x] + mat[Ym1][Xp1];
	somme += mat[y][Xm1] + mat[y][x] + mat[y][Xp1];
	somme += mat[Yp1][Xm1] + mat[Yp1][x] + mat[Yp1][Xp1];
	return somme;
}

void generate_noise(int** initial, int** modif, int largeur, int hauteur) {
	int i, j;
	for (int i = 0; i < hauteur; i++) {
		for (int j = 0; j < largeur; j++) {
			modif[i][j] = valeurCase(initial, largeur, hauteur, j, i) / 9;
		}
	}
}


int main() {

	int largeur = 50, hauteur = 50, i;
	int size = 10;
	int afficherNoise = 1;
	int** alea;
	int** noise;

	alea = create_matrice(largeur, hauteur);
	initialisation_matrice(alea, largeur, hauteur);
	noise = create_matrice(largeur, hauteur);
	generate_noise(alea, noise, largeur, hauteur);

	// Initialisation de la SDL
	if (SDL_Init(SDL_INIT_VIDEO) != 0) {
		SDL_Log("Erreur lors de l'initialisation de la SDL : %s", SDL_GetError());
		return EXIT_FAILURE;
	}

	// Création de la fenêtre
	SDL_Window* window = SDL_CreateWindow("Game of Life",
		SDL_WINDOWPOS_CENTERED,
		SDL_WINDOWPOS_CENTERED,
		largeur * size, hauteur * size, 0);
	if (!window) {
		SDL_Log("Erreur lors de la création de la fenêtre : %s", SDL_GetError());
		SDL_Quit();
		return EXIT_FAILURE;
	}

	// Création du rendu
	SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	if (!renderer) {
		SDL_Log("Erreur lors de la création du rendu : %s", SDL_GetError());
		SDL_DestroyWindow(window);
		SDL_Quit();
		return EXIT_FAILURE;
	}

	// Attendre jusqu'à ce que l'utilisateur ferme la fenêtre
	int running = 1;
	SDL_Event event;
	while (running) {
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT) {
				running = 0;
			}
			else if (event.type == SDL_KEYDOWN) {
				if (event.key.keysym.sym == SDLK_SPACE) {
					if (afficherNoise) afficherNoise = 0;
					else afficherNoise = 1;
				}
			}
		}

		// Afficher le rendu
		if (afficherNoise) {
			renderer = draw(renderer, noise, largeur, hauteur, size);
		}
		else {
			renderer = draw(renderer, alea, largeur, hauteur, size);
		}
		SDL_RenderPresent(renderer);
	}

	// Libérer les ressources
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	SDL_Quit();

	return EXIT_SUCCESS;
}
