import random
import pygame


class CarDrive:

    def __init__(self, screen: pygame.Surface):

        self.screen = screen
        self.running = True
        self.lose = False
        self.police = pygame.font.Font('Anton-Regular.ttf',
                                       int(100 / (1280 / self.screen.get_width())))
        self.point = 0
        self.voiture = (100, 100)
        self.voiture_size = 10
        self.direction = 0

    def draw(self):
        point = self.police.render(f"{self.point}", False, 0)
        self.screen.blit(point, ((self.screen.get_width() - point.get_width()) / 2,
                                 (self.screen.get_height() - point.get_height()) / 2, ))

        pygame.draw.circle(self.screen, (0, 0, 255), self.voiture, self.voiture_size)


    def update(self):
        self.screen.fill((240, 240, 240))

        self.draw()

    def reset(self):
        self.point = 0

    # Fonction pour le lançage manuel
    def run(self):
        clock = pygame.time.Clock()
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.lose:
                self.reset()

            self.update()
            clock.tick(60)
            pygame.display.flip()

        pygame.quit()


pygame.init()
screen = pygame.display.set_mode((1260, 720))
game = CarDrive(screen)
game.run()
