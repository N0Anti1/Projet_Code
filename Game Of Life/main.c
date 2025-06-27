#include <stdio.h>
#include <stdlib.h>
#include <SDL.h>


int** create_matrice1(int largeur, int hauteur) {
	
	int i;
	int** mat;

	mat = (int**)malloc(sizeof(int*) * hauteur);
	for (i = 0; i < hauteur; i++) {
		mat[i] = (int*)malloc(sizeof(int) * largeur);
	}

	return mat;
}

void initialisation_matrice1(int** mat, int largeur, int hauteur) {
	int i, j;
	for (i = 0; i < hauteur; i++) {
		for (j = 0; j < largeur; j++) {
			mat[i][j] = rand() % 2;
		}
	}
}

void afficher_matrice(int** mat, int largeur, int hauteur) {
	int i, j;
	for (i = 0; i < hauteur; i++) {
		for (j = 0; j < largeur; j++) {
			printf("%d", mat[i][j]);
		}
		printf("\n");
	}
}

int somme_cote(int** mat, int largeur, int hauteur, int x, int y) {
	int somme = 0;
	int Xm1 = (x - 1 + largeur) % largeur;
	int Xp1 = (x + 1 + largeur) % largeur;
	int Ym1 = (y - 1 + hauteur) % hauteur;
	int Yp1 = (y + 1 + hauteur) % hauteur;

	somme += mat[Ym1][Xm1] + mat[Ym1][x] + mat[Ym1][Xp1];
	somme += mat[y][Xm1] + mat[y][Xp1];
	somme += mat[Yp1][Xm1] + mat[Yp1][x] + mat[Yp1][Xp1];
	return somme;
}

void next_generation(int** mat, int** next, int largeur, int hauteur) {
	int i, j, nbVoisin;

	for (i = 0; i < hauteur; i++) {
		for (j = 0; j < largeur; j++) {
			nbVoisin = somme_cote(mat, largeur, hauteur, j, i);
			next[i][j] = 0;

			if (mat[i][j] == 0 && nbVoisin == 3) { next[i][j] = 1;}
			if (mat[i][j] == 1 && (nbVoisin == 2 || nbVoisin == 3)) { next[i][j] = 1;}
		}
	}
}

SDL_Renderer* draw1(SDL_Renderer* renderer, int** mat, int largeur, int hauteur, int zoom, int posX, int posY) {
	// Effacer l'écran avec une couleur noire
	SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
	SDL_RenderClear(renderer);

	int i, j;
	for (i = 0; i < hauteur; i++) {
		for (int j = 0; j < largeur; j++) {
			if (mat[i / zoom + posY][j / zoom + posX] == 0) {
				SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
			}
			else {
				SDL_SetRenderDrawColor(renderer, 0, 255, 255, 255);
			}
			SDL_RenderDrawPoint(renderer, j, i);
		}
	}

	return renderer;
}


int main1() {

	int largeur = 500, hauteur = 500, i;
	float zoom = 1.;
	int posX = 0, posY = 0;
	int time = 0;
	int** matrice;
	int** next;

	matrice = create_matrice(largeur, hauteur);
	initialisation_matrice(matrice, largeur, hauteur);
	next = create_matrice(largeur, hauteur);

	// Initialisation de la SDL
	if (SDL_Init(SDL_INIT_VIDEO) != 0) {
		SDL_Log("Erreur lors de l'initialisation de la SDL : %s", SDL_GetError());
		return EXIT_FAILURE;
	}

	// Création de la fenêtre
	SDL_Window* window = SDL_CreateWindow("Game of Life",
		SDL_WINDOWPOS_CENTERED,
		SDL_WINDOWPOS_CENTERED,
		largeur, hauteur, 0);
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
				if (event.key.keysym.sym == SDLK_ESCAPE) {
					running = 0;
				}
				else if (event.key.keysym.sym == SDLK_SPACE) {
					if (time) {
						time = 0;
					}
					else {
						time = 1;
					}
				}
				else if (event.key.keysym.sym == SDLK_r) {
					initialisation_matrice(matrice, largeur, hauteur);
				}
				else if (event.key.keysym.sym == SDLK_z && posY >= 0) {
					posY -= zoom;
					if (posY < 0) {
						posY = 0;
					}
				}
				else if (event.key.keysym.sym == SDLK_s && hauteur > hauteur / zoom + posY) {
					posY += zoom;
					if (posY >= hauteur) {
						posY = hauteur - 1;
					}
				}
				else if (event.key.keysym.sym == SDLK_q && posX > 0) {
					posX -= zoom;
					if (posX < 0) {
						posX = 0;
					}
				}
				else if (event.key.keysym.sym == SDLK_d && largeur > largeur / zoom + posX) {
					posX += zoom;
					if (posX >= largeur) {
						posX = largeur - 1;
					}
				}
			}
			else if (event.type == SDL_MOUSEWHEEL) {
				if (event.wheel.y > 0) {
					zoom*=1.4;
					if (zoom > 20) {
						zoom = 20;
					}
				}
				else if (event.wheel.y < 0) {
					zoom/=1.4;
					if (zoom < 1) {
						zoom = 1;
					}
					if (largeur / zoom + posX >= largeur) {
						posX = largeur - largeur / zoom;
					}
					if (hauteur / zoom + posY >= hauteur) {
						posY = hauteur - hauteur / zoom;
					}
				}
			}
		}
		if (time) {
			next_generation(matrice, next, largeur, hauteur);
			matrice = next;
		}
		renderer = draw(renderer, matrice, largeur, hauteur, zoom, posX, posY);
		// Afficher le rendu
		SDL_RenderPresent(renderer);
	}

	// Libérer les ressources
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	SDL_Quit();

	return EXIT_SUCCESS;
}
