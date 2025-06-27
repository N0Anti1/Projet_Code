import math
import random
import pygame

from assets.script.tir import Blaster, Missile


class EnemyManagement:

    def __init__(self, screen, data, player):
        self.screen = screen
        self.data = data
        self.enemies = []
        self.top_wave = 0
        self.phase = 1
        self.speed_wave = 0.3
        self.level = 0
        self.player = player

    def new_enemy(self, health, damage, shot_speed, cooldown, speed, name):
        self.enemies.append(
            Enemy(health, damage, shot_speed, cooldown, speed, self.data.image_enemy[name], name, self.screen,
                  self.data, self.player))

    def new_wave(self, number, name):
        largeur, hauteur = self.data.size_enemy[name]
        width = int(self.screen.get_width() // (largeur * 1.2)) - 1
        height = math.ceil(number / width)
        self.top_wave += -height * hauteur * 1.2

        enemypedia = {
            "normal": {"health": self.level,
                       "damage": 5 + self.level * 1.1,
                       "shot_speed": self.data.un,
                       "cooldown": 1 + self.level * 0.01,
                       "speed": self.data.un},
            "speed": {"health": self.level * 0.8,
                      "damage": self.level,
                      "shot_speed": self.data.un * 1.2,
                      "cooldown": 2 + self.level * 0.02,
                      "speed": self.data.un * 2},
            "tank": {"health": self.level * 4,
                     "damage": self.level,
                     "shot_speed": self.data.un,
                     "cooldown": 0.5 + self.level * 0.01,
                     "speed": self.data.un * 0.75},
            "damage": {"health": self.level * 2,
                       "damage": self.level * 2.5,
                       "shot_speed": self.data.un * 2,
                       "cooldown": 1 + self.level * 0.01,
                       "speed": self.data.un},
            "boss1": {"health": self.player.max_health,
                      "damage": self.player.damage,
                      "shot_speed": self.player.shot_speed,
                      "cooldown": self.player.cooldown,
                      "speed": self.data.un},
        }

        for y in range(height):
            n = number - y * width if number - y * width < width else width
            startX = (self.screen.get_width() - (n * largeur + (n - 1) * largeur * 0.2)) / 2
            for x in range(width):
                if y * width + x < number:
                    self.new_enemy(enemypedia[name]["health"], enemypedia[name]["damage"],
                                   enemypedia[name]["shot_speed"], enemypedia[name]["cooldown"],
                                   enemypedia[name]["speed"], name)
                    self.enemies[-1].position = [startX + x * largeur * 1.2, self.top_wave + y * hauteur * 1.2]

    def next_level(self):
        if self.phase == len(self.data.level[self.level]):
            self.level += 1
            self.phase = 1
            if self.level <= len(self.data.level) - 1:
                for vague in self.data.level[self.level][self.phase - 1]:
                    self.new_wave(vague[0], vague[1])
        else:
            self.phase += 1
            for vague in self.data.level[self.level][self.phase - 1]:
                self.new_wave(vague[0], vague[1])

    def update(self):
        if self.top_wave < 0:
            self.top_wave += self.speed_wave * self.data.un
        for enemy in self.enemies:
            enemy.update()
            if self.top_wave < 0:
                enemy.position[1] += self.speed_wave * self.data.un


class Enemy:

    def __init__(self, health, damage, shot_speed, cooldown, speed, image, name, screen, data, player):
        self.health = health
        self.damage = damage
        self.shot_speed = shot_speed
        self.cooldown = cooldown
        self.last_shot = random.randint(0, 240)
        self.speed = speed
        self.image = image
        self.name = name
        self.screen = screen
        self.data = data
        self.player = player

        self.size = self.image.get_size()
        self.position = [100, 100]
        self.destination = [random.randint(0, self.screen.get_width() - self.size[0]),
                            random.randint(0, self.screen.get_height() - self.size[1])]
        self.tirs = []

    def update(self):
        if self.last_shot > 0:
            self.last_shot -= self.cooldown
        else:
            self.tir_blaster()
        for tir in self.tirs.copy():
            x, y = tir.position
            if type(tir) == Blaster:
                x += tir.speed * math.sin(math.radians(tir.angle))
                y += tir.speed * math.cos(math.radians(tir.angle))
                tir.position = (x, y)
            elif type(tir) == Missile:
                pX, pY = tir.cible.position[0] + tir.cible.size[0] / 2, tir.cible.position[1] + tir.cible.size[1] / 2
                angle = math.atan((pX - x) / (pY - y))
                if pY > y:
                    x += tir.speed * math.sin(angle)
                    y += tir.speed * math.cos(angle)
                else:
                    x -= tir.speed * math.sin(angle)
                    y -= tir.speed * math.cos(angle)
                tir.position = (x, y)

            if y < -tir.image.get_height() or y > self.screen.get_height():
                self.tirs.remove(tir)
            elif x < -tir.image.get_width() or x > self.screen.get_width():
                self.tirs.remove(tir)

    def tir_blaster(self):
        if self.last_shot <= 0:
            self.last_shot = 240
            if self.name == "speed":
                cible = (self.position[0] + self.size[0] / 2, self.screen.get_height())
                pos = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
                angle = math.degrees(math.atan((cible[0] - pos[0]) / (cible[1] - pos[1])))
                image = pygame.transform.scale(self.data.image_tir["blaster_bleu"],
                                               (self.size[0] / 50, self.size[1] * 7 / 37))
                self.tirs.append(Blaster(self.damage, self.shot_speed, pos, angle, image))
            elif self.name == "tank":
                pos1 = (self.position[0] + self.size[0] / 3, self.position[1] + self.size[1] / 2)
                pos2 = (self.position[0] + self.size[0] * 2 / 3, self.position[1] + self.size[1] / 2)
                image = pygame.transform.scale(self.data.image_tir["blaster_violet"],
                                               (self.size[0] / 50, self.size[1] * 7 / 37))
                self.tirs.append(Blaster(self.damage, self.shot_speed, pos1, 0, image))
                self.tirs.append(Blaster(self.damage, self.shot_speed, pos2, 0, image))
            elif self.name == "damage":
                image = pygame.transform.scale(self.data.image_tir["mine"],
                                               (self.size[1] / 5, self.size[1] / 5))
                if random.random() > 0.5:
                    pos1 = (self.position[0] + self.size[0] / 3, self.position[1] + self.size[1] / 2)
                    pos2 = (self.position[0] + self.size[0] * 2 / 3, self.position[1] + self.size[1] / 2)
                    self.tirs.append(Missile(self.damage, self.shot_speed, pos2, self.player, image))
                else:
                    pos1 = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
                self.tirs.append(Missile(self.damage, self.shot_speed, pos1, self.player, image))
            elif self.name == "boss1":
                pos1 = (self.position[0] + self.size[0] / 3, self.position[1] + self.size[1] / 2)
                pos2 = (self.position[0] + self.size[0] * 2 / 3, self.position[1] + self.size[1] / 2)
                image = pygame.transform.scale(self.data.image_tir["blaster_blanc"],
                                               (self.size[0] / 50, self.size[1] * 7 / 37))
                for angle in [0, 45, 75, 95]:
                    self.tirs.append(Blaster(self.damage, self.shot_speed, pos1, -angle, image))
                    self.tirs.append(Blaster(self.damage, self.shot_speed, pos2, angle, image))
            else:
                pos = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
                image = pygame.transform.scale(self.data.image_tir["blaster_rouge"],
                                               (self.size[0] / 50, self.size[1] * 7 / 37))
                self.tirs.append(Blaster(self.damage, self.shot_speed, pos, 0, image))

    def move(self, direction):
        if direction == "UP":
            self.position[1] -= self.speed
        if direction == "DOWN":
            self.position[1] += self.speed
        if direction == "RIGHT":
            self.position[0] += self.speed
        if direction == "LEFT":
            self.position[0] -= self.speed
