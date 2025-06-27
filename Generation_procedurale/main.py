import random
import pygame

pygame.init()


SetCircuitBoard = {  # CircuitBoard ==> path = "assets/MyCircuit/CB"
    1: [1, 1, 1, 1, "1"],
    2: [2, 2, 2, 2, "2"],
    3: [3, 3, 3, 3, "2"],
    4: [2, 1, 1, 1],
    5: [3, 1, 1, 1],
    6: [1, 2, 2, 2],
    7: [3, 2, 2, 2],
    8: [1, 3, 3, 3],
    9: [2, 3, 3, 3],
    10: [1, 2, 1, 2, "2"],
    11: [1, 3, 1, 3, "2"],
    12: [2, 3, 2, 3, "2"],
    13: [2, 2, 1, 1],
    14: [3, 3, 1, 1],
    15: [3, 3, 2, 2]
}
SetColorLine2 = {  # Ligne de couleur ==> path = "assets/MyCircuit/ColorLine/"
    1: [1, 1, 1, 1, "1"],
    2: [21, 11, 21, 11, "2"],
    3: [12, 22, 12, 22, "2"],
    4: [11, 1, 1, 1],
    5: [21, 1, 1, 1],
    6: [12, 1, 1, 1],
    7: [22, 1, 1, 1],
    8: [1, 11, 11, 11],
    9: [1, 21, 21, 21],
    10: [12, 21, 11, 21],
    11: [22, 11, 21, 11],
    12: [1, 12, 12, 12],
    13: [1, 22, 22, 22],
    14: [11, 22, 12, 22],
    15: [21, 12, 22, 12],
    16: [1, 11, 1, 11],
    17: [1, 21, 1, 21],
    18: [1, 12, 1, 12],
    19: [1, 22, 1, 22],
    20: [21, 12, 21, 12],
    21: [11, 22, 11, 22],
    22: [11, 11, 1, 1],
    23: [21, 21, 1, 1],
    24: [12, 12, 1, 1],
    25: [22, 22, 1, 1],
    26: [12, 12, 21, 21],
    27: [22, 22, 11, 11],
}
SetCircuit = {  # CircuitBoard ==> path = "assets/circuit/"
    1: [1, 1, 1, 1, "1"],
    2: [2, 2, 2, 2, "1"],
    3: [2, 3, 2, 2],
    4: [2, 4, 2, 4, "2"],
    5: [2, 3, 2, 1],
    6: [2, 3, 2, 3, "2"],
    7: [4, 3, 4, 3, "2"],
    8: [4, 2, 3, 2],
    9: [3, 3, 2, 3],
    10: [3, 3, 3, 3, "2"],
    11: [3, 3, 2, 2],
    12: [2, 3, 2, 3, "2"]
}
SetCircuitRose = {  # CircuitBoard ==> path = "assets/circuitRose/"
    1: [1, 1, 1, 1, "1"],
    2: [2, 2, 2, 2, "1"],
    3: [2, 3, 2, 2],
    4: [2, 4, 2, 4, "2"],
    5: [2, 3, 2, 1],
    6: [2, 3, 2, 3, "2"],
    7: [4, 3, 4, 3, "2"],
    8: [4, 2, 3, 2],
    9: [3, 3, 2, 3],
    10: [3, 3, 3, 3, "2"],
    11: [3, 3, 2, 2],
    12: [2, 3, 2, 3, "2"]
}
SetRail = {  # Rail de train ==> path = "assets/rail/"
    1: [1, 1, 1, 1, "1"],
    2: [2, 2, 2, 1],
    3: [3, 1, 3, 1, "2"],
    4: [4, 1, 4, 1, "2"],
    5: [3, 4, 1, 1, "1"],
    6: [1, 3, 3, 1, "1"],
    7: [1, 1, 4, 3, "1"],
    8: [4, 1, 1, 4, "1"],
    9: [2, 2, 1, 1],
    10: [2, 1, 2, 1, "2"],
    11: [2, 2, 2, 2, "1"],
    12: [2, 3, 2, 3, "2", "-1"],
    13: [2, 4, 2, 4, "2", "-1"],
}
SetRond = {  # Des ronds ==> path = "assets/rond/"
    1: [1, 1, 1, 1, "1"],
    2: [1, 2, 2, 2],
    3: [2, 2, 1, 1],
    4: [2, 1, 2, 1, "2"],
    5: [2, 1, 1, 1],
}
SetMontagne = {  # Soleil et nuage ==> path = "assets/mountain/"
    1: [1, 1, 1, 1, "1"],
    2: [1, 2, 2, 2]
}
SetGame = {  # Game ==> path = "assets/MyCircuit/CB"
    1: [1, 1, 1, 1, "1"],
    2: [2, 2, 2, 2, "2"],
    10: [1, 2, 1, 2, "2"],
    13: [2, 2, 1, 1]
}

