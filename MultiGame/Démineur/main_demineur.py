import pygame
import random
import time
from PIL import Image
from Démineur.IA_Demineur import IA_Demineur


# >>>> DEBUG ZONE COULEUR >>>> #

couleur_mine = (120, 220, 80)  # Vert clair
couleur_pioche = (90, 165, 60)  # Vert foncé
couleur_drapeau = (105, 182, 70)  # Vert pâle
couleur_plateau = (120, 220, 80)  # Vert clair
# couleur_affichage = (255, 255, 255)  # Blanc
couleur_1 = (0, 0, 255)  # Bleu
couleur_2 = (0, 255, 0)  # Vert
couleur_3 = (255, 0, 0)  # Rouge
couleur_4 = (255, 255, 0)  # Jaune
couleur_5 = (255, 0, 255)  # Violet
couleur_6 = (0, 255, 255)  # Cyan
couleur_7 = (255, 255, 255)  # Blanc
couleur_8 = (0, 0, 0)  # Noir


# <<<< DEBUG ZONE COULEUR <<<< #


class Demineur:

    def __init__(self):
        pygame.init()
        # Taille de l'écran, du plateau...
        # Easy = 7 * 8 * 100 // Medium = 14 * 18 * 60 // Hard = 16 * 31 * 50
        self.screen = pygame.display.set_mode((0, 0))
        self.image_icon = pygame.image.load('../Démineur/bombe.png')
        pygame.display.set_caption("Démineur 3000")
        pygame.display.set_icon(self.image_icon)

        self.HAUTEUR = 14
        self.LARGEUR = 18
        self.TAILLE = int((self.screen.get_height()) / (self.HAUTEUR + 2))
        self.OFFSET = 2 * self.TAILLE
        self.TRAIT = 2
        self.LEFT = (self.screen.get_width() - self.LARGEUR * self.TAILLE) / 2
        self.TOP = (self.screen.get_height() - self.HAUTEUR * self.TAILLE - self.OFFSET) / 2
        if self.LEFT < 0:
            self.TAILLE = int(self.screen.get_width() / self.LARGEUR)
            self.LEFT = (self.screen.get_width() - self.LARGEUR * self.TAILLE) / 2
            self.TOP = (self.screen.get_height() - self.HAUTEUR * self.TAILLE - self.OFFSET) / 2

        self.NB_MINE = int(self.LARGEUR * self.HAUTEUR / 10 * 2)
        self.FONT_SIZE = int(3 * self.TAILLE / 4)

        # Définition des fonctions du jeu
        self.mines = []
        self.pioche = []
        self.drapeau = []
        self.boom = []
        self.rotate_bombe = []
        self.perdu = False
        self.explose = True
        self.time_set = 0
        self.gagne = False
        self.time_start = 0
        self.time_end = 0
        self.temps_explose = 0
        self.premier_clic = (-2, -2)
        self.couleur_affichage = (255, 255, 255)  # Blanc

        # Défini la boucle de jeu sur True
        self.running = True

        # Initialisations des composants
        police = pygame.font.Font("Roboto.ttf", self.FONT_SIZE)
        self.font_affiche = pygame.font.Font("Roboto.ttf", int(self.FONT_SIZE * 1))
        self.pioche1 = police.render("1", True, couleur_1)
        self.pioche2 = police.render("2", True, couleur_2)
        self.pioche3 = police.render("3", True, couleur_3)
        self.pioche4 = police.render("4", True, couleur_4)
        self.pioche5 = police.render("5", True, couleur_5)
        self.pioche6 = police.render("6", True, couleur_6)
        self.pioche7 = police.render("7", True, couleur_7)
        self.pioche8 = police.render("8", True, couleur_8)
        self.affichage_mine = self.font_affiche.render(f"Mines : {len(self.mines) - len(self.drapeau)}",
                                                       True, self.couleur_affichage)
        self.affichage_temps = self.font_affiche.render(f"0:00", True, self.couleur_affichage)
        self.image1 = pygame.image.load("../Démineur/drapeau.png")
        self.image_drapeau = pygame.transform.scale(self.image1, (int(3 * self.TAILLE / 4), int(3 * self.TAILLE / 4)))
        self.image2 = pygame.image.load("../Démineur/bombe.png")
        self.image_bombe = pygame.transform.scale(self.image2, (int(3 * self.TAILLE / 4), int(3 * self.TAILLE / 4)))
        self.image3 = pygame.image.load("../Démineur/croix.png")
        self.croix_exit = pygame.transform.scale(self.image3, (int(3 * self.TAILLE / 4), int(3 * self.TAILLE / 4)))
        self.croix_rect = self.croix_exit.get_rect()
        self.croix_rect.x = self.screen.get_width() - self.croix_exit.get_width() - 10
        self.croix_rect.y = (self.OFFSET / 2 - self.croix_exit.get_height()) / 2
        self.loading = pygame.image.load("../Démineur/loading.png")
        self.loading = pygame.transform.scale(self.loading, (3 * self.TAILLE, 3 * self.TAILLE))
        self.song = pygame.mixer.Sound("../Démineur/explosion_song.mp3")
        self.ia_demineur = IA_Demineur(self.LARGEUR, self.HAUTEUR)

        self.difficulte_info = {1: ["FACILE", 8, 7], 2: ["MOYEN", 14, 18], 3: ["DIFFICILE", 16, 31]}
        self.difficulte = 2
        self.message_diff = self.font_affiche.render(f"{self.difficulte_info[self.difficulte][0]}", True, (255, 255, 255))
        self.bouton_difficulte = pygame.Rect((self.screen.get_width() - self.message_diff.get_width()) / 2, self.TAILLE / 2, self.message_diff.get_width(), self.TAILLE)

        # >>>> PREDICTION IA >>>> #

        self.pioche_predit = []
        self.drapeau_predit = []
        self.IA = True
        self.IA_est_mort = False

        # <<<< PREDICTION IA <<<< #

        # CHEAT CODE #

        self.code = ""
        self.SHIFT = False
        self.ENTER = False
        self.cheat_active = False

        # CHEAT CODE #

    def restart(self, ingame=False):
        self.TAILLE = int((self.screen.get_height()) / (self.HAUTEUR + 2))
        self.OFFSET = 2 * self.TAILLE
        self.LEFT = (self.screen.get_width() - self.LARGEUR * self.TAILLE) / 2
        self.TOP = (self.screen.get_height() - self.HAUTEUR * self.TAILLE - self.OFFSET) / 2
        if self.LEFT < 0:
            self.TAILLE = int(self.screen.get_width() / self.LARGEUR)
            self.LEFT = (self.screen.get_width() - self.LARGEUR * self.TAILLE) / 2
            self.TOP = (self.screen.get_height() - self.HAUTEUR * self.TAILLE - self.OFFSET) / 2

        self.NB_MINE = int(self.LARGEUR * self.HAUTEUR / 10 * 2)
        self.FONT_SIZE = int(3 * self.TAILLE / 4)

        # Définition des fonctions du jeu
        self.mines = []
        self.pioche = []
        self.drapeau = []
        self.boom = []
        self.rotate_bombe = []
        self.perdu = False
        self.explose = True
        self.time_set = 0
        self.gagne = False
        self.time_end = 0
        self.temps_explose = 0
        if not ingame:
            self.premier_clic = (-2, -2)
            self.time_start = 0
            self.loading = pygame.image.load("../Démineur/loading.png")
            self.loading = pygame.transform.scale(self.loading, (3 * self.TAILLE, 3 * self.TAILLE))
        else:
            self.time_start = time.time()
        self.couleur_affichage = (255, 255, 255)  # Blanc

        # Initialisations des composants
        police = pygame.font.Font("Roboto.ttf", self.FONT_SIZE)
        self.font_affiche = pygame.font.Font("Roboto.ttf", int(self.FONT_SIZE * 1))
        self.pioche1 = police.render("1", True, couleur_1)
        self.pioche2 = police.render("2", True, couleur_2)
        self.pioche3 = police.render("3", True, couleur_3)
        self.pioche4 = police.render("4", True, couleur_4)
        self.pioche5 = police.render("5", True, couleur_5)
        self.pioche6 = police.render("6", True, couleur_6)
        self.pioche7 = police.render("7", True, couleur_7)
        self.pioche8 = police.render("8", True, couleur_8)
        self.affichage_mine = self.font_affiche.render(f"Mines : {len(self.mines) - len(self.drapeau)}",
                                                       True, self.couleur_affichage)
        self.affichage_temps = self.font_affiche.render(f"0:00", True, self.couleur_affichage)
        self.image_drapeau = pygame.transform.scale(self.image1, (int(3 * self.TAILLE / 4), int(3 * self.TAILLE / 4)))
        self.image_bombe = pygame.transform.scale(self.image2, (int(3 * self.TAILLE / 4), int(3 * self.TAILLE / 4)))
        self.croix_exit = pygame.transform.scale(self.image3, (int(3 * self.TAILLE / 4), int(3 * self.TAILLE / 4)))
        self.croix_rect = self.croix_exit.get_rect()
        self.croix_rect.x = self.screen.get_width() - self.croix_exit.get_width() - 10
        self.croix_rect.y = (self.OFFSET / 2 - self.croix_exit.get_height()) / 2
        self.ia_demineur = IA_Demineur(self.LARGEUR, self.HAUTEUR)

        self.message_diff = self.font_affiche.render(f"{self.difficulte_info[self.difficulte][0]}", True, (255, 255, 255))
        self.bouton_difficulte = pygame.Rect((self.screen.get_width() - self.message_diff.get_width()) / 2, self.TAILLE / 2, self.message_diff.get_width(), self.TAILLE)

        # >>>> PREDICTION IA >>>> #

        self.pioche_predit = []
        self.drapeau_predit = []
        self.IA = True
        self.IA_est_mort = False

        # <<<< PREDICTION IA <<<< #

        # CHEAT CODE #

        self.code = ""
        self.SHIFT = False
        self.ENTER = False
        self.cheat_active = False

        # CHEAT CODE #

    # Affichage de la grille de jeu
    def grid(self):
        for x in range(self.LARGEUR):
            for y in range(self.HAUTEUR):
                if (x, y) in self.boom:
                    pygame.draw.rect(self.screen, couleur_drapeau,
                                     (self.LEFT + x * self.TAILLE + self.TRAIT,
                                      self.TOP + y * self.TAILLE + self.TRAIT + self.OFFSET, self.TAILLE - self.TRAIT,
                                      self.TAILLE - self.TRAIT))
                    imagebombe = pygame.transform.rotate(self.image_bombe, self.rotate_bombe[self.mines.index((x, y))])
                    self.screen.blit(imagebombe,
                                     (self.LEFT + x * self.TAILLE + (self.TAILLE - imagebombe.get_width()) / 2,
                                      self.TOP + y * self.TAILLE + (self.TAILLE - imagebombe.get_width()) / 2 + self.OFFSET))
                    if (x, y) in self.drapeau:
                        self.screen.blit(self.image_drapeau,
                                         (self.LEFT + x * self.TAILLE + (
                                                     self.TAILLE - self.image_drapeau.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.image_drapeau.get_width()) / 2 + self.OFFSET))
                elif (x, y) in self.drapeau and not self.IA:
                    pygame.draw.rect(self.screen, couleur_drapeau,
                                     (self.LEFT + x * self.TAILLE + self.TRAIT,
                                      self.TOP + y * self.TAILLE + self.TRAIT + self.OFFSET, self.TAILLE - self.TRAIT,
                                      self.TAILLE - self.TRAIT))
                    self.screen.blit(self.image_drapeau,
                                     (self.LEFT + x * self.TAILLE + (self.TAILLE - self.image_drapeau.get_width()) / 2,
                                      self.TOP + y * self.TAILLE + (
                                              self.TAILLE - self.image_drapeau.get_width()) / 2 + self.OFFSET))
                elif (x, y) in self.mines:
                    pygame.draw.rect(self.screen, couleur_mine,
                                     (self.LEFT + x * self.TAILLE + self.TRAIT,
                                      self.TOP + y * self.TAILLE + self.TRAIT + self.OFFSET, self.TAILLE - self.TRAIT,
                                      self.TAILLE - self.TRAIT))
                elif (x, y) in self.pioche and not self.IA:
                    pygame.draw.rect(self.screen, couleur_pioche,
                                     (self.LEFT + x * self.TAILLE + self.TRAIT,
                                      self.TOP + y * self.TAILLE + self.TRAIT + self.OFFSET, self.TAILLE - self.TRAIT,
                                      self.TAILLE - self.TRAIT))
                    if self.verif_num(x, y) == 1:
                        self.screen.blit(self.pioche1,
                                         (self.LEFT + x * self.TAILLE + (self.TAILLE - self.pioche1.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.pioche1.get_height()) / 2 + self.OFFSET))
                    elif self.verif_num(x, y) == 2:
                        self.screen.blit(self.pioche2,
                                         (self.LEFT + x * self.TAILLE + (self.TAILLE - self.pioche2.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.pioche2.get_height()) / 2 + self.OFFSET))
                    elif self.verif_num(x, y) == 3:
                        self.screen.blit(self.pioche3,
                                         (self.LEFT + x * self.TAILLE + (self.TAILLE - self.pioche3.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.pioche3.get_height()) / 2 + self.OFFSET))
                    elif self.verif_num(x, y) == 4:
                        self.screen.blit(self.pioche4,
                                         (self.LEFT + x * self.TAILLE + (self.TAILLE - self.pioche4.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.pioche4.get_height()) / 2 + self.OFFSET))
                    elif self.verif_num(x, y) == 5:
                        self.screen.blit(self.pioche5,
                                         (self.LEFT + x * self.TAILLE + (self.TAILLE - self.pioche5.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.pioche5.get_height()) / 2 + self.OFFSET))
                    elif self.verif_num(x, y) == 6:
                        self.screen.blit(self.pioche6,
                                         (self.LEFT + x * self.TAILLE + (self.TAILLE - self.pioche6.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.pioche6.get_height()) / 2 + self.OFFSET))
                    elif self.verif_num(x, y) == 7:
                        self.screen.blit(self.pioche7,
                                         (self.LEFT + x * self.TAILLE + (self.TAILLE - self.pioche7.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.pioche7.get_height()) / 2 + self.OFFSET))
                    elif self.verif_num(x, y) == 8:
                        self.screen.blit(self.pioche8,
                                         (self.LEFT + x * self.TAILLE + (self.TAILLE - self.pioche8.get_width()) / 2,
                                          self.TOP + y * self.TAILLE + (
                                                      self.TAILLE - self.pioche8.get_height()) / 2 + self.OFFSET))
                    else:
                        self.deterre(x, y)
                else:
                    pygame.draw.rect(self.screen, couleur_plateau,
                                     (self.LEFT + x * self.TAILLE + self.TRAIT,
                                      self.TOP + y * self.TAILLE + self.TRAIT + self.OFFSET, self.TAILLE - self.TRAIT,
                                      self.TAILLE - self.TRAIT))

    # Création des mines
    def create_mine(self, x, y):
        self.mines.clear()
        first_click_aura = [(x + i - 1, y + j - 1) for i in range(3) for j in range(3)]
        while len(self.mines) != self.NB_MINE:
            place_x = random.randint(0, self.LARGEUR - 1)
            place_y = random.randint(0, self.HAUTEUR - 1)
            if (place_x, place_y) not in self.mines and (place_x, place_y) not in first_click_aura:
                self.mines.append((place_x, place_y))
                self.rotate_bombe.append(random.randint(0, 360))

    # Evenements au clic gauche
    def click_gauche(self, x, y):
        if len(self.mines) == 0:
            self.create_mine(x, y)
        if (x, y) in self.mines and (x, y) not in self.drapeau:
            if not self.IA:
                self.boom.append((x, y))
                self.song.play(1)
            else:
                self.IA_est_mort = True
        elif (x, y) not in self.pioche and (x, y) not in self.drapeau:
            self.pioche.append((x, y))
            self.ia_demineur.information("gauche", (x, y), self.verif_num(x, y))

    # Evenement au clic droit
    def click_droit(self, x, y):
        if (x, y) not in self.drapeau and (x, y) not in self.pioche:
            self.drapeau.append((x, y))
            self.ia_demineur.information("droit", (x, y), 1)
        elif (x, y) in self.drapeau:
            self.drapeau.remove((x, y))
            self.ia_demineur.information("droit", (x, y), -1)

    # Compte le nombre de mines aux alentours
    def verif_num(self, x, y):
        mine_around = 0
        for i in range(3):
            for j in range(3):
                if (x + i - 1, y + j - 1) in self.mines:
                    mine_around += 1
        return mine_around

    # Montre toutes les cases autour d'un "0"
    def deterre(self, x, y):
        for i in range(3):
            for j in range(3):
                if (x + i - 1, y + j - 1) not in self.pioche:
                    if 0 <= x + i - 1 < self.LARGEUR and 0 <= y + j - 1 < self.HAUTEUR:
                        self.pioche.append((x + i - 1, y + j - 1))
                        self.ia_demineur.information("gauche", (x + i - 1, y + j - 1),
                                                     self.verif_num(x + i - 1, y + j - 1))

    # Affiche les éléments pour le joueur
    def afficher(self):
        pygame.draw.rect(self.screen, couleur_plateau, (0, 0, self.screen.get_width(), self.OFFSET))
        self.screen.blit(self.affichage_mine, (10, (self.OFFSET / 2 - self.affichage_mine.get_height()) / 2))
        self.screen.blit(self.affichage_temps,
                         (10, self.OFFSET / 2 + (self.OFFSET / 2 - self.affichage_mine.get_height()) / 2))
        self.screen.blit(self.croix_exit,
                         (self.screen.get_width() - self.croix_exit.get_width() - 10,
                          (self.OFFSET / 2 - self.croix_exit.get_height()) / 2))
        pygame.draw.rect(self.screen, couleur_pioche, self.bouton_difficulte)
        self.screen.blit(self.message_diff, ((self.screen.get_width() - self.message_diff.get_width()) / 2, self.bouton_difficulte.y))

    def run(self):
        # Boucle de jeu
        while self.running:
            self.screen.fill((0, 0, 0))

            # Récupère tous les évènements (clic, appuis d'une touche...)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    try:
                        if event.key != 13:
                            self.code += chr(event.key)
                    except:
                        pass
                    self.cheat_active = False
                    if event.key == pygame.K_r:
                        self.restart(ingame=False)
                    elif event.key == pygame.K_x:
                        self.code = "x"
                    elif event.key == pygame.K_LSHIFT:
                        self.SHIFT = True
                    elif event.key == pygame.K_RETURN:
                        self.ENTER = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.SHIFT = False
                    elif event.key == pygame.K_RETURN:
                        self.ENTER = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y > self.OFFSET:
                        y -= (self.OFFSET + self.TOP)
                        x -= self.LEFT
                        x //= self.TAILLE
                        y //= self.TAILLE
                        if event.button == pygame.BUTTON_LEFT and not self.perdu and not self.gagne:
                            if len(self.mines) == 0:
                                self.time_start = time.time()
                            self.click_gauche(x, y)
                            if self.premier_clic == (-2, -2):
                                self.premier_clic = (x, y)
                        elif event.button == pygame.BUTTON_RIGHT and not self.perdu and not self.gagne:
                            self.click_droit(x, y)
                    if self.croix_rect.collidepoint(event.pos):
                        self.running = False
                    if self.bouton_difficulte.collidepoint(event.pos):
                        self.difficulte = self.difficulte + 1 if self.difficulte < 3 else 1
                        self.message_diff = self.font_affiche.render(f"{self.difficulte_info[self.difficulte][0]}", True, (255, 255, 255))
                        self.HAUTEUR = self.difficulte_info[self.difficulte][1]
                        self.LARGEUR = self.difficulte_info[self.difficulte][2]
                        self.restart(ingame=False)

            # Fait apparaître les bombe après la mort
            if len(self.boom) == 1:
                self.time_end = time.time()
                self.time_set = time.time()
                self.boom.append(self.boom[0])
                self.temps_explose = 2 / len(self.mines)
                self.perdu = True
            if self.time_set + 2 < time.time() and self.perdu and self.explose:
                for i in range(len(self.mines)):
                    if time.time() >= self.time_set + 2 + (self.temps_explose * i):
                        if self.mines[i] not in self.boom:
                            self.boom.append(self.mines[i])
                            self.song.play(1)
                if len(self.boom) == len(self.mines) + 1:
                    self.explose = False

            # Stop le chrono après la victoire
            if len(self.pioche) == self.LARGEUR * self.HAUTEUR - len(self.mines) and not self.gagne:
                self.time_end = time.time()
                self.gagne = True

            # >>>> CHEAT CODE >>>> #

            if self.SHIFT and self.ENTER:
                if self.code == "xyzzy":
                    self.cheat_active = True
                else:
                    self.cheat_active = False

            co_x, co_y = pygame.mouse.get_pos()
            co_x -= self.LEFT
            co_y -= (self.OFFSET + self.TOP)
            co_x //= self.TAILLE
            co_y //= self.TAILLE
            if self.cheat_active:
                if (co_x, co_y) in self.mines:
                    self.couleur_affichage = (0, 0, 0)
                else:
                    self.couleur_affichage = (255, 255, 255)
            else:
                self.couleur_affichage = (255, 255, 255)

            # <<<< CHEAT CODE <<<< #

            # Actualise l'affichage du temps et des mines
            if not self.IA:
                self.affichage_mine = self.font_affiche.render(f"Mines : {len(self.mines) - len(self.drapeau)}",
                                                               True, self.couleur_affichage)
            if self.gagne or self.perdu:
                minute = int(int(self.time_end - self.time_start) / 60)
                seconde = int(self.time_end - self.time_start) - minute * 60
            elif self.time_start != 0:
                minute = int(int(time.time() - self.time_start) / 60)
                seconde = int(time.time() - self.time_start) - minute * 60
            else:
                minute = 0
                seconde = 0
            if seconde < 10:
                self.affichage_temps = self.font_affiche.render(f"{minute}:0{seconde}", True, self.couleur_affichage)
            else:
                self.affichage_temps = self.font_affiche.render(f"{minute}:{seconde}", True, self.couleur_affichage)

            # >>>> IA Demineur >>>> #

            fini = True
            if self.IA:
                for l in range(self.LARGEUR):
                    for h in range(self.HAUTEUR):
                        if (l, h) not in self.pioche and (l, h) not in self.drapeau:
                            if self.ia_demineur.quoi_faire(l, h) == "pioche":
                                self.pioche_predit.append((l, h))
                                self.click_gauche(l, h)
                                fini = False
                            if self.ia_demineur.quoi_faire(l, h) == "drapeau":
                                self.drapeau_predit.append((l, h))
                                self.click_droit(l, h)
                                fini = False

            if fini and self.IA:
                resultat = self.ia_demineur.reflechi()
                if len(resultat) != 0:
                    fini = False
                    for res in range(int(len(resultat) / 2)):
                        if resultat[res + 1] == "creuse":
                            self.click_gauche(resultat[res][0], resultat[res][1])
                        elif resultat[res + 1] == "drapeau":
                            self.click_droit(resultat[res][0], resultat[res][1])

            if len(self.mines) - len(self.drapeau) == 0 and len(self.mines) > 0 and self.IA:
                clean = self.ia_demineur.clean()
                if len(clean) != 0:
                    for cle in range(len(clean)):
                        self.click_gauche(clean[cle][0], clean[cle][1])

            if self.IA_est_mort:
                fini = True

            if fini and len(self.mines) - len(self.drapeau) != 0 and self.IA:
                self.restart(ingame=True)
                self.click_gauche(self.premier_clic[0], self.premier_clic[1])
            elif fini and len(self.mines) - len(self.drapeau) == 0 and self.IA:
                if self.premier_clic != (-2, -2):
                    self.IA = False
                    self.pioche_predit.clear()
                    self.drapeau_predit.clear()
                    self.drapeau.clear()
                    self.pioche.clear()
                    self.gagne = False
                    self.pioche.append(self.premier_clic)

            if seconde >= 2 * self.difficulte and self.IA:
                self.restart(ingame=True)
                self.click_gauche(self.premier_clic[0], self.premier_clic[1])

            # <<<< IA Demineur <<<< #

            # Fait apparaître la grille et l'affichage à l'écran
            self.grid()
            self.afficher()
            if self.IA and not fini:
                orig_rect = self.loading.get_rect()
                rot_image = pygame.transform.rotate(self.loading, 45)
                rot_rect = orig_rect.copy()
                rot_rect.center = rot_image.get_rect().center
                self.loading = rot_image.subsurface(rot_rect).copy()
                self.screen.blit(self.loading, ((self.screen.get_width() - self.loading.get_width()) / 2, (self.screen.get_height() - self.loading.get_height()) / 2))
            pygame.display.flip()

        # Ferme le module pygame
        pygame.quit()
