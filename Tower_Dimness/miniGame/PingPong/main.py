import pygame
from math import cos, sin, pi
from random import random


class PingPong:
    def __init__(self, screen: pygame.Surface, life):
        self.ecran = screen
        self.w, self.h = screen.get_size()
        self.screen = pygame.Surface(screen.get_size())
        self.life = life
        self.running = True

        self.victoire = False
        self.speed = 4 * self.life

        self.goal_player = pygame.Rect(0, self.h - self.h / 20, self.w, self.h / 20)
        self.goal_boss = pygame.Rect(0, 0, self.w, self.h / 20)
        self.barre = pygame.Rect(0, self.goal_player.y - self.h / 30 - 1, self.w / 4, self.h / 30)
        self.barre_boss = [pygame.Rect(0, self.goal_boss.bottom + 1 + nb * (self.h / 30 + 1), self.w, self.h / 30) for nb in range(self.life)]

        self.balle_radius = self.h / 40
        self.balle_pos = [self.w / 2, self.h / 2]
        angle = random() * pi
        self.angleX = cos(angle)
        self.angleY = sin(angle)

        coeur = pygame.image.load("miniGame/PingPong/coeur.png")
        self.coeur = pygame.transform.scale(coeur, (self.h / 10, self.h / 10))

    def draw(self):
        pygame.draw.rect(self.screen, (50, 50, 50), self.goal_player)
        pygame.draw.rect(self.screen, (50, 50, 50), self.goal_boss)
        pygame.draw.rect(self.screen, (255, 0, 0), self.barre)
        for i in range(len(self.barre_boss)):
            pygame.draw.rect(self.screen, (255, 0, 255), self.barre_boss[i])
            if i + 1 == len(self.barre_boss):
                self.screen.blit(self.coeur, (self.barre_boss[i].x - self.coeur.get_width() / 2, self.barre_boss[i].y - self.coeur.get_height() / 2))
        pygame.draw.circle(self.screen, (0, 255, 0), self.balle_pos, self.balle_radius)

    def update(self):
        self.barre.x = pygame.mouse.get_pos()[0] - self.barre.width / 2
        if self.barre.x < 0:
            self.barre.x = 0
        elif self.barre.right > self.w:
            self.barre.x = self.w - self.barre.width
        if len(self.barre_boss) > 0:
            self.barre_boss[-1].x = (self.balle_pos[0] - self.barre_boss[-1].width / 2)
            if self.barre_boss[-1].x < 0:
                self.barre_boss[-1].x = 0
            elif self.barre_boss[-1].right > self.w:
                self.barre_boss[-1].x = self.w - self.barre_boss[-1].width

        self.move_balle()

    def move_balle(self):
        new_pos = [self.balle_pos[0] + self.angleX * self.speed, self.balle_pos[1] + self.angleY * self.speed]
        if new_pos[0] - self.balle_radius < 0:
            self.angleX = -self.angleX
        elif new_pos[0] + self.balle_radius > self.w:
            self.angleX = -self.angleX
        if new_pos[1] - self.balle_radius < 0:
            if len(self.barre_boss) == 0:
                self.victoire = True
                self.running = False
        elif new_pos[1] + self.balle_radius > self.h:
            self.restart()

        if new_pos[1] + self.balle_radius > self.barre.y:
            if self.barre.left < self.balle_pos[0] < self.barre.right:
                self.angleY = - self.angleY
                if self.life > 2:
                    self.angleX = cos((random() - 0.5) * 2)

        rect = pygame.Rect(self.balle_pos[0] - self.balle_radius, self.balle_pos[1] - self.balle_radius, self.balle_radius * 2, self.balle_radius * 2)
        if len(self.barre_boss) > 0:
            if rect.colliderect(self.barre_boss[-1]):
                self.angleY = -self.angleY
                self.speed += 1
                self.barre_boss[-1].width -= self.w / 15
                if self.barre_boss[-1].width < self.w / 15:
                    self.barre_boss.pop(-1)

        self.balle_pos[0] += self.angleX * self.speed
        self.balle_pos[1] += self.angleY * self.speed

    def restart(self):
        self.victoire = False
        self.speed = 4 * self.life

        self.goal_player = pygame.Rect(0, self.h - self.h / 20, self.w, self.h / 20)
        self.goal_boss = pygame.Rect(0, 0, self.w, self.h / 20)
        self.barre = pygame.Rect(0, self.goal_player.y - self.h / 30 - 1, self.w / 4, self.h / 30)
        self.barre_boss = [pygame.Rect(0, self.goal_boss.bottom + 1 + nb * (self.h / 30 + 1), self.w, self.h / 30) for nb in range(self.life)]

        self.balle_radius = self.h / 40
        self.balle_pos = [self.w / 2, self.h / 2]
        angle = random() * pi
        self.angleX = cos(angle)
        self.angleY = sin(angle)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.update()
            self.draw()
            self.ecran.blit(self.screen, (0, 0))
            pygame.display.flip()
            clock.tick(60)
