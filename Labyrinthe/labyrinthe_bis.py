import pygame
from random import choice, randint


class Labyrinthe_Etoile:

    def __init__(self):
        pygame.init()

        self.image_icon = pygame.image.load('../Labyrinthe/Laby_icon.png')
        self.screen = pygame.display.set_mode((0, 0))
        pygame.display.set_caption("Labyrinthe Étoile")
        pygame.display.set_icon(self.image_icon)

        self.running = True
        self.HAUTEUR = 30
        self.LARGEUR = 50
        self.SIZE = int(self.screen.get_height() / self.HAUTEUR)
        self.LINE = int(self.SIZE / 8)
        self.LEFT = (self.screen.get_width() - self.LARGEUR * self.SIZE) / 2
        self.TOP = (self.screen.get_height() - self.HAUTEUR * self.SIZE) / 2
        if self.LEFT < 0:
            self.SIZE = int(self.screen.get_width() / self.LARGEUR)
            self.LEFT = (self.screen.get_width() - self.LARGEUR * self.SIZE) / 2
            self.TOP = (self.screen.get_height() - self.HAUTEUR * self.SIZE) / 2

        # LABYRINTHE #
        self.index_case = []
        self.valeur_sud = []
        self.valeur_est = []
        self.depart = (randint(0, int(self.LARGEUR / 2)), randint(0, self.HAUTEUR - 1))
        self.arrivee = (randint(int(self.LARGEUR / 2), self.LARGEUR - 1), randint(0, self.HAUTEUR - 1))
        self.chemin = [self.depart]
        self.lab = [self.depart]
        self.create = False
        self.menu = True

        self.couleur_background = (randint(0, 255), randint(0, 255), randint(0, 255))

        # PLAYER #
        self.case_player = [self.depart]
        self.resoudre = False

        # RESOUDRE IA #
        self.case_IA = [self.arrivee]
        self.case_lab = []
        self.create_path = False
        self.path_finder = False
        self.path = [self.depart]

        self.init_lab()

    # Initialise le labyrinthe en remplissant les tableaus de murs 'Sud' et 'Est'
    def init_lab(self):
        for t in range(self.LARGEUR):
            for h in range(self.HAUTEUR):
                self.index_case.append((t, h))
                self.valeur_sud.append(True)
                self.valeur_est.append(True)
                self.case_lab.append(self.LARGEUR * self.HAUTEUR)

    # Dessine le labyrinthe
    def draw_lab(self):
        for x in range(self.LARGEUR):
            for y in range(self.HAUTEUR):
                pygame.draw.rect(self.screen, self.couleur_background, (self.LEFT + x * self.SIZE + self.LINE, self.TOP + y * self.SIZE + self.LINE, self.SIZE, self.SIZE))

                # Dessine la tête qui créer le laby
                if (x, y) == self.chemin[-1]:
                    pygame.draw.rect(self.screen, (255, 255, 0), (self.LEFT + x * self.SIZE + self.LINE, self.TOP + y * self.SIZE + self.LINE, self.SIZE, self.SIZE))

                # Dessine l'arrivé du laby en le self.chemin du joueur
                if (x, y) == self.arrivee:
                    pygame.draw.rect(self.screen, (0, 255, 255), (self.LEFT + x * self.SIZE + self.LINE, self.TOP + y * self.SIZE + self.LINE, self.SIZE, self.SIZE))
                if (x, y) in self.case_player and not self.create and (self.resoudre or self.path_finder):
                    pygame.draw.rect(self.screen, (255, 0, 0), (self.LEFT + x * self.SIZE + self.LINE, self.TOP + y * self.SIZE + self.LINE, self.SIZE, self.SIZE))

                # Dessine la solution de l'IA
                if (x, y) in self.path and self.path_finder:
                    pygame.draw.rect(self.screen, (255, 255, 0), (self.LEFT + x * self.SIZE + self.LINE, self.TOP + y * self.SIZE + self.LINE, self.SIZE, self.SIZE))

                # Dessine les murs
                pygame.draw.rect(self.screen, (0, 0, 0), (self.LEFT + (x + 1) * self.SIZE, self.TOP + (y + 1) * self.SIZE, self.LINE, self.LINE))
                if self.valeur_sud[self.index_case.index((x, y))]:
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     (self.LEFT + x * self.SIZE + self.LINE, self.TOP + (y + 1) * self.SIZE + self.LINE / 2),
                                     (self.LEFT + (x + 1) * self.SIZE, self.TOP + (y + 1) * self.SIZE + self.LINE / 2), self.LINE)
                if self.valeur_est[self.index_case.index((x, y))]:
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     (self.LEFT + (x + 1) * self.SIZE + self.LINE / 2, self.TOP + y * self.SIZE + self.LINE),
                                     (self.LEFT + (x + 1) * self.SIZE + self.LINE / 2, self.TOP + (y + 1) * self.SIZE), self.LINE)

    # Créer le laby en choisissant la direction où aller et en "cassant" le mur qui est au milieu
    def create_lab(self):
        co_x, co_y = self.chemin[-1]
        destination_possible = []
        if (co_x - 1, co_y) not in self.lab and co_x - 1 >= 0:
            destination_possible.append("GAUCHE")
        if (co_x + 1, co_y) not in self.lab and co_x + 1 < self.LARGEUR:
            destination_possible.append("DROITE")
        if (co_x, co_y - 1) not in self.lab and co_y - 1 >= 0:
            destination_possible.append("HAUT")
        if (co_x, co_y + 1) not in self.lab and co_y + 1 < self.HAUTEUR:
            destination_possible.append("BAS")

        if len(destination_possible) != 0:
            destination = choice(destination_possible)
            if destination == "GAUCHE":
                self.valeur_est[self.index_case.index((co_x - 1, co_y))] = False
                self.chemin.append((co_x - 1, co_y))
                self.lab.append((co_x - 1, co_y))
            elif destination == "DROITE":
                self.valeur_est[self.index_case.index((co_x, co_y))] = False
                self.chemin.append((co_x + 1, co_y))
                self.lab.append((co_x + 1, co_y))
            elif destination == "HAUT":
                self.valeur_sud[self.index_case.index((co_x, co_y - 1))] = False
                self.chemin.append((co_x, co_y - 1))
                self.lab.append((co_x, co_y - 1))
            elif destination == "BAS":
                self.valeur_sud[self.index_case.index((co_x, co_y))] = False
                self.chemin.append((co_x, co_y + 1))
                self.lab.append((co_x, co_y + 1))
        else:
            self.chemin.pop()

    # Supprime des murs au hasard du laby
    def cut_lab(self):
        for i in range(int(self.LARGEUR * self.HAUTEUR / 20)):
            if i % 2 == 0:
                index = randint(0, len(self.valeur_sud) - 1)
                if self.index_case[index][1] != self.HAUTEUR - 1:
                    self.valeur_sud[index] = False
            else:
                index = randint(0, len(self.valeur_est) - 1)
                if self.index_case[index][0] != self.LARGEUR - 1:
                    self.valeur_est[index] = False
        self.case_lab[self.lab.index(self.arrivee)] = 0

    # Créer le self.chemin du joueur en suivant sa souris
    def resolve_player(self, x, y):
        if (x, y) not in self.case_player:
            # Aller à gauche
            if (x + 1, y) == self.case_player[-1] and (self.case_player[-1][0] - 1, self.case_player[-1][1]) in self.lab:
                if not self.valeur_est[self.index_case.index((self.case_player[-1][0] - 1, self.case_player[-1][1]))]:
                    self.case_player.append((self.case_player[-1][0] - 1, self.case_player[-1][1]))
            # Aller à droite
            if (x - 1, y) == self.case_player[-1] and (self.case_player[-1][0] + 1, self.case_player[-1][1]) in self.lab:
                if not self.valeur_est[self.index_case.index(self.case_player[-1])]:
                    self.case_player.append((self.case_player[-1][0] + 1, self.case_player[-1][1]))
            # Aller en haut
            if (x, y + 1) == self.case_player[-1] and (self.case_player[-1][0], self.case_player[-1][1] - 1) in self.lab:
                if not self.valeur_sud[self.index_case.index((self.case_player[-1][0], self.case_player[-1][1] - 1))]:
                    self.case_player.append((self.case_player[-1][0], self.case_player[-1][1] - 1))
            # Aller en bas
            if (x, y - 1) == self.case_player[-1] and (self.case_player[-1][0], self.case_player[-1][1] + 1) in self.lab:
                if not self.valeur_sud[self.index_case.index(self.case_player[-1])]:
                    self.case_player.append((self.case_player[-1][0], self.case_player[-1][1] + 1))

    # Permet au joueur de revenir en arrière quand il s'est trompé
    def return_player(self, x, y):
        if (x, y) in self.case_player:
            index = self.case_player.index((x, y))
            while index + 1 != len(self.case_player):
                self.case_player.pop()

    # Prépare le chemin en associant à chaque case une valeur qui augmente en s'éloignant de l'arrivée
    def resolve_IA(self):
        for case in self.case_IA:
            actual_number = self.case_lab[self.lab.index(case)]
            # Aller à gauche
            if (case[0] - 1, case[1]) in self.lab and (case[0] - 1, case[1]) not in self.case_IA:
                if not self.valeur_est[self.index_case.index((case[0] - 1, case[1]))]:
                    self.case_IA.append((case[0] - 1, case[1]))
                    self.case_lab[self.lab.index((case[0] - 1, case[1]))] = actual_number + 1
            # Aller à droite
            if (case[0] + 1, case[1]) in self.lab and (case[0] + 1, case[1]) not in self.case_IA:
                if not self.valeur_est[self.index_case.index(case)]:
                    self.case_IA.append((case[0] + 1, case[1]))
                    self.case_lab[self.lab.index((case[0] + 1, case[1]))] = actual_number + 1
            # Aller en haut
            if (case[0], case[1] - 1) in self.lab and (case[0], case[1] - 1) not in self.case_IA:
                if not self.valeur_sud[self.index_case.index((case[0], case[1] - 1))]:
                    self.case_IA.append((case[0], case[1] - 1))
                    self.case_lab[self.lab.index((case[0], case[1] - 1))] = actual_number + 1
            # Aller en bas
            if (case[0], case[1] + 1) in self.lab and (case[0], case[1] + 1) not in self.case_IA:
                if not self.valeur_sud[self.index_case.index(case)]:
                    self.case_IA.append((case[0], case[1] + 1))
                    self.case_lab[self.lab.index((case[0], case[1] + 1))] = actual_number + 1

    # Suit les valeurs qui diminues jusqu'à l'arrivé et dessine le self.chemin idéal
    def pathfinder(self):
        path_x, path_y = self.path[-1]
        valeur_min = self.case_lab[self.lab.index((path_x, path_y))]
        case_min = ()
        # Aller à gauche
        if (path_x - 1, path_y) in self.case_IA:
            if not self.valeur_est[self.index_case.index((path_x - 1, path_y))]:
                if self.case_lab[self.lab.index((path_x - 1, path_y))] < valeur_min:
                    valeur_min = self.case_lab[self.lab.index((path_x - 1, path_y))]
                    case_min = (path_x - 1, path_y)
        # Aller à droite
        if (path_x + 1, path_y) in self.case_IA:
            if not self.valeur_est[self.index_case.index((path_x, path_y))]:
                if self.case_lab[self.lab.index((path_x + 1, path_y))] < valeur_min:
                    valeur_min = self.case_lab[self.lab.index((path_x + 1, path_y))]
                    case_min = (path_x + 1, path_y)
        # Aller en haut
        if (path_x, path_y - 1) in self.case_IA:
            if not self.valeur_sud[self.index_case.index((path_x, path_y - 1))]:
                if self.case_lab[self.lab.index((path_x, path_y - 1))] < valeur_min:
                    valeur_min = self.case_lab[self.lab.index((path_x, path_y - 1))]
                    case_min = (path_x, path_y - 1)
        # Aller en bas
        if (path_x, path_y + 1) in self.case_IA:
            if not self.valeur_sud[self.index_case.index((path_x, path_y))]:
                if self.case_lab[self.lab.index((path_x, path_y + 1))] < valeur_min:
                    case_min = (path_x, path_y + 1)
        if case_min != ():
            self.path.append(case_min)

    # Créer le labyrinthe rapidement
    def creation_rapide(self):
        while len(self.chemin) != 1:
            self.create_lab()
        self.cut_lab()

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            # Récupère les évènements
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    # Touche 'a' pour la création rapide du labyrinthe
                    elif event.key == pygame.K_a and self.menu:
                        self.create_lab()
                        self.creation_rapide()
                        self.resoudre = True
                        self.menu = False
                    # Touche 'espace' pour créer le labyrinthe
                    elif event.key == pygame.K_SPACE and self.menu:
                        self.create = True
                        self.menu = False
                    # Touche 'r' pour réinitialiser le labyrinthe
                    elif event.key == pygame.K_r:
                        self.depart = (randint(0, int(self.LARGEUR / 2)), randint(0, self.HAUTEUR - 1))
                        self.arrivee = (randint(int(self.LARGEUR / 2), self.LARGEUR - 1), randint(0, self.HAUTEUR - 1))
                        self.index_case = []
                        self.valeur_sud = []
                        self.valeur_est = []
                        self.chemin = [self.depart]
                        self.lab = [self.depart]
                        self.create = False
                        self.menu = True
                        self.couleur_background = (randint(0, 255), randint(0, 255), randint(0, 255))

                        # PLAYER #
                        self.case_player = [self.depart]
                        self.resoudre = False

                        # RESOUDRE IA #
                        self.case_IA = [self.arrivee]
                        self.case_lab = []
                        self.create_path = False
                        self.path_finder = False
                        self.path = [self.depart]
                        self.init_lab()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        clic_x, clic_y = event.pos
                        clic_x -= self.LEFT
                        clic_y -= self.TOP
                        clic_x //= self.SIZE
                        clic_y //= self.SIZE
                        self.return_player(clic_x, clic_y)

            # Créer le labyrinthe en utilisant la tête chercheuse
            if self.create:
                self.create_lab()
                if len(self.chemin) == 1:
                    self.cut_lab()
                    self.create = False
                    self.resoudre = True
            # Fait le chemin en suivant la souris du joueur
            elif not self.create and self.resoudre:
                pos_x, pos_y = pygame.mouse.get_pos()
                pos_x -= (self.LINE + self.LEFT)
                pos_y -= (self.LINE + self.TOP)
                pos_x //= self.SIZE
                pos_y //= self.SIZE
                self.resolve_player(pos_x, pos_y)
                if self.case_player[-1] == self.arrivee:
                    self.resoudre = False
                    self.create_path = True
            # Créer la solution (invisible)
            elif self.create_path:
                self.resolve_IA()
                if self.depart in self.case_IA:
                    self.create_path = False
                    self.path_finder = True
            # Dessine la solution une fois qu'elle a été trouvé
            elif self.path_finder:
                self.pathfinder()

            self.draw_lab()
            pygame.display.flip()

        pygame.quit()


game = Labyrinthe_Etoile()
game.run()
