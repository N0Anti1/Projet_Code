import pygame

from assets.script.data import Data
from assets.script.menu import MenuAccueil
from assets.script.player import Player
from assets.script.enemy import EnemyManagement
from assets.script.powerUP import PowerUP
from assets.script.tir import Missile


class Game:

    def __init__(self):
        self.largeur = 1280
        self.hauteur = 720
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        self.running = True

        # Joueur
        self.data = Data(self.screen)
        self.menu = MenuAccueil(self.screen, self.data)
        self.player = Player(self.screen, self.data)
        self.enemyManagement = EnemyManagement(self.screen, self.data, self.player)

        self.powerUP = []
        self.boom = []

    def reset_game(self):
        self.player = Player(self.screen, self.data)
        self.enemyManagement = EnemyManagement(self.screen, self.data, self.player)
        self.powerUP = []
        self.boom = []

    def update_game(self):
        self.player.update(self.menu)
        self.enemyManagement.update()
        for power in self.powerUP.copy():
            power.position[1] += self.data.un
            if power.position[1] > self.screen.get_height():
                self.powerUP.remove(power)
        self.collision()

        for boom in self.boom.copy():
            boom[2] += 1
            if boom[2] >= 74:
                self.boom.remove(boom)

        if len(self.enemyManagement.enemies) == 0:
            if self.enemyManagement.phase == len(self.data.level[self.enemyManagement.level]) and len(self.player.tirs) == len(self.powerUP) == 0:
                self.player.health += self.player.max_health * 0.15
                if self.player.health > self.player.max_health * 1.1:
                    self.player.health = self.player.max_health * 1.1
                self.enemyManagement.next_level()
            elif self.enemyManagement.phase != len(self.data.level[self.enemyManagement.level]):
                self.enemyManagement.next_level()

    def collision(self):
        playerRect = pygame.Rect(self.player.position, self.player.size)
        morts = []
        for enemy in self.enemyManagement.enemies:
            enemyRect = pygame.Rect(enemy.position, enemy.size)
            if playerRect.colliderect(enemyRect):
                vie_enemy = enemy.health
                enemy.health -= self.player.health
                if enemy.health <= 0:
                    morts.append(enemy)
                self.player.health -= vie_enemy
            for tir in enemy.tirs.copy():
                tirRect = pygame.Rect(tir.position, tir.image.get_size())
                detruit = False
                if type(tir) == Missile:
                    for tir2 in self.player.tirs.copy():
                        tir2Rect = pygame.Rect(tir2.position, tir2.image.get_size())
                        if tirRect.colliderect(tir2Rect) and not detruit:
                            enemy.tirs.remove(tir)
                            detruit = True
                            self.player.tirs.remove(tir2)
                if playerRect.colliderect(tirRect):
                    self.player.health -= tir.damage
                    if not detruit:
                        detruit = True
                        enemy.tirs.remove(tir)
                if detruit and type(tir) == Missile:
                    self.boom.append([tir.position[0], tir.position[1], 0])
            for tir in self.player.tirs.copy():
                tirRect = pygame.Rect(tir.position, tir.image.get_size())
                if enemyRect.colliderect(tirRect) and enemy not in morts:
                    enemy.health -= tir.damage
                    if enemy.health <= 0:
                        morts.append(enemy)
                    self.player.tirs.remove(tir)
        for mort in morts:
            new = PowerUP(mort.position, self.screen, self.data)
            if new.name != "rien":
                self.powerUP.append(new)
            self.enemyManagement.enemies.remove(mort)
        if self.player.health <= 0:
            self.running = False
        for power in self.powerUP.copy():
            powerRect = pygame.Rect(power.position, power.image.get_size())
            if playerRect.colliderect(powerRect):
                if power.name == "health":
                    self.player.health += self.player.max_health * 0.15
                    if self.player.health > self.player.max_health:
                        self.player.health = self.player.max_health
                elif power.name == "max_health":
                    ancien = self.player.max_health
                    self.player.max_health *= 1.1
                    self.player.health += self.player.max_health - ancien
                elif power.name == "damage":
                    self.player.damage += 0.3
                elif power.name == "shot_speed":
                    self.player.shot_speed += 0.05 * self.data.un
                elif power.name == "cooldown":
                    self.player.cooldown += 0.2
                elif power.name == "multishot":
                    self.player.multishot += 1
                elif power.name == "speed":
                    self.player.speed += 0.05 * self.data.un
                self.powerUP.remove(power)

    def draw_game(self):
        for tir in self.player.tirs:
            self.screen.blit(tir.image, tir.position)
        for enemy in self.enemyManagement.enemies:
            for tir in enemy.tirs:
                self.screen.blit(tir.image, tir.position)
            self.screen.blit(enemy.image, enemy.position)

        for boom in self.boom:
            self.screen.blit(self.data.boom[boom[2]], (boom[0], boom[1]))
        for power in self.powerUP:
            gap = (self.data.aura.get_width() - power.image.get_width()) / 2
            self.screen.blit(self.data.aura, (power.position[0] - gap, power.position[1] - gap))
            self.screen.blit(power.image, power.position)
        pygame.draw.rect(self.screen, (255, 0, 0), (self.player.position[0], self.player.position[1] + self.player.size[1] + 10, self.player.size[0], 5))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.player.position[0], self.player.position[1] + self.player.size[1] + 10, self.player.size[0] * self.player.health / self.player.max_health, 5))
        self.screen.blit(self.player.animate(), self.player.position)

        message = self.data.police.render(f"Level : {self.enemyManagement.level}", False, (255, 255, 255))
        self.screen.blit(message, (0, 0))
        message = self.data.police.render(f"vie: {self.player.health} / vie max: {self.player.max_health} / dégat: {self.player.damage} / shot speed: {self.player.shot_speed} / cooldown: {self.player.cooldown} / vitesse: {self.player.speed}", False, (255, 255, 255))
        self.screen.blit(message, (0, self.screen.get_height() - message.get_height()))

    def update_menu(self):
        self.player.update(self.menu)
        if self.menu.menuType == 2:
            self.player.position = [(self.screen.get_width() - self.player.size[0]) / 2, self.screen.get_height() - 2 * self.player.size[1]]
            self.menu.move_pedia(self.player)
        else:
            self.player.position[1] = (self.screen.get_height() - self.player.size[1]) / 2
        tier = self.screen.get_width() / len(self.menu.menus[self.menu.menuType])
        messages = self.menu.menus[self.menu.menuType]
        menuRect = [pygame.Rect((tier * i + (tier - messages[i].get_width()) / 2, messages[i].get_height()), messages[i].get_size()) for i in range(len(messages))]
        for rect in range(len(menuRect)):
            for tir in self.player.menu_tir.copy():
                tirRect = pygame.Rect(tir.position, tir.image.get_size())
                if menuRect[rect].colliderect(tirRect):
                    if rect == 0 and self.menu.menuType == 0:
                        self.reset_game()
                        self.menu.menu = False
                        self.menu.menuType = 1
                    elif rect == 1:
                        self.menu.lastMenu = self.menu.menuType
                        self.menu.menuType = 2
                    elif rect == 2 and self.menu.menuType == 0:
                        self.running = False
                    elif rect == 0 and self.menu.menuType == 1:
                        last = self.player.position
                        self.player.position = self.player.lastPosition
                        self.player.lastPosition = last
                        self.menu.menu = False
                    elif rect == 2 and self.menu.menuType == 1:
                        self.menu.menuType = 0
                    elif rect == 0 and self.menu.menuType == 2:
                        self.menu.menuType = self.menu.lastMenu
                    self.player.menu_tir.clear()
                    break

    def draw_menu(self):
        self.screen.blit(self.data.menu["image_fond"], (0, 0))
        for tir in self.player.menu_tir:
            self.screen.blit(tir.image, tir.position)

        if self.menu.menuType == 2:
            decal = 0
            for key in self.data.image_shadow_enemy:
                liste = []
                for k in self.data.image_shadow_enemy:
                    liste.append(k)
                image = self.data.image_shadow_enemy[key]
                pygame.draw.rect(self.screen, 255, (self.menu.pedia_left + decal, (self.screen.get_height() - image.get_height()) / 2, image.get_width(), image.get_height()))
                self.screen.blit(image, (self.menu.pedia_left + decal, (self.screen.get_height() - image.get_height()) / 2))
                decal += self.menu.between_shadow + image.get_width()

        messages = self.menu.menus[self.menu.menuType]
        tier = self.screen.get_width() / len(self.menu.menus[self.menu.menuType])
        for i in range(len(messages)):
            self.screen.blit(messages[i], (tier * i + (tier - messages[i].get_width()) / 2, messages[i].get_height()))
        self.screen.blit(self.player.animate(), self.player.position)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.menu.menu:
                            self.player.tir_blaster(True)
                        if len(self.enemyManagement.enemies) > 0:
                            self.player.tir_blaster()
                    elif event.key == pygame.K_ESCAPE and self.menu.menuType == 1:
                        last = self.player.position
                        self.player.position = self.player.lastPosition
                        self.player.lastPosition = last
                        self.menu.menu = not self.menu.menu
                        self.menu.menuType = 1

            if self.menu.menu:
                self.update_menu()
                self.draw_menu()
            else:
                self.update_game()
                self.draw_game()
            pygame.display.flip()
            clock.tick(60)
