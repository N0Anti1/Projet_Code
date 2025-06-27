import pygame
from random import choice
from IA_wordle import IA_Wordle


class Wordle:

    def __init__(self):
        pygame.init()
        self.running = True

        self.screen = pygame.display.set_mode((0, 0))
        pygame.display.set_caption("Wordle")
        self.titre = "LE MOT"

        self.TAILLE = 5
        self.HAUTEUR = 6
        self.SIZE = int(self.screen.get_height() / (self.HAUTEUR + 2))
        self.LEFT = (self.screen.get_width() - self.TAILLE * self.SIZE) / 2
        self.TOP = (self.screen.get_height() - (self.HAUTEUR + 2) * self.SIZE) / 2
        if self.LEFT < 0:
            self.SIZE = int(self.screen.get_width() / self.TAILLE)
            self.LEFT = (self.screen.get_width() - self.TAILLE * self.SIZE) / 2
            self.TOP = (self.screen.get_height() - (self.HAUTEUR + 2) * self.SIZE) / 2

        self.file_stat = open(f'../Wordle/stats{self.TAILLE}.txt', 'r')
        self.stats = [int(number) for number in self.file_stat.readlines()[0].split(',')]
        self.file_stat_w = f'../Wordle/stats{self.TAILLE}.txt'

        self.file = open(f'../Wordle/word{self.TAILLE}.txt')
        self.liste = self.file.readlines()  # cp1252
        self.dictionnaire = []

        for index in range(len(self.liste)):
            self.dictionnaire.append(self.liste[index].strip('\n'))

        self.start_word = {
            4: "raie",
            5: "raies",
            6: "taries",
            7: "traines",
            8: "notaires",
            9: "notariees",
            10: "coursaient"
        }

        self.mot_choisi = choice(self.dictionnaire)
        self.ia = IA_Wordle(self.TAILLE)

        self.ligne = 0
        self.fini = False
        self.perdu = False
        self.mot_ecrit = [""]
        self.bonne_lettre = []
        self.mauvaise_lettre = []

        self.police = pygame.font.Font('../Wordle/Roboto.ttf', self.SIZE)
        self.police_titre = pygame.font.Font('../Wordle/Roboto.ttf', int(self.SIZE / 2))
        self.police_victoire = pygame.font.Font('../Wordle/Roboto.ttf', int(self.SIZE / 4))

        reload = pygame.image.load("../Wordle/reload.png")
        reload = pygame.transform.scale(reload, (self.SIZE / 2, self.SIZE / 2))
        fleche = pygame.image.load("../Wordle/flèche.png")
        fleche = pygame.transform.scale(fleche, (self.SIZE / 2, self.SIZE / 2))
        dead = pygame.image.load("../Wordle/dead.png")
        self.dead = pygame.transform.scale(dead, (self.SIZE / 4, self.SIZE / 4))
        self.reload = reload
        self.reload_rect = self.reload.get_rect()
        self.reload_rect.x = (self.screen.get_width() - self.reload.get_width()) / 2
        self.reload_rect.y = self.TOP + self.SIZE + self.SIZE / 4

        self.fleche_droite = fleche
        self.fleche_droite_rect = self.fleche_droite.get_rect()
        self.fleche_droite_rect.x = self.LEFT + self.SIZE / 4 + (self.TAILLE - 1) * self.SIZE
        self.fleche_droite_rect.y = self.TOP + self.SIZE + self.SIZE / 4

        self.fleche_gauche = pygame.transform.rotate(fleche, 180)
        self.fleche_gauche_rect = self.fleche_gauche.get_rect()
        self.fleche_gauche_rect.x = self.LEFT + self.SIZE / 4
        self.fleche_gauche_rect.y = self.TOP + self.SIZE + self.SIZE / 4

    def draw_title(self):
        LEFT = (self.screen.get_width() - 6 * int(self.SIZE / 2)) / 2
        for x in range(6):
            if x == 0:
                pygame.draw.rect(self.screen, (50, 200, 50),
                                 (LEFT + x * int(self.SIZE / 2), self.TOP + 2 * int(self.SIZE / 2) + -2 * int(self.SIZE / 2), int(self.SIZE / 2), int(self.SIZE / 2)))
            elif x == 4:
                pygame.draw.rect(self.screen, (200, 150, 0),
                                 (LEFT + x * int(self.SIZE / 2), self.TOP + 2 * int(self.SIZE / 2) + -2 * int(self.SIZE / 2), int(self.SIZE / 2), int(self.SIZE / 2)))
            else:
                pygame.draw.rect(self.screen, (50, 50, 50),
                                 (LEFT + x * int(self.SIZE / 2), self.TOP + 2 * int(self.SIZE / 2) + -2 * int(self.SIZE / 2), int(self.SIZE / 2), int(self.SIZE / 2)))
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (LEFT + x * int(self.SIZE / 2), self.TOP + 2 * int(self.SIZE / 2) + -2 * int(self.SIZE / 2), int(self.SIZE / 2), int(self.SIZE / 2)), 2)
            lettre = self.police_titre.render(self.titre[x], True, (255, 255, 255))
            self.screen.blit(lettre, (LEFT + x * int(self.SIZE / 2) + (int(self.SIZE / 2) - lettre.get_width()) / 2,
                                      self.TOP + 2 * int(self.SIZE / 2) + -2 * int(self.SIZE / 2) + (int(self.SIZE / 2) - lettre.get_height()) / 2))
        self.screen.blit(self.reload, ((self.screen.get_width() - self.reload.get_width()) / 2, self.TOP + self.SIZE + self.SIZE / 4))
        self.screen.blit(self.fleche_gauche, (self.LEFT + self.SIZE / 4, self.TOP + self.SIZE + self.SIZE / 4))
        self.screen.blit(self.fleche_droite, (self.LEFT + self.SIZE / 4 + (self.TAILLE - 1) * self.SIZE, self.TOP + self.SIZE + self.SIZE / 4))

    def draw_case(self):
        for x in range(self.TAILLE):
            for y in range(self.HAUTEUR):
                if y < self.ligne:
                    if (x, y) in self.bonne_lettre:
                        pygame.draw.rect(self.screen, (50, 200, 50),
                                         (self.LEFT + x * self.SIZE, self.TOP + 2 * self.SIZE + y * self.SIZE, self.SIZE, self.SIZE))
                    elif (x, y) in self.mauvaise_lettre:
                        pygame.draw.rect(self.screen, (200, 150, 0),
                                         (self.LEFT + x * self.SIZE, self.TOP + 2 * self.SIZE + y * self.SIZE, self.SIZE, self.SIZE))
                    else:
                        pygame.draw.rect(self.screen, (50, 50, 50),
                                         (self.LEFT + x * self.SIZE, self.TOP + 2 * self.SIZE + y * self.SIZE, self.SIZE, self.SIZE))
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (self.LEFT + x * self.SIZE, self.TOP + 2 * self.SIZE + y * self.SIZE, self.SIZE, self.SIZE), 2)
                elif y == self.ligne and x + 1 <= len(self.mot_ecrit[y]):
                    pygame.draw.rect(self.screen, (100, 100, 100),
                                     (self.LEFT + x * self.SIZE, self.TOP + 2 * self.SIZE + y * self.SIZE, self.SIZE, self.SIZE), 4)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50),
                                     (self.LEFT + x * self.SIZE, self.TOP + 2 * self.SIZE + y * self.SIZE, self.SIZE, self.SIZE), 2)

                try:
                    lettre = self.police.render(self.mot_ecrit[y][x], True, (255, 255, 255))
                    self.screen.blit(lettre, (self.LEFT + x * self.SIZE + (self.SIZE - lettre.get_width()) / 2,
                                              self.TOP + 2 * self.SIZE + y * self.SIZE + (self.SIZE - lettre.get_height()) / 2))
                except:
                    pass

    def verif_word(self):
        if self.mot_ecrit[self.ligne].lower() == self.mot_choisi:
            self.fini = True
            self.stats[self.ligne] += 1
        elif self.mot_ecrit[self.ligne].lower() in self.dictionnaire:
            sequence = [0 for _ in range(self.TAILLE)]
            new_mot = []
            for lettre in self.mot_choisi:
                new_mot.append(lettre)
            for place in range(self.TAILLE):
                if self.mot_ecrit[self.ligne][place].lower() == new_mot[place]:
                    sequence[place] = 2
                    new_mot[place] = 0
                    self.bonne_lettre.append((place, self.ligne))
            for place in range(self.TAILLE):
                if self.mot_ecrit[self.ligne][place].lower() in new_mot and self.mot_ecrit[self.ligne][place].lower() != self.mot_choisi[place]:
                    sequence[place] = 1
                    new_mot[new_mot.index(self.mot_ecrit[self.ligne][place].lower())] = 0
                    self.mauvaise_lettre.append((place, self.ligne))
            self.ligne += 1
            self.mot_ecrit.append("")
        if self.ligne > 5:
            self.fini = True
            self.perdu = True
            self.stats[self.ligne] += 1

    def afficher_victoire(self):
        for x in range(self.TAILLE):
            pygame.draw.rect(self.screen, (50, 200, 50),
                             (self.LEFT + x * self.SIZE, self.TOP + 7 * self.SIZE, self.SIZE, self.SIZE))
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (self.LEFT + x * self.SIZE, self.TOP + 7 * self.SIZE, self.SIZE, self.SIZE), 2)
            lettre = self.police.render(self.mot_choisi[x].upper(), True, (255, 255, 255))
            self.screen.blit(lettre, (self.LEFT + x * self.SIZE + (self.SIZE - lettre.get_width()) / 2,
                                      self.TOP + 7 * self.SIZE + (self.SIZE - lettre.get_height()) / 2))
        pygame.draw.rect(self.screen, (50, 50, 50), (self.LEFT, self.TOP + 2 * self.SIZE, self.SIZE * self.TAILLE, self.SIZE * 5))
        message = self.police_titre.render("{}".format("{} COUP{}".format(self.ligne + 1, "S" if self.ligne + 1 > 1 else "") if not self.perdu else "TU AS PERDU"), True, (0, 255, 0) if not self.perdu else (255, 0, 0))
        performances = self.police_titre.render("Statistiques :", True, (255, 255, 255))
        self.screen.blit(message, ((self.screen.get_width() - message.get_width()) / 2, self.TOP + 2 * self.SIZE))
        self.screen.blit(performances, (self.LEFT, self.TOP + 3 * self.SIZE))
        for x in range(7):
            if x < 6:
                self.screen.blit(self.police_victoire.render(f"{x + 1} :", True, (255, 255, 255)),
                                 (self.LEFT, self.TOP + 4 * self.SIZE + x * self.SIZE / 3))
            else:
                self.screen.blit(self.dead, (self.LEFT, self.TOP + 4 * self.SIZE + x * self.SIZE / 3))
            somme = sum(self.stats) if sum(self.stats) != 0 else 1
            pourcentage = int(self.stats[x] / somme * 100)
            if pourcentage != 0:
                pygame.draw.line(self.screen, (50, 255, 50),
                                 (self.LEFT + self.SIZE / 2, self.TOP + 4 * self.SIZE + x * self.SIZE / 3 + int(self.SIZE / 6)),
                                 (self.LEFT + self.SIZE / 2 + pourcentage * (self.TAILLE - 1) * self.SIZE / 100, self.TOP + 4 * self.SIZE + x * self.SIZE / 3 + int(self.SIZE / 6)), int(self.SIZE / 6))

    def restart(self):
        document = open(self.file_stat_w, 'w')
        document.close()
        file = open(self.file_stat_w, 'a')
        statistiques = ""
        for x in range(7):
            statistiques += f"{self.stats[x]}," if x < 6 else f"{self.stats[x]}"
        file.write(statistiques)
        file.close()

        self.file_stat = open(f'../Wordle/stats{self.TAILLE}.txt', 'r')
        self.stats = [int(number) for number in self.file_stat.readlines()[0].split(',')]
        self.file_stat_w = f'../Wordle/stats{self.TAILLE}.txt'

        self.file = open(f'../Wordle/word{self.TAILLE}.txt', 'r')
        self.liste = self.file.readlines()  # cp1252
        self.dictionnaire = []

        for index in range(len(self.liste)):
            self.dictionnaire.append(self.liste[index].strip('\n'))

        self.mot_choisi = choice(self.dictionnaire)

        self.ligne = 0
        self.fini = False
        self.perdu = False
        self.mot_ecrit = [""]
        self.bonne_lettre = []
        self.mauvaise_lettre = []

        self.SIZE = int(self.screen.get_height() / (self.HAUTEUR + 2))
        self.LEFT = (self.screen.get_width() - self.TAILLE * self.SIZE) / 2
        self.TOP = (self.screen.get_height() - (self.HAUTEUR + 2) * self.SIZE) / 2
        if self.LEFT < 0:
            self.SIZE = int(self.screen.get_width() / self.TAILLE)
            self.LEFT = (self.screen.get_width() - self.TAILLE * self.SIZE) / 2
            self.TOP = (self.screen.get_height() - (self.HAUTEUR + 2) * self.SIZE) / 2
        self.fleche_gauche_rect.x = self.LEFT + self.SIZE / 4
        self.fleche_droite_rect.x = self.LEFT + self.SIZE / 4 + (self.TAILLE - 1) * self.SIZE

    def run(self):
        while self.running:
            self.screen.fill((20, 20, 20))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.restart()
                        self.running = False
                    # Écrire le mot et le supprimer
                    elif 97 <= event.key <= 122 and not self.fini:
                        if len(self.mot_ecrit[self.ligne]) < self.TAILLE:
                            self.mot_ecrit[self.ligne] += chr(event.key).upper()
                    elif event.key == pygame.K_BACKSPACE and len(self.mot_ecrit[self.ligne]) != 0 and not self.fini:
                        mot = self.mot_ecrit[self.ligne]
                        self.mot_ecrit[self.ligne] = ""
                        for lettre in range(len(mot) - 1):
                            self.mot_ecrit[self.ligne] += mot[lettre]
                    elif event.key == pygame.K_RETURN and len(self.mot_ecrit[self.ligne]) == self.TAILLE and not self.fini:
                        self.verif_word()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        if self.reload_rect.collidepoint(event.pos):
                            self.restart()
                        if self.fleche_gauche_rect.collidepoint(event.pos):
                            if self.TAILLE > 4:
                                self.TAILLE -= 1
                                self.restart()
                        if self.fleche_droite_rect.collidepoint(event.pos):
                            if self.TAILLE < 10:
                                self.TAILLE += 1
                                self.restart()

            if self.fini:
                self.afficher_victoire()
                self.draw_title()
            else:
                self.draw_case()
                self.draw_title()
            pygame.display.flip()

        pygame.quit()

game = Wordle()
game.run()
