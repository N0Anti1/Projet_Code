# -*- coding: cp1252 -*-

from dataclasses import dataclass
import pygame
import pytmx
import pyscroll
import time

from player import NPC, Items, Enemy


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Sign:
    place_world: str
    collision_rect: str
    message: str


@dataclass
class Door:
    collision_rect: str
    item_interact: str
    item_need: bool
    open: bool


@dataclass
class Chest:
    collision_rect: str
    item_interact: str
    item_need: bool
    object_in: bool
    objet_donner: Items


@dataclass
class PassiveEnemy:
    name: str
    rect: pygame.Rect
    life: int
    state: bool


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    doors: list[Door]
    chests: list[Chest]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    signs: list[Sign]
    passif_enemy: list[PassiveEnemy]


class MapManager:

    def __init__(self, screen, player, codeur, senario, dialogBox):
        self.screen = screen
        self.player = player
        self.codeur = codeur
        self.senario = senario
        self.dialog_box = dialogBox
        self.maps = dict()  # "house" --> Map("house", walls, group)
        self.current_map = "HouseHome_second_Intro"

        self.register_map("HouseHome_second_Intro", portals=[
            Portal(from_world="HouseHome_second_Intro", origin_point="house_home_second_exit", target_world="HouseHome_first_Intro", teleport_point="exit_house_home_second")
        ])
        self.register_map("HouseHome_first_Intro", portals=[
            Portal(from_world="HouseHome_first_Intro", origin_point="house_home_second_enter", target_world="HouseHome_second_Intro", teleport_point="spawn_house_home_second"),
            Portal(from_world="HouseHome_first_Intro", origin_point="house_home_first_exit", target_world="World_Intro", teleport_point="exit_house_home_first")
        ])
        self.register_map("World_Intro", portals=[
            Portal(from_world="World_Intro", origin_point="house_home_first_enter", target_world="HouseHome_first_Intro", teleport_point="spawn_house_home_first"),
            Portal(from_world="World_Intro", origin_point="house_Paul_enter", target_world="HousePaul_Intro", teleport_point="spawn_house_paul")
        ], npcs=[
            NPC("robin", nb_points=2, dialog=["Bonjour, je m'appelle Robin", "Peux-tu aller me chercher des champignons pour la soupe ?"]),
            NPC("paul", nb_points=4, dialog=["Enchanté, je suis Paul", "J'aurais besoin d'une hache pour couper du bois.\nPeux-tu aller me la chercher chez moi ?"])
        ], signs=[
            Sign(place_world="World_Intro", collision_rect="panneau1", message="/\\ Chez Martin\n<-- Chez Paul\n--> Pont")
        ])
        self.register_map("HousePaul_Intro", portals=[
            Portal(from_world="HousePaul_Intro", origin_point="house_paul_exit", target_world="Dungeon_Intro", teleport_point="spawn_dungeon")
        ])
        self.register_map("Dungeon_Intro", portals=[
            Portal(from_world="Dungeon_Intro", origin_point="dungeon_second_enter", target_world="Dungeon_Intro", teleport_point="spawn_dungeon_second"),
            Portal(from_world="Dungeon_Intro", origin_point="dungeon_second_exit", target_world="Dungeon_Intro", teleport_point="exit_dungeon_second"),
            Portal(from_world="Dungeon_Intro", origin_point="dungeon_exit", target_world="Credit", teleport_point="spawn_credit")
        ], npcs=[
            NPC("boss", nb_points=4, dialog=["MOUAAAAAAA", "C'était une bonne partie !!!"])
        ])
        self.register_map("Credit", portals=[
            Portal(from_world="Credit", origin_point="credit_exit", target_world="HouseHome_second_Intro", teleport_point="spawn_player")
        ])

        self.teleport_player("spawn_player")
        self.teleport_npcs()

        self.damage_player = False

    def check_touching(self, dialog_box):
        if dialog_box.reading:
            if dialog_box.letter_index >= len(dialog_box.texts[dialog_box.text_index]) and not dialog_box.message:
                if dialog_box.choice == "RIGHT" and self.player.inventory == "" and dialog_box.objet != "":
                    self.player.inventory = dialog_box.objet
                    self.player.objet_stocker = dialog_box.name
                    self.player.durability = 1
                    for sprite in self.get_group().sprites():
                        if type(sprite) is Items:
                            if sprite.index == dialog_box.index_objet:
                                self.player.degat = sprite.degat
                                sprite.kill()
                    for chest in self.get_map().chests:
                        if chest.objet_donner.index == dialog_box.index_objet:
                            chest.object_in = False
                    if self.current_map == "HousePaul_Intro":
                        self.senario.update("Trouver la Hache", self.player)
                    dialog_box.texts = []
                    dialog_box.next_text()
                elif dialog_box.choice == "RIGHT" and dialog_box.objet != "":
                    if dialog_box.text_index >= 1:
                        self.player.inventory = dialog_box.objet
                        self.player.objet_stocker = dialog_box.name
                        self.player.durability = 1
                        for sprite in self.get_group().sprites():
                            if type(sprite) is Items:
                                if sprite.index == dialog_box.index_objet:
                                    self.player.degat = sprite.degat
                                    sprite.kill()
                    if self.current_map == "HousePaul_Intro":
                        self.senario.update("Trouver la Hache", self.player)
                    dialog_box.next_text()
                elif dialog_box.choice == "RIGHT":
                    if "chest" in dialog_box.index_objet:
                        self.open_chest(dialog_box.index_objet)
                    else:
                        self.open_door(dialog_box.index_objet)
                    self.player.consume()
                    dialog_box.reading = False
                    dialog_box.name = ""
                elif dialog_box.choice != "NONE":
                    dialog_box.reading = False
                    dialog_box.name = ""
                dialog_box.choice = "NONE"
            else:
                dialog_box.execute()
        else:
            frapper = True
            for sprite in self.get_group().sprites():
                if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                    frapper = False
                    if sprite.name == "robin":
                        if self.senario.quests["Apporter des Champignons à Robin"][0] < 0:
                            self.senario.update("Apporter des Champignons à Robin")
                        elif self.player.inventory != "":
                            if self.player.inventory == "Champignon":
                                sprite.dialog = ["Merci à toi !"]
                        else:
                            sprite.dialog = ["Il me faut des Champignons pour la soupe !"]
                        if self.senario.quests["Apporter des Champignons à Robin"][0] >= self.senario.quests["Apporter des Champignons à Robin"][1]:
                            sprite.dialog = ["Merci pour ces Champignons.\nJe vais bien manger ce soir !", "Va voir Paul, il a une mission pour toi"]
                            for porte in self.maps["World_Intro"].doors:
                                if porte.collision_rect == "pont_home_door":
                                    porte.open = True
                        self.senario.update("Apporter des Champignons à Robin", self.player)
                    elif sprite.name == "paul":
                        self.senario.update("Apporter une Hache à Paul")
                    elif sprite.name == "boss":
                        self.senario.update("Battre le boss", map_manager=self)
                    dialog_box.message = True
                    dialog_box.texts = sprite.dialog
                    dialog_box.name = sprite.name
                    dialog_box.execute()
                elif sprite.feet.colliderect(self.player.rect) and type(sprite) is Items:
                    frapper = False
                    dialog_box.message = False
                    dialog_box.name = sprite.name
                    dialog_box.objet = sprite.link
                    dialog_box.index_objet = sprite.index
                    dialog_box.texts = [f"Veux tu prendre l'objet \"{sprite.name}\"?", f"En es-tu sur ?\nTu vas "
                                                                                       f"perdre ton objet \""
                                                                                       f"{self.player.objet_stocker}\""]
                    dialog_box.execute()

            for sign in self.get_map().signs:
                point = self.get_object(sign.collision_rect)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    frapper = False
                    dialog_box.message = True
                    dialog_box.texts = [sign.message]
                    dialog_box.execute()

            for door in self.get_map().doors:
                if not door.open:
                    point = self.get_object(door.collision_rect)
                    rect = pygame.Rect(point.x-8, point.y-8, point.width+16, point.height+16)
                    if self.player.feet.colliderect(rect):
                        frapper = False
                        if not door.item_need:
                            dialog_box.message = True
                            dialog_box.texts = ["C'est ouvert"]
                            dialog_box.execute()
                            self.open_door(door.collision_rect)
                        else:
                            if self.player.objet_stocker == door.item_interact:
                                dialog_box.message = False
                                dialog_box.name = ""
                                dialog_box.objet = ""
                                dialog_box.index_objet = door.collision_rect
                                dialog_box.texts = [f"Veux tu utiliser l'objet \"{self.player.objet_stocker}\" pour "
                                                    f"ouvrir ?"]
                                dialog_box.execute()
                            else:
                                dialog_box.message = True
                                dialog_box.texts = [f"Il faut l'objet \"{door.item_interact}\" pour ouvrir"]
                                dialog_box.execute()

            for chest in self.get_map().chests:
                point = self.get_object(chest.collision_rect)
                rect = pygame.Rect(point.x-8, point.y-8, point.width+16, point.height+16)
                if self.player.feet.colliderect(rect):
                    frapper = False
                    if chest.object_in:
                        if chest.item_need:
                            if self.player.objet_stocker == chest.item_interact:
                                dialog_box.message = False
                                dialog_box.name = ""
                                dialog_box.objet = ""
                                dialog_box.index_objet = chest.collision_rect
                                dialog_box.texts = [f"Veux tu utiliser l'objet \"{self.player.objet_stocker}\" pour "
                                                    f"ouvrir ?"]
                                dialog_box.execute()
                            else:
                                dialog_box.message = True
                                dialog_box.texts = [f"Il faut l'objet \"{chest.item_interact}\" pour ouvrir"]
                                dialog_box.execute()
                        else:
                            dialog_box.message = False
                            dialog_box.name = chest.objet_donner.name
                            dialog_box.objet = chest.objet_donner.link
                            dialog_box.index_objet = chest.objet_donner.index
                            dialog_box.texts = [f"Vous avez trouver l'objet \"{chest.objet_donner.name}\". Voulez "
                                                f"vous le prendre ?", f"En es-tu sur ?\nTu vas perdre "
                                                                      f"ton objet \"{self.player.objet_stocker}\""]
                            dialog_box.execute()
                    else:
                        dialog_box.message = True
                        dialog_box.texts = ["C'est vide"]
                        dialog_box.execute()
            if frapper:
                if (self.player.inventory == "Hache" or self.current_map == "Dungeon_Intro") and not self.player.shoot:
                    self.player.current_image = 0
                    self.player.shoot = True
                    if self.player.direction == "player_right":
                        rect_attack = pygame.Rect(self.player.rect.x + self.player.rect.width, self.player.rect.y, self.player.rect.width, self.player.rect.height)
                    elif self.player.direction == "player_left":
                        rect_attack = pygame.Rect(self.player.rect.x - self.player.rect.width, self.player.rect.y, self.player.rect.width, self.player.rect.height)
                    elif self.player.direction == "player_down":
                        rect_attack = pygame.Rect(self.player.rect.x, self.player.rect.y + self.player.rect.height, self.player.rect.width, self.player.rect.height)
                    else:
                        rect_attack = pygame.Rect(self.player.rect.x, self.player.rect.y - self.player.rect.height, self.player.rect.width, self.player.rect.height)
                    for mob in self.get_group().sprites():
                        if type(mob) is Enemy and self.player.inventory == "Hache":
                            if rect_attack.colliderect(mob.rect):
                                if self.player.direction == "player_right":
                                    mob.position[0] = mob.position[0] + 20
                                elif self.player.direction == "player_left":
                                    mob.position[0] = mob.position[0] - 20
                                elif self.player.direction == "player_down":
                                    mob.position[1] = mob.position[1] + 20
                                else:
                                    mob.position[1] = mob.position[1] - 20
                                mob.get_damage()
                    for passif in self.get_map().passif_enemy:
                        if rect_attack.colliderect(passif.rect) and passif.state:
                            if self.player.inventory == "Hache":
                                passif.life = passif.life - 5
                            else:
                                passif.life = passif.life - 1
                            if passif.life <= 0:
                                passif.state = False
                                self.senario.update("Détruire les Cristaux")

    def check_collisions(self):
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
                    if portal.target_world == "World_Intro":
                        self.senario.update("Sortir de la maison")
                    elif portal.target_world == "HousePaul_Intro":
                        self.senario.update("Trouver la Hache", self.player)
                    elif portal.teleport_point == "spawn_dungeon":
                        self.senario.update("Détruire les Cristaux")
                        self.sauvegarder()
                    elif portal.target_world == "Credit":
                        self.senario.update("Credit", self.player)
                    elif portal.teleport_point == "spawn_player" and portal.from_world == "Credit":
                        return "Restart"
        for sprite in self.get_group().sprites():
            if type(sprite) is not Items and type(sprite) is not PassiveEnemy:
                if type(sprite) is NPC:
                    if sprite.feet.colliderect(self.player.feet):
                        sprite.move_back()
                if sprite.feet.collidelist(self.get_walls()) > -1:
                    sprite.move_back()
                elif sprite.feet.collidelist(self.get_doors()) > -1:
                    sprite.move_back()
            if type(sprite) is Enemy:
                if sprite.rect.colliderect(self.player.feet):
                    if self.player.last_damage + 2 < time.time() and not self.player.mort:
                        self.player.life -= 1
                        self.player.last_damage = time.time()
                        self.damage_player = True
                        if self.player.life <= 0:
                            self.player.current_image = 0
                            self.player.mort = True
                            self.senario.update("Survivre")
                zone = self.get_object(sprite.zone_rect)
                rect = pygame.Rect(zone.x, zone.y, zone.width, zone.height)
                if rect.colliderect(self.player.feet):
                    sprite.save_location()
                    if sprite.rect.center[0] < self.player.rect.center[0]:
                        sprite.move("RIGHT", self.get_walls())
                    elif sprite.rect.center[0] > self.player.rect.center[0]:
                        sprite.move("LEFT", self.get_walls())
                    if sprite.rect.center[1] < self.player.rect.center[1]:
                        sprite.move("DOWN", self.get_walls())
                    elif sprite.rect.center[1] > self.player.rect.center[1]:
                        sprite.move("UP", self.get_walls())

    def sauvegarder(self):
        with open("sauvegardeGame.txt", "w+") as file:
            file.write(self.current_map + "\n")
            p1, p2 = self.player.position
            file.write(str(p1) + "#" + str(p2) + "\n")
            file.write(self.player.inventory + "\n")
            file.write(self.player.objet_stocker + "\n")
            file.write(str(self.player.durability) + "\n")
            file.write(str(self.player.degat) + "\n")
            file.write(str(self.player.life) + "\n")
            for quest in self.senario.quests:
                for i in range(len(self.senario.quests[quest])):
                    if i > 0:
                        file.write("&")
                    file.write(str(self.senario.quests[quest][i]))
                file.write("|")
            file.write("\n")
            for actu in self.senario.actual_quest:
                file.write(actu + "|")
            file.write("\n")
            for map in self.maps:
                file.write(self.maps[map].name + "\n")
                for wall in self.maps[map].walls:
                    file.write(str(wall[0]) + "#" + str(wall[1]) + "#" + str(wall[2]) + "#" + str(wall[3]) + "|")
                file.write("\n")
                for door in self.maps[map].doors:
                    file.write(door.collision_rect + "#" + door.item_interact + "#" + str(door.item_need) + "#" + str(door.open) + "|")
                file.write("\n")
                for chest in self.maps[map].chests:
                    file.write(chest.collision_rect + "#" + chest.item_interact + "#" + str(chest.item_need) + "#" + str(chest.object_in) + "#" + chest.objet_donner.link + "#" + chest.objet_donner.name + "#" + chest.objet_donner.index + "#" + str(chest.objet_donner.degat) + "|")
                file.write("\n")
                for pnj in self.maps[map].npcs:
                    file.write(pnj.name + "#" + str(pnj.nb_points) + "#")
                    for text in pnj.dialog:
                        dial = text.replace("\n", "SAUT_DE_LIGNE")
                        file.write(dial + "&")
                    file.write("|")
                file.write("\n")
                for group in self.maps[map].group:
                    if type(group) is Enemy:
                        x, y = group.position
                        file.write(group.name + "#" + str(group.life) + "#" + str(group.zone_rect) + "#" + str(x) + "#" + str(y) + "|")
                file.write("\n")
                for group in self.maps[map].group:
                    if type(group) is Items:
                        file.write(group.link + "#" + group.name + "#" + group.index + "#" + str(group.degat) + "#" + str(group.position[0]) + "#" + str(group.position[1]) + "|")
                file.write("\n")
                for passif in self.maps[map].passif_enemy:
                    file.write(passif.name + "#" + str(passif.life) + "#" + "{}".format("True" if passif.state else "False") + "|")
                file.write("\n")
            file.close()
        self.codeur.encoder()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[], signs=[]):
        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/Tileset/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2 / ((960 / self.screen.get_width() + 540 / self.screen.get_height()) / 2)

        # Dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)

        # Gérer les collisions
        walls = []
        doors = []
        chests = []
        passive = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if obj.name is not None:
                    give = tmx_data.get_object_by_id(obj.objet_donner)
                    chests.append(Chest(collision_rect=obj.name, item_interact=obj.item_interact,
                                        item_need=obj.item_need, object_in=obj.object_in,
                                        objet_donner=Items(give.link, give.name, give.index, give.degat)))
            elif obj.type == "door":
                doors.append(Door(collision_rect=obj.name, item_interact=obj.item_interact, item_need=obj.item_need,
                                  open=obj.open))
            elif obj.type == "enemy":
                if obj.name == "slime":
                    group.add(Enemy(obj.name, obj.x, obj.y, 0.5, obj.life, obj.zone))
                elif obj.name == "bat":
                    group.add(Enemy(obj.name, obj.x, obj.y, 0.75, obj.life, obj.zone))
                elif obj.name == "goblin":
                    group.add(Enemy(obj.name, obj.x, obj.y, 0.25, obj.life, obj.zone))
            elif obj.type == "passif_enemy":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                passive.append(PassiveEnemy(obj.name, rect, 30, True))

        # Récupérer tout les npcs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)
        for item in tmx_data.objects:
            if item.type == "item":
                group.add(Items(item.link, item.name, item.index, item.degat, screen=self.screen, x=item.x, y=item.y))

        # Créer un objet Map
        self.maps[name] = Map(name, walls, doors, chests, group, tmx_data, portals, npcs, signs, passive)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def get_doors(self):
        door_rect = []
        for door in self.get_map().doors:
            if not door.open:
                rect = self.get_object(door.collision_rect)
                door_rect.append([rect.x, rect.y, rect.width, rect.height])
        return door_rect

    def open_door(self, porte):
        for door in self.get_map().doors:
            if door.collision_rect == porte:
                door.open = not door.open

    def open_chest(self, coffre):
        for chest in self.get_map().chests:
            if chest.collision_rect == coffre:
                chest.item_need = False

    def teleport_npcs(self):
        for carte in self.maps:
            map_data = self.maps[carte]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        if self.check_collisions() == "Restart":
            return "Restart"

        for npc in self.get_map().npcs:
            npc.move()
