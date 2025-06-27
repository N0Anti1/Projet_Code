import random

import pygame


class DodgeIt:

    def __init__(self, screen):
        pygame.init()

        self.screen = screen
        self.running = True
        self.police = pygame.font.Font('Dodge_It/Anton-Regular.ttf',
                                       int(100 / (1280 / self.screen.get_width())))

        self.lose = False
        self.ball_radius = 21 / (1280 / self.screen.get_width())
        self.ball = [self.screen.get_width() / 2, self.screen.get_height() / 2]
        self.gravity = .15 / (1280 / self.screen.get_width())
        self.fall = -5 / (1280 / self.screen.get_width())
        self.speed = 1 / (1280 / self.screen.get_width())

        self.point = 0
        self.point_radius = 7 / (1280 / self.screen.get_width())
        self.apple = (random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height()))
        self.death_point = []

    def eat(self):
        self.point += 1
        self.apple = (random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height()))
        self.death_point.append((random.randint(0, self.screen.get_width()),
                                 random.randint(0, self.screen.get_height())))

    def draw(self):
        point = self.police.render(f"{self.point}", False, 0)
        self.screen.blit(point, ((self.screen.get_width() - point.get_width()) / 2,
                                 (self.screen.get_height() - point.get_height()) / 2, ))

        for point in self.death_point:
            pygame.draw.circle(self.screen, (200, 0, 0), point, self.point_radius)
        pygame.draw.circle(self.screen, 0, self.apple, self.point_radius)
        pygame.draw.circle(self.screen, 0, self.ball, self.ball_radius)

    def update(self):
        self.screen.fill((240, 240, 240))

        if self.ball[0] < 0 or self.ball[0] > self.screen.get_width():
            self.lose = True
        if self.ball[1] < 0 or self.ball[1] > self.screen.get_height():
            self.lose = True

        P1 = pygame.Vector2(self.ball)
        for death in self.death_point:
            P2 = pygame.Vector2(death)
            if P1.distance_to(P2) <= self.ball_radius:
                self.lose = True
        P2 = pygame.Vector2(self.apple)
        if P1.distance_to(P2) <= self.ball_radius + self.point_radius:
            self.eat()

        self.ball[1] += self.fall
        self.fall += self.gravity

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: self.speed -= .3 / (1280 / self.screen.get_width())
        if pressed[pygame.K_RIGHT]: self.speed += .3 / (1280 / self.screen.get_width())
        if self.speed >= 3 / (1280 / self.screen.get_width()): self.speed = 3 / (1280 / self.screen.get_width())
        if self.speed <= -3 / (1280 / self.screen.get_width()): self.speed = -3 / (1280 / self.screen.get_width())
        self.ball[0] += self.speed

        self.draw()

    def reset(self):
        self.lose = False
        self.ball = [self.screen.get_width() / 2, self.screen.get_height() / 2]
        self.fall = -5 / (1280 / self.screen.get_width())
        self.speed = 1 / (1280 / self.screen.get_width())

        self.point = 0
        self.apple = (random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height()))
        self.death_point = []

    def run(self):
        clock = pygame.time.Clock()
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.fall -= 3 / (1280 / self.screen.get_width())

            if self.lose:
                self.reset()

            self.update()
            clock.tick(60)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    game = DodgeIt(screen)
    game.run()
