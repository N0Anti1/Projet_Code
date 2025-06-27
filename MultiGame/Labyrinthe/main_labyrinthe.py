import pygame
from random import random, randint, choice


class Laby_2000:

    def __init__(self):
        pygame.init()

        self.image_icon = pygame.image.load('../Labyrinthe/Laby_icon.png')

        self.screen = pygame.display.set_mode((0, 0))
        pygame.display.set_caption("Laby 2000")
        pygame.display.set_icon(self.image_icon)

        self.running = True
        self.HAUTEUR = 31
        self.LARGEUR = 51
        self.SIZE = int(self.screen.get_height() / self.HAUTEUR)
        self.LEFT = (self.screen.get_width() - self.LARGEUR * self.SIZE) / 2
        self.TOP = (self.screen.get_height() - self.HAUTEUR * self.SIZE) / 2
        if self.LEFT < 0:
            self.SIZE = int(self.screen.get_width() / self.LARGEUR)
            self.LEFT = (self.screen.get_width() - self.LARGEUR * self.SIZE) / 2
            self.TOP = (self.screen.get_height() - self.HAUTEUR * self.SIZE) / 2

        # self.LABYRINTHE #
        self.lab = []
        self.val = []
        self.wall = []
        self.lab_fini = False
        self.show_lab = True
        # Sur la gauche ==> x = 0 et y = impair // Sur le haut ==> x = impair et y = 0
        # Sur la droite ==> x = LARGEUR - 1 et y = HAUTEUR - pair // Sur le bas ==> x = LARGEUR - pair et y = HAUTEUR - 1
        self.depart = (0, 1)
        self.arrivee = (self.LARGEUR - 1, self.HAUTEUR - 2)
        self.couleur_background = (0, 0, 0)

        self.creer = False

        # RESOUDRE PLAYER #
        self.case_player = [self.depart]
        self.fini_resolve = False

        # RESOUDRE IA #
        self.case_IA = [self.arrivee]
        self.case_lab = []
        self.path_finder = False
        self.path = [self.depart]

        self.init_lab()

    # Créer les tableaux pour initialiser mon labyrinthe
    def init_lab(self):
        for x in range(self.LARGEUR):
            for y in range(self.HAUTEUR):
                if x % 2 == y % 2 == 1:
                    self.lab.append((x, y))
                    self.val.append((randint(0, 255), randint(0, 255), randint(0, 255)))
                elif x % 2 != y % 2 and 0 < x < self.LARGEUR - 1 and 0 < y < self.HAUTEUR - 1:
                    self.wall.append((x, y))

    # Dessine la grille de mon labyrinthe
    def draw_lab(self):
        for x in range(self.LARGEUR):
            for y in range(self.HAUTEUR):
                # Dessine le chemin du laby
                if (x, y) in self.lab:
                    pygame.draw.rect(self.screen, self.val[self.lab.index((x, y))], (self.LEFT + x * self.SIZE, self.TOP + y * self.SIZE, self.SIZE, self.SIZE))

    # Une deuxième fonction pour afficher le chemin que réalise le joueur en augmentant les FPS
    # par rapport à la première fonction
    def draw_pas_tout_le_lab(self):
        # Dessine les murs une fois le laby fini
        for index in self.wall:
            pygame.draw.rect(self.screen, (0, 0, 0), (self.LEFT + index[0] * self.SIZE, self.TOP + index[1] * self.SIZE, self.SIZE, self.SIZE))
        # Dessine l'arrivée du laby
        pygame.draw.rect(self.screen, (0, 255, 255), (self.LEFT + self.arrivee[0] * self.SIZE, self.TOP + self.arrivee[1] * self.SIZE, self.SIZE, self.SIZE))
        # Dessine le chemin du joueur
        for index in self.case_player:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.LEFT + index[0] * self.SIZE, self.TOP + index[1] * self.SIZE, self.SIZE, self.SIZE))
        # Dessine le chemin le plus court à la fin
        if self.fini_resolve:
            for index in self.path:
                pygame.draw.rect(self.screen, (255, 255, 0), (self.LEFT + index[0] * self.SIZE, self.TOP + index[1] * self.SIZE, self.SIZE, self.SIZE))

    # Regardes les toutes les cases autour d'une case initial et colorie les cases qui font partie du laby
    def look_around(self, x, y, couleur):
        for i in range(3):
            for j in range(3):
                if (x + i - 1, y + j - 1) in self.lab:
                    if self.val[self.lab.index((x + i - 1, y + j - 1))] != couleur:
                        self.val[self.lab.index((x + i - 1, y + j - 1))] = couleur
                        self.look_around(x + i - 1, y + j - 1, couleur)

    # Casse les murs pour créer mon laby
    def casse_mur(self):
        mur_x, mur_y = choice(self.wall)
        case = []

        # Récupère quel mur casser
        if (mur_x, mur_y - 1) in self.lab and (mur_x, mur_y + 1) in self.lab:
            case.append((mur_x, mur_y - 1))
            case.append((mur_x, mur_y + 1))
        elif (mur_x - 1, mur_y) in self.lab and (mur_x + 1, mur_y) in self.lab:
            case.append((mur_x - 1, mur_y))
            case.append((mur_x + 1, mur_y))

        # Choisi la nouvelle couleur pour les cases associées
        if self.val[self.lab.index(case[0])] != self.val[self.lab.index(case[1])]:
            nombre1 = self.val.count(self.val[self.lab.index(case[0])])
            nombre2 = self.val.count(self.val[self.lab.index(case[1])])
            pourcentage = random()
            if pourcentage < nombre1 / (nombre1 + nombre2):
                nouvelle_couleur = self.val[self.lab.index(case[0])]
            else:
                nouvelle_couleur = self.val[self.lab.index(case[1])]
            self.wall.remove((mur_x, mur_y))
            self.lab.append((mur_x, mur_y))
            self.val.append(nouvelle_couleur)
            self.look_around(mur_x, mur_y, nouvelle_couleur)
        else:
            self.wall.remove((mur_x, mur_y))

    def wall_recup(self):
        # Supprime des murs à la fin pour complexifier le laby (avec un rapport de 1 mur cassé pour 100 cases)
        for _ in range(int(self.LARGEUR * self.HAUTEUR / 100)):
            self.remove_wall = choice(self.wall)
            self.lab.append(self.remove_wall)
            self.val.append(self.val[0])
            self.wall.remove(self.remove_wall)
        self.wall.clear()

        # Récupère tous les murs dans la variable 'wall'
        for x in range(self.LARGEUR):
            for y in range(self.HAUTEUR):
                if (x, y) not in self.lab:
                    self.wall.append((x, y))
                else:
                    self.case_lab.append(self.LARGEUR * self.HAUTEUR)
        self.case_lab[self.lab.index(self.arrivee)] = 0

    # Créer le chemin du joueur en suivant sa souris
    def resolve_player(self, x, y):
        if (x, y) in self.lab and (x, y) not in self.case_player:
            if (x - 1, y) == self.case_player[-1] or (x + 1, y) == self.case_player[-1]:
                self.case_player.append((x, y))
            elif (x, y - 1) == self.case_player[-1] or (x, y + 1) == self.case_player[-1]:
                self.case_player.append((x, y))

    # Retourne en arrière dans le chemin en clicant à l'endroit voulu
    def return_player(self, x, y):
        if (x, y) in self.case_player:
            index = self.case_player.index((x, y))
            while index + 1 != len(self.case_player):
                self.case_player.pop()

    # Prépare le chemin en associant à chaque case une valeur qui augmente en s'éloignant de l'arrivée
    def resolve_IA(self):
        for case in self.case_IA:
            actual_number = self.case_lab[self.lab.index(case)]
            if (case[0] - 1, case[1]) in self.lab and (case[0] - 1, case[1]) not in self.case_IA:
                self.case_IA.append((case[0] - 1, case[1]))
                self.case_lab[self.lab.index((case[0] - 1, case[1]))] = actual_number + 1
            if (case[0] + 1, case[1]) in self.lab and (case[0] + 1, case[1]) not in self.case_IA:
                self.case_IA.append((case[0] + 1, case[1]))
                self.case_lab[self.lab.index((case[0] + 1, case[1]))] = actual_number + 1
            if (case[0], case[1] - 1) in self.lab and (case[0], case[1] - 1) not in self.case_IA:
                self.case_IA.append((case[0], case[1] - 1))
                self.case_lab[self.lab.index((case[0], case[1] - 1))] = actual_number + 1
            if (case[0], case[1] + 1) in self.lab and (case[0], case[1] + 1) not in self.case_IA:
                self.case_IA.append((case[0], case[1] + 1))
                self.case_lab[self.lab.index((case[0], case[1] + 1))] = actual_number + 1

    # Suit les valeurs qui diminues jusqu'à l'arrivé et dessine le chemin idéal
    def pathfinder(self):
        path_x, path_y = self.path[-1]
        valeur_min = self.LARGEUR * self.HAUTEUR
        case_min = ()
        if (path_x - 1, path_y) in self.case_IA:
            if self.case_lab[self.lab.index((path_x - 1, path_y))] < valeur_min:
                valeur_min = self.case_lab[self.lab.index((path_x - 1, path_y))]
                case_min = (path_x - 1, path_y)
        if (path_x + 1, path_y) in self.case_IA:
            if self.case_lab[self.lab.index((path_x + 1, path_y))] < valeur_min:
                valeur_min = self.case_lab[self.lab.index((path_x + 1, path_y))]
                case_min = (path_x + 1, path_y)
        if (path_x, path_y - 1) in self.case_IA:
            if self.case_lab[self.lab.index((path_x, path_y - 1))] < valeur_min:
                valeur_min = self.case_lab[self.lab.index((path_x, path_y - 1))]
                case_min = (path_x, path_y - 1)
        if (path_x, path_y + 1) in self.case_IA:
            if self.case_lab[self.lab.index((path_x, path_y + 1))] < valeur_min:
                case_min = (path_x, path_y + 1)
        if case_min != ():
            self.path.append(case_min)

    # Créer le labyrinthe rapidement
    def creation_rapide(self):
        while self.val.count(self.val[0]) != len(self.val):
            self.casse_mur()

    def run(self):
        while self.running:
            self.screen.fill(self.couleur_background)

            # Récupère les évènements
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    # Touche 'a' pour la création rapide du labyrinthe
                    elif event.key == pygame.K_a and not self.creer:
                        self.creation_rapide()
                        self.lab.append(self.depart)
                        self.val.append(self.val[0])
                        self.lab.append(self.arrivee)
                        self.val.append(self.val[0])
                        self.wall_recup()
                        self.lab_fini = True
                        self.creer = True
                        self.couleur_background = self.val[0]
                    # Touche 'espace' pour créer le labyrinthe
                    if event.key == pygame.K_SPACE and not self.creer:
                        self.creer = True
                    # Touche 'r' pour réinitialiser le labyrinthe
                    if event.key == pygame.K_r:
                        # self.LABYRINTHE #
                        self.lab = []
                        self.val = []
                        self.wall = []
                        self.lab_fini = False
                        self.show_lab = True
                        self.creer = False
                        self.init_lab()
                        self.couleur_background = (0, 0, 0)

                        # RESOUDRE PLAYER #
                        self.case_player = [self.depart]
                        self.fini_resolve = False

                        # RESOUDRE IA #
                        self.case_IA = [self.arrivee]
                        self.case_lab = []
                        self.path_finder = False
                        self.path = [self.depart]
                # Clic gauche de la souris pour revenir en arrière sur le chemin
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.fini_resolve and self.creer:
                    if event.button == pygame.BUTTON_LEFT:
                        clic_x, clic_y = event.pos
                        clic_x -= self.LEFT
                        clic_y -= self.TOP
                        clic_x //= self.SIZE
                        clic_y //= self.SIZE
                        self.return_player(clic_x, clic_y)

            # Au début, créer le laby en cassant les murs
            if self.val.count(self.val[0]) != len(self.val) and not self.lab_fini and self.creer:
                self.casse_mur()
            # Fait apparître l'entrée et la sortie
            elif not self.lab_fini and self.creer:
                self.lab.append(self.depart)
                self.val.append(self.val[0])
                self.lab.append(self.arrivee)
                self.val.append(self.val[0])
                self.wall_recup()
                self.lab_fini = True
                self.couleur_background = self.val[0]
            # Fait le chemin en suivant la souris du joueur
            elif not self.fini_resolve and self.creer:
                pos_x, pos_y = pygame.mouse.get_pos()
                pos_x -= self.LEFT
                pos_y -= self.TOP
                pos_x //= self.SIZE
                pos_y //= self.SIZE
                self.resolve_player(pos_x, pos_y)
                if self.arrivee in self.case_player:
                    self.fini_resolve = True
                    self.path_finder = True
            # Créer la solution (invisible)
            elif self.path_finder:
                self.resolve_IA()
                if self.depart in self.case_IA:
                    self.path_finder = False
            # Dessine la solution une fois qu'elle a été trouvé
            else:
                self.pathfinder()

            if not self.lab_fini:
                self.draw_lab()
            else:
                self.draw_pas_tout_le_lab()
            pygame.display.flip()

        pygame.quit()

