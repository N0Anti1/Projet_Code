# -*- coding: cp1252 -*-

import time
import pygame

from dialog import DialogBox
from map import MapManager
from player import Player, Inventaire, Items, NPC, Enemy
from encodeur import Encodeur
from game_manager import Senario


class Game:

    def __init__(self):

        # Créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((0, 0))
        pygame.display.set_caption("Pygamon-Adventure")

        # Générer un joueur
        self.codeur = Encodeur("sauvegardeGame.txt", "EncodeGameSave.txt")
        self.player = Player()
        self.dialog_box = DialogBox(self.screen)
        self.senario = Senario(self.screen)
        self.map_manager = MapManager(self.screen, self.player, self.codeur, self.senario, self.dialog_box)
        self.inventaire = Inventaire(self.screen)

        """self.DIRECTION = []"""

        front = pygame.image.load("assets/menu/front.png")
        self.front = pygame.transform.scale(front, self.screen.get_size())

        quitter = pygame.image.load("assets/menu/quitter_button.png")
        self.quitter = pygame.transform.scale(quitter, (
        int(self.screen.get_width() * 1000 / 2560), int(self.screen.get_height() * 260 / 1440)))
        self.quitter_rect = self.quitter.get_rect()
        self.quitter_rect.y = self.screen.get_height() - self.quitter.get_height()
        new_game = pygame.image.load("assets/menu/new_game_button.png")
        self.new_game = pygame.transform.scale(new_game, (
        int(self.screen.get_width() * 1000 / 2560), int(self.screen.get_height() * 260 / 1440)))
        self.new_game_rect = self.new_game.get_rect()
        self.new_game_rect.y = self.screen.get_height() - self.quitter.get_height() - self.new_game.get_height()
        continuer = pygame.image.load("assets/menu/continue_button.png")
        self.continuer = pygame.transform.scale(continuer, (
        int(self.screen.get_width() * 1000 / 2560), int(self.screen.get_height() * 260 / 1440)))
        self.continuer_rect = self.continuer.get_rect()
        self.continuer_rect.y = self.screen.get_height() - self.quitter.get_height() - self.new_game.get_height() - self.continuer.get_height()

        pause = pygame.image.load("assets/menu/pause.png")
        self.pause = pygame.transform.scale(pause, self.screen.get_size())

        continuer_pause = pygame.image.load("assets/menu/continue_pause_button.png")
        self.continuer_pause = pygame.transform.scale(continuer_pause, (int(self.screen.get_width() * 492 / 2560), int(self.screen.get_height() * 200 / 1440)))
        self.continuer_pause_rect = self.continuer_pause.get_rect()
        self.continuer_pause_rect.x = (self.screen.get_width() - self.continuer_pause.get_width()) / 2
        self.continuer_pause_rect.y = (self.screen.get_height() - self.continuer_pause.get_height()) / 2
        recommencer = pygame.image.load("assets/menu/recommencer_button.png")
        self.recommencer = pygame.transform.scale(recommencer, (int(self.screen.get_width() * 681 / 2560), int(self.screen.get_height() * 136 / 1440)))
        self.recommencer_rect = self.recommencer.get_rect()
        self.recommencer_rect.x = (self.screen.get_width() - self.recommencer.get_width()) / 2
        self.recommencer_rect.y = (self.screen.get_height() - self.recommencer.get_height()) / 2
        menu_pause = pygame.image.load("assets/menu/menu_pause_button.png")
        self.menu_pause = pygame.transform.scale(menu_pause, (int(self.screen.get_width() * 278 / 2560), int(self.screen.get_height() * 200 / 1440)))
        self.menu_pause_rect = self.menu_pause.get_rect()
        self.menu_pause_rect.x = (self.screen.get_width() - self.menu_pause.get_width()) / 2
        self.menu_pause_rect.y = (self.screen.get_height() - self.continuer_pause.get_height()) / 2 + self.continuer_pause.get_height()

        self.afficher_menu = True
        self.afficher_menu_mort = False
        self.accueil = True
        self.damage_player_time = 0
        self.damage_player = False
        self.mort = False

    def create_new_game(self):
        self.player = Player()
        self.senario = Senario(self.screen)
        self.map_manager = MapManager(self.screen, self.player, self.codeur, self.senario, self.dialog_box)
        self.dialog_box = DialogBox(self.screen)
        self.inventaire = Inventaire(self.screen)
        self.afficher_menu = False
        self.afficher_menu_mort = False
        self.map_manager.sauvegarder()

    def load_game(self):
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player, self.codeur, self.senario, self.dialog_box)
        self.dialog_box = DialogBox(self.screen)
        self.inventaire = Inventaire(self.screen)

        with open("sauvegardeGame.txt", "w") as save:
            save.write(self.codeur.deencoder())
            save.close()

        donee = []
        with open("sauvegardeGame.txt", "r") as save:
            for ligne in save.readlines():
                donee.append(ligne.strip("\n"))

        if len(donee) == 10 + 8 * len(self.map_manager.maps):
            self.map_manager.current_map = donee[0]
            position = donee[1].split("#")
            self.player.position = [float(position[0]), float(position[1])]
            self.player.inventory = donee[2]
            self.player.objet_stocker = donee[3]
            self.player.durability = float(donee[4])
            self.player.degat = float(donee[5])
            self.player.life = int(donee[6])
            quete = donee[7].split("|")
            conteur = 0
            for quest in self.senario.quests:
                result = quete[conteur].split("&")
                if len(result) > 1:
                    tab = []
                    for i in result:
                        tab.append(int(i))
                    self.senario.quests[quest] = tab
                else:
                    self.senario.quests[quest] = [True] if quete[conteur] == "True" else [False]
                conteur += 1
            self.senario.actual_quest = donee[8].split("|")
            self.senario.actual_quest.pop(-1)

            for i in range(len(self.map_manager.maps)):
                carte = self.map_manager.maps[donee[9 + i * 8]]

                walls = []
                for wall in donee[10 + i * 8].split("|"):
                    rect = wall.split("#")
                    if len(rect) == 4:
                        walls.append(pygame.Rect(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3])))
                carte.walls = walls

                doors = donee[11 + i * 8].split("|")
                for index in range(len(doors)):
                    door = doors[index].split("#")
                    if len(door) == 4:
                        carte.doors[index].collision_rect = door[0]
                        carte.doors[index].item_interact = door[1]
                        carte.doors[index].item_need = True if door[2] == "True" else False
                        carte.doors[index].open = True if door[3] == "True" else False

                chests = donee[12 + i * 8].split("|")
                for index in range(len(chests)):
                    chest = chests[index].split("#")
                    if len(chest) == 8:
                        carte.chests[index].collision_rect = chest[0]
                        carte.chests[index].item_interact = chest[1]
                        carte.chests[index].item_need = True if chest[2] == "True" else False
                        carte.chests[index].object_in = True if chest[3] == "True" else False
                        carte.chests[index].objet_donner = Items(chest[4], chest[5], chest[6], float(chest[7]))

                npcs = donee[13 + i * 8].split("|")
                for index in range(len(npcs)):
                    npc = npcs[index].split("#")
                    for group in carte.group:
                        if type(group) is NPC and group.name == npc[0]:
                            group.nb_points = int(npc[1])
                            texts = npc[2].split("&")
                            dialogue = []
                            for text in range(len(texts) - 1):
                                message = texts[text].replace("SAUT_DE_LIGNE", "\n")
                                dialogue.append(message)
                            group.dialog = dialogue

                mobs = []
                objets = donee[14 + i * 8].split("|")
                for index in range(len(objets)):
                    objet = objets[index].split("#")
                    if len(objet) == 5:
                        if objet[0] == "slime":
                            mobs.append(Enemy(objet[0], float(objet[3]), float(objet[4]), 0.5, int(objet[1]), objet[2]))
                        elif objet[0] == "bat":
                            mobs.append(Enemy(objet[0], float(objet[3]), float(objet[4]), 0.75, int(objet[1]), objet[2]))
                        elif objet[0] == "goblin":
                            mobs.append(Enemy(objet[0], float(objet[3]), float(objet[4]), 0.25, int(objet[1]), objet[2]))
                for obj in carte.group:
                    if type(obj) is Enemy:
                        obj.kill()
                for mob in mobs:
                    carte.group.add(mob)

                items = []
                objets = donee[15 + i * 8].split("|")
                for index in range(len(objets)):
                    objet = objets[index].split("#")
                    if len(objet) == 6:
                        items.append(Items(objet[0], objet[1], objet[2], float(objet[3]), x=float(objet[4]), y=float(objet[5])))
                for obj in carte.group:
                    if type(obj) is Items:
                        obj.kill()
                for item in items:
                    carte.group.add(item)

                passifs = donee[16 + i * 8].split("|")
                for passif in passifs:
                    cristal = passif.split("#")
                    for passive in carte.passif_enemy:
                        if passive.name == cristal[0]:
                            passive.life = int(cristal[1])
                            passive.state = True if cristal[2] == "True" else False
            self.afficher_menu = False
            self.afficher_menu_mort = False
        else:
            self.create_new_game()

    def draw_menu(self):
        if self.accueil:
            self.screen.blit(self.front, (0, 0))
            self.screen.blit(self.continuer, (0,
                                              self.screen.get_height() - self.quitter.get_height() - self.new_game.get_height() - self.continuer.get_height()))
            self.screen.blit(self.new_game,
                             (0, self.screen.get_height() - self.quitter.get_height() - self.new_game.get_height()))
            self.screen.blit(self.quitter, (0, self.screen.get_height() - self.quitter.get_height()))
        elif not self.afficher_menu_mort:
            self.screen.blit(self.pause, (0, 0))
            self.screen.blit(self.continuer_pause, ((self.screen.get_width() - self.continuer_pause.get_width()) / 2,
                                              (self.screen.get_height() - self.continuer_pause.get_height()) / 2))
            self.screen.blit(self.menu_pause,
                             ((self.screen.get_width() - self.menu_pause.get_width()) / 2,
                              (self.screen.get_height() - self.continuer_pause.get_height()) / 2 + self.continuer_pause.get_height()))
        else:
            self.screen.blit(self.pause, (0, 0))
            self.screen.blit(self.recommencer, ((self.screen.get_width() - self.recommencer.get_width()) / 2,
                                              (self.screen.get_height() - self.recommencer.get_height()) / 2))
            self.screen.blit(self.menu_pause,
                             ((self.screen.get_width() - self.menu_pause.get_width()) / 2,
                              (self.screen.get_height() - self.recommencer.get_height()) / 2 + self.recommencer.get_height()))

    def update(self):
        if self.map_manager.update() == "Restart":
            self.create_new_game()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if not self.dialog_box.reading:
            if pressed[pygame.K_UP]:
                self.player.move_player("UP")
            elif pressed[pygame.K_DOWN]:
                self.player.move_player("DOWN")
            elif pressed[pygame.K_RIGHT]:
                self.player.move_player("RIGHT")
            elif pressed[pygame.K_LEFT]:
                self.player.move_player("LEFT")

    def run(self):
        # Boucle du jeu
        running = True
        clock = pygame.time.Clock()

        while running:

            if self.afficher_menu or self.afficher_menu_mort:
                self.draw_menu()
            else:
                if not self.player.shoot and not self.player.mort:
                    self.handle_input()
                else:
                    self.player.update_animation(self.player.direction)
                self.update()
                self.map_manager.draw()
                self.dialog_box.render()
                self.inventaire.draw(self.player.inventory)
                self.senario.draw_quest()
            if self.map_manager.damage_player:
                self.map_manager.damage_player = False
                self.damage_player_time = time.time()
                self.damage_player = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and self.afficher_menu:
                    if event.key == pygame.K_ESCAPE:
                        self.afficher_menu = False
                elif event.type == pygame.KEYDOWN and self.afficher_menu_mort:
                    if event.key == pygame.K_SPACE:
                        self.load_game()
                elif event.type == pygame.KEYDOWN and not self.afficher_menu:
                    if event.key == pygame.K_ESCAPE:
                        self.map_manager.sauvegarder()
                        self.afficher_menu = True
                        self.accueil = False
                    if event.key == pygame.K_SPACE and not self.player.mort:
                        self.map_manager.check_touching(self.dialog_box)
                    if self.dialog_box.reading and not self.dialog_box.message:
                        if event.key == pygame.K_RIGHT:
                            self.dialog_box.choice = "RIGHT"
                        elif event.key == pygame.K_LEFT:
                            self.dialog_box.choice = "LEFT"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT and self.afficher_menu:
                        if self.accueil:
                            if self.quitter_rect.collidepoint(event.pos):
                                running = False
                            elif self.new_game_rect.collidepoint(event.pos):
                                self.create_new_game()
                            elif self.continuer_rect.collidepoint(event.pos):
                                self.load_game()
                        else:
                            if self.continuer_pause_rect.collidepoint(event.pos):
                                self.afficher_menu = False
                            elif self.menu_pause_rect.collidepoint(event.pos):
                                self.accueil = True
                    if event.button == pygame.BUTTON_LEFT and self.afficher_menu_mort:
                        if self.recommencer_rect.collidepoint(event.pos):
                            self.load_game()
                        elif self.menu_pause_rect.collidepoint(event.pos):
                            self.accueil = True
                            self.afficher_menu = True
                            self.afficher_menu_mort = False

            if self.damage_player:
                if self.damage_player_time + 1 < time.time():
                    self.damage_player = False
                pygame.draw.rect(self.screen, (255, 0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()), 50)
            if self.player.life <= 0 and not self.player.mort:
                self.player.kill()
                self.player.life = 3
                self.accueil = False
                self.afficher_menu_mort = True
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