AllPlateau = {
    1: [SetCircuitBoard, "assets/MyCircuit/CB"],
    2: [SetCircuit, "assets/circuit/"],
    3: [SetCircuitRose, "assets/circuitRose/"],
    4: [SetRail, "assets/rail/"],
    5: [SetRond, "assets/rond/"],
    6: [SetMontagne, "assets/mountain/"],
    7: [SetColorLine2, "assets/MyCircuit/ColorLine/"],
    8: [SetGame, "assets/MyCircuit/CB"],
}


class Dictionnaire:

    def __init__(self, size, plateau, path):
        self.size = size
        self.plateau = plateau
        self.path = path
        self.allTuiles = self.loadAllTuiles(self.plateau)
        self.allTextures = self.loadTexture()

    def loadAllTuiles(self, plateau):
        allTuiles = {}
        for key in plateau.keys():
            composant = plateau[key]
            turn = 4
            coeff = 1
            if len(composant) > 4:
                turn = int(composant[4])
                if len(composant) > 5:
                    coeff = int(composant[5])
            for i in range(turn):
                # 0, 1, 2, 3 // -1, 0, 1, 2 // -2, -1, 0, 1 // -3, -2, -1, 0
                allTuiles[key+(i/10)] = self.newTuile(composant[-i], composant[1-i], composant[2-i], composant[3-i], coeff)
        return allTuiles

    def loadTexture(self):
        allTextures = {}
        for i in self.allTuiles.keys():
            coeff = 1
            if len(self.allTuiles[i]) > 4:
                coeff = self.allTuiles[i][4]
            allTextures[i] = self.newTexture(i, coeff)
        return allTextures

    def newTuile(self, nord, est, sud, ouest, coeff):
        tuile = [nord, est, sud, ouest, coeff, "1.1"]
        return tuile

    def newTexture(self, number, coeff):
        image = pygame.image.load(f"{self.path}{int(number)}.png")
        if int(number) != number:
            image = pygame.transform.rotate(image, -90*coeff * (10 * (number - int(number))))
        image = pygame.transform.scale(image, self.size)
        return image


