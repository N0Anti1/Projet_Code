# -*- coding: cp1252 -*-

import pygame
from miniGame.PingPong.main import PingPong


class Senario:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.quests = {
            "Sortir de la maison": [False],
            "Apporter des Champignons à Robin": [-1, 3],
            "Apporter une Hache à Paul": [False],
            "Trouver la Hache": [False],
            "Détruire les Cristaux": [-1, 3],
            "Battre le boss": [False],
            "Survivre": [True]
        }

        self.actual_quest = ["Sortir de la maison"]
        self.police = pygame.font.Font('assets/menu/Freestyle_Script.ttf', int(self.screen.get_height() / 15))

    def draw_quest(self):
        for quete in self.actual_quest:
            if type(self.quests[quete][0]) == bool:
                message = self.police.render("{} : {}".format(quete, "X" if not self.quests[quete][0] else "V"), True, (255, 255, 255))
            else:
                message = self.police.render("{} : {}".format(quete, f"{self.quests[quete][0]}/{self.quests[quete][1]}"), True, (255, 255, 255))
            self.screen.blit(message, (0, self.screen.get_height() / 10 + self.actual_quest.index(quete) * message.get_height()))

    def update(self, action, player=None, map_manager=None):
        if action == "Sortir de la maison":
            if not self.quests[action][0]:
                self.quests[action][0] = True
        elif action == "Apporter des Champignons à Robin":
            if self.quests[action][0] == -1:
                self.actual_quest = [action]
                self.quests[action][0] += 1
            elif self.quests[action][0] < self.quests[action][1]:
                if player.inventory == "Champignon":
                    self.quests[action][0] += 1
                    player.inventory = ""
                    player.objet_stocker = ""
        elif action == "Apporter une Hache à Paul":
            self.actual_quest = [action]
        elif action == "Trouver la Hache":
            if action not in self.actual_quest and not self.quests[action][0]:
                self.actual_quest.append(action)
            if player.inventory == "Hache":
                self.quests[action][0] = True
            else:
                self.quests[action][0] = False
        elif action == "Détruire les Cristaux":
            if self.quests[action][0] == -1:
                self.actual_quest = [action, "Battre le boss", "Survivre"]
                self.quests[action][0] += 1
            elif self.quests[action][0] < self.quests[action][1]:
                self.quests[action][0] += 1
        elif action == "Battre le boss":
            if not self.quests[action][0]:
                nb_cristal = 1
                for passif in map_manager.get_map().passif_enemy:
                    if passif.state:
                        nb_cristal += 1
                game = PingPong(self.screen, nb_cristal)
                game.run()
                if game.victoire:
                    self.quests[action] = [True]
                    for pnj in map_manager.get_map().npcs:
                        if pnj.name == "boss":
                            msg = ["MOUAAAAAAA\nTu m'as vaincu !", "C'était une bonne partie !!!"]
                            pnj.dialog = msg
                    for door in map_manager.get_map().doors:
                        if door.collision_rect == "dungeon_exit_door":
                            map_manager.open_door(door.collision_rect)
                else:
                    for pnj in map_manager.get_map().npcs:
                        if pnj.name == "boss":
                            msg = ["MOUAAAAAAA", "Je ne suis pas un monstre facile à battre !!!"]
                            pnj.dialog = msg
        elif action == "Survivre":
            if self.quests[action][0]:
                self.quests[action][0] = False
        elif action == "Credit":
            self.actual_quest = []
            player.inventory = ""
            player.objet_stocker = ""
        elif action == "Restart":
            self.quests = {
                "Sortir de la maison": [False],
                "Apporter des Champignons à Robin": [-1, 3],
                "Apporter une Hache à Paul": [False],
                "Trouver la Hache": [False],
                "Détruire les Cristaux": [-1, 3],
                "Battre le boss": [False],
                "Survivre": [True]
            }

            self.actual_quest = ["Sortir de la maison"]
