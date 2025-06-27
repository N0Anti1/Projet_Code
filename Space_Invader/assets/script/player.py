import math
import pygame
from assets.script.tir import Blaster


class Player:

    def __init__(self, screen: pygame.Surface, data):
        self.screen = screen
        self.data = data
        self.health = 100 / 1.1
        self.max_health = 100 / 1.1
        self.damage = 1
        self.shot_speed = self.data.un
        self.cooldown = 1
        self.last_shot = 0
        self.multishot = 1
        self.speed = self.data.un * 2

        self.size = self.data.image_player[0].get_size()
        self.position = [(self.screen.get_width() - self.size[0]) / 2, (self.screen.get_height() - self.size[1]) / 2]
        self.lastPosition = [(self.screen.get_width() - self.size[0]) / 2, (self.screen.get_height() - self.size[1]) / 2]
        self.current_image = 0

        self.tirs = []
        self.menu_tir = []

    def update(self, menu):
        if self.health > self.max_health:
            self.max_health = self.health
        self.move(pygame.key.get_pressed(), menu)
        if self.last_shot > 0:
            self.last_shot -= self.cooldown
        if menu.menu:
            tirs = self.menu_tir
        else:
            tirs = self.tirs
        for tir in tirs.copy():
            x, y = tir.position
            x -= tir.speed * math.sin(math.radians(tir.angle))
            y -= tir.speed * math.cos(math.radians(tir.angle))
            tir.position = (x, y)
            if y < -tir.image.get_height() or y > self.screen.get_height():
                tirs.remove(tir)
            elif x < -tir.image.get_width() or x > self.screen.get_width():
                tirs.remove(tir)

    def tir_blaster(self, menu=False):
        if self.last_shot <= 0:
            self.last_shot = 90

            gauche = (
                self.position[0] + self.size[0] / 50 * 18,
                self.position[1] + self.size[1] / 37 * 2)
            droite = (
                self.position[0] + self.size[0] / 50 * 31,
                self.position[1] + self.size[1] / 37 * 2)

            gap = 45
            while self.multishot * gap >= 180:
                gap -= 1
            if gap < 1:
                gap = 1

            if menu:
                tirs = self.menu_tir
            else:
                tirs = self.tirs
            for i in range(self.multishot):
                image = pygame.transform.scale(self.data.image_tir["blaster_vert"], (self.size[0] / 50, self.size[1] * 7 / 37))
                angle = gap * ((i+1)//2) * (-1)**(i-1)
                tirs.append(Blaster(self.damage, self.shot_speed, gauche, angle, image))
                angle = gap * ((i+1)//2) * (-1)**(i)
                tirs.append(Blaster(self.damage, self.shot_speed, droite, angle, image))

    def animate(self):
        self.current_image += 0.1 * len(self.data.image_player) / 4
        if self.current_image >= len(self.data.image_player):
            self.current_image = 0

        return self.data.image_player[int(self.current_image)]

    def move(self, pressed: pygame.key.get_pressed, menu):
        if not menu.menu or menu.menuType != 2:
            if pressed[pygame.K_RIGHT] and self.position[0] < self.screen.get_width() - self.size[0] / 2:
                self.position[0] += self.speed
            elif pressed[pygame.K_LEFT] and self.position[0] > -self.size[0] / 2:
                self.position[0] -= self.speed
        if not menu.menu:
            if pressed[pygame.K_UP] and self.position[1] > -self.size[1] / 2:
                self.position[1] -= self.speed
            elif pressed[pygame.K_DOWN] and self.position[1] < self.screen.get_height() - self.size[1] / 2:
                self.position[1] += self.speed