class Generator:

    def __init__(self, plateau, largeur, hauteur, size):
        # Variables :
        self.BoardType = plateau
        self.largeur = largeur
        self.hauteur = hauteur
        self.size = size
        self.plateau = AllPlateau[self.BoardType][0]
        self.pathPlateau = AllPlateau[self.BoardType][1]

        # Paramètre à pas changer
        self.screen = pygame.display.set_mode(((self.largeur + 0) * self.size, (self.hauteur + 0) * self.size))
        self.police = pygame.font.Font(pygame.font.get_default_font(), int(self.size / 5))
        self.Police = pygame.font.Font(pygame.font.get_default_font(), self.size)
        self.running = True
        self.texture = True
        self.drawGrid = False
        self.dictionnaire = Dictionnaire((self.size, self.size), self.plateau, self.pathPlateau)
        self.grille = [[[tuile for tuile in self.dictionnaire.allTuiles] for j in range(self.largeur+0)] for i in range(self.hauteur+0)]
        self.next = []
        self.caseRestantes = [(random.randint(0, self.largeur-1), random.randint(0, self.hauteur-1))]
        self.couleur = {
            1: [self.loadImage(1, 0), self.loadImage(1, 1)]
        }
        self.allCouleur = [["0" for x in range(self.largeur)] for y in range(self.hauteur)]

    def loadImage(self, color, sens):
        image = pygame.image.load(f"assets/MyCircuit/color{color}.png")
        image = pygame.transform.scale(image, (self.size, self.size))
        image = pygame.transform.rotate(image, 90 * sens)
        return image

    def draw(self):
        for y in range(self.hauteur+0):
            for x in range(self.largeur+0):
                if len(self.grille[y][x]) == 1:
                    if self.texture:
                        image = self.dictionnaire.allTextures[self.grille[y][x][0]]
                        self.screen.blit(image, (x * self.size, y * self.size))
                        val = float(self.allCouleur[y][x])
                        if int(val) != 0:
                            self.screen.blit(self.couleur[int(val)][int((val - int(val)) * 10)], (x * self.size, y * self.size))
                    else:
                        for i in range(4):
                            message = self.police.render(f"{self.dictionnaire.allTuiles[self.grille[y][x][0]][i]}", True, 0)
                            if i == 0:
                                self.screen.blit(message, (x * self.size + self.size / 2, y * self.size))
                            elif i == 1:
                                self.screen.blit(message, (x * self.size + self.size - message.get_width(), y * self.size + self.size / 2))
                            elif i == 2:
                                self.screen.blit(message, (x * self.size + self.size / 2, y * self.size + self.size - message.get_height()))
                            elif i == 3:
                                self.screen.blit(message, (x * self.size, y * self.size + self.size / 2))
                if self.drawGrid:
                    pygame.draw.rect(self.screen, 0, (x * self.size, y * self.size, self.size, self.size), 1)
                if (x, y) in self.caseRestantes:
                    pygame.draw.rect(self.screen, 0, (x * self.size, y * self.size, self.size, self.size), self.caseRestantes.count((x, y)))

    def ChoisirTuile(self, x, y):
        try:
            self.grille[y][x] = [random.choice(self.grille[y][x])]
            self.next.append((x, y))
            while len(self.next) > 0:
                self.Propagate(self.next[0][0], self.next[0][1])
                self.next.pop(0)
        except IndexError:
            self.reset()

    def Propagate(self, x, y):
        ordreP = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        ordreCible = [2, 3, 0, 1]
        for i in range(4):
            cibleX, cibleY = x + ordreP[i][0], y + ordreP[i][1]
            if 0 <= cibleX < self.largeur and 0 <= cibleY < self.hauteur:
                removable = []
                for valeur in self.grille[y][x]:
                    number = self.dictionnaire.allTuiles[valeur][i]
                    for autre in self.grille[cibleY][cibleX]:
                        if self.dictionnaire.allTuiles[autre][ordreCible[i]] == number:
                            removable.append(autre)
                for number in self.dictionnaire.allTuiles.keys():
                    if number not in removable and number in self.grille[cibleY][cibleX]:
                        self.grille[cibleY][cibleX].remove(number)
                        if (cibleX, cibleY) not in self.next:
                            self.next.append((cibleX, cibleY))

    def reset(self):
        self.plateau = AllPlateau[self.BoardType][0]
        self.pathPlateau = AllPlateau[self.BoardType][1]
        self.dictionnaire = Dictionnaire((self.size, self.size), self.plateau, self.pathPlateau)
        self.grille = [[[tuile for tuile in self.dictionnaire.allTuiles] for j in range(self.largeur+0)] for i in range(self.hauteur+0)]
        self.next = []
        self.caseRestantes = [(random.randint(0, self.largeur-1), random.randint(0, self.hauteur-1))]

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.BoardType += 1
                        if self.BoardType > len(AllPlateau.keys()):
                            self.BoardType = 1
                        self.reset()
                    elif event.key == pygame.K_LEFT:
                        self.BoardType -= 1
                        if self.BoardType == 0:
                            self.BoardType = len(AllPlateau.keys())
                        self.reset()
                    elif event.key == pygame.K_SPACE:
                        self.drawGrid = not self.drawGrid
                    elif event.key == pygame.K_r:
                        self.reset()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        x, y = event.pos
                        x //= self.size
                        y //= self.size
                        actu = 0
                        if int(float(self.allCouleur[y][x])) == 1:
                            actu = (float(self.allCouleur[y][x]) - int(float(self.allCouleur[y][x]))) * 10 + 1
                            actu %= 2
                        self.allCouleur[y][x] = f"1.{int(actu)}"

            if len(self.caseRestantes) > 0:
                case = random.choice(self.caseRestantes)
                x, y = case
                if x+1 < self.largeur and (x+1, y) not in self.caseRestantes and len(self.grille[y][x+1]) > 1:
                    self.caseRestantes.append((x+1, y))
                if x-1 >= 0 and (x-1, y) not in self.caseRestantes and len(self.grille[y][x-1]) > 1:
                    self.caseRestantes.append((x-1, y))
                if y+1 < self.hauteur and (x, y+1) not in self.caseRestantes and len(self.grille[y+1][x]) > 1:
                    self.caseRestantes.append((x, y+1))
                if y-1 >= 0 and (x, y-1) not in self.caseRestantes and len(self.grille[y-1][x]) > 1:
                    self.caseRestantes.append((x, y-1))
                self.ChoisirTuile(x, y)
                if case in self.caseRestantes:
                    self.caseRestantes.remove(case)
            self.draw()
            pygame.display.flip()

        pygame.quit()


generateur = Generator(plateau=2, largeur=15, hauteur=15, size=30)
generateur.run()
