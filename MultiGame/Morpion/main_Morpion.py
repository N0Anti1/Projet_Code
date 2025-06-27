import pygame


class Morpion:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0))
        self.SIDE = True
        self.SIZE = int(self.screen.get_height() / 3)
        if 3 * self.SIZE > self.screen.get_width():
            self.SIZE = int(self.screen.get_width() / 3)
            self.SIDE = False
        self.LEFT = (self.screen.get_width() - 3 * self.SIZE) / 2
        self.TOP = (self.screen.get_height() - 3 * self.SIZE) / 2

        self.running = True

        self.croix_exit = pygame.image.load('../Morpion/croix.png')
        self.croix_exit = pygame.transform.scale(self.croix_exit, (self.SIZE / 4, self.SIZE / 4))
        self.croix_rect = self.croix_exit.get_rect()
        self.croix_rect.x = self.screen.get_width() - self.croix_exit.get_width()
        self.croix_rect.y = 0
        self.police = pygame.font.Font('Roboto.ttf', self.SIZE)
        self.score_rouge = 0
        self.score_bleu = 0
        # Tour de jeu : True = Rouge et False = Bleu
        self.tour = True
        self.victoire = False
        self.tableau = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def draw_grid(self):
        self.screen.blit(self.croix_exit, (self.screen.get_width() - self.croix_exit.get_width(), 0))
        message_r = self.police.render(f"{self.score_rouge}", True, (255, 0, 0))
        message_b = self.police.render(f"{self.score_bleu}", True, (0, 0, 255))
        if self.SIDE:
            self.screen.blit(message_r, (self.LEFT - message_r.get_width(), (self.screen.get_height() - message_r.get_height()) / 2))
            self.screen.blit(message_b, (self.LEFT + 3 * self.SIZE, (self.screen.get_height() - message_b.get_height()) / 2))
        else:
            self.screen.blit(message_r, ((self.screen.get_width() - message_r.get_width()) / 2, self.TOP - message_r.get_height()))
            self.screen.blit(message_b, ((self.screen.get_width() - message_b.get_width()) / 2, self.TOP + 3 * self.SIZE))
        for y in range(len(self.tableau)):
            for x in range(len(self.tableau[y])):
                if self.tableau[y][x] == 1:
                    pygame.draw.rect(self.screen, (255, 0, 0), (self.LEFT + x * self.SIZE + self.SIZE / 3, self.TOP + y * self.SIZE + self.SIZE / 3, int(self.SIZE / 3), int(self.SIZE / 3)), int(self.SIZE / 10))
                if self.tableau[y][x] == 10:
                    pygame.draw.circle(self.screen, (0, 0, 255), (self.LEFT + x * self.SIZE + self.SIZE / 2, self.TOP + y * self.SIZE + self.SIZE / 2), self.SIZE / 3)
                    pygame.draw.circle(self.screen, (255, 255, 255), (self.LEFT + x * self.SIZE + self.SIZE / 2, self.TOP + y * self.SIZE + self.SIZE / 2), self.SIZE / 4)
                pygame.draw.rect(self.screen, (255, 0, 0) if self.tour and not self.victoire else (0, 0, 255) if not self.victoire else (0, 0, 0), (self.LEFT + x * self.SIZE, self.TOP + y * self.SIZE, self.SIZE, self.SIZE), int(self.SIZE / 10))

    def clic(self, x, y):
        if self.tableau[y][x] == 0:
            if self.tour:
                self.tableau[y][x] = 1
            else:
                self.tableau[y][x] = 10
            self.tour = not self.tour
            self.verif_win()

    def verif_win(self):
        le_compte = 0
        ligne = [0 for _ in range(len(self.tableau[0]))]
        for y in range(len(self.tableau)):
            for x in range(len(self.tableau[y])):
                ligne[x] += self.tableau[y][x]
            if self.tableau[y].count(self.tableau[y][0]) == 3 and self.tableau[y][0] > 0:
                self.victoire = True
                le_compte = 3 * self.tableau[y][0]
        for num in ligne:
            if num == 3:
                self.victoire = True
                le_compte = num
            elif num == 30:
                self.victoire = True
                le_compte = num
        if self.tableau[0][0] == self.tableau[1][1] == self.tableau[2][2] > 0:
            self.victoire = True
            le_compte = 3 * self.tableau[1][1]
        if self.tableau[2][0] == self.tableau[1][1] == self.tableau[0][2] > 0:
            self.victoire = True
            le_compte = 3 * self.tableau[1][1]

        if self.victoire:
            if le_compte == 3:
                self.score_rouge += 1
            else:
                self.score_bleu += 1

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.victoire:
                        compte = 0
                        for x in range(3):
                            compte += self.tableau[x].count(0)
                        self.tour = False if (self.tour and compte % 2 == 1) or (not self.tour and compte % 2 == 0) else True
                        self.tableau = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                        self.victoire = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        x, y = event.pos
                        x -= self.LEFT
                        y -= self.TOP
                        x //= self.SIZE
                        y //= self.SIZE
                        if 0 <= x < 3 and 0 <= y < 3 and not self.victoire:
                            self.clic(int(x), int(y))
                    if self.croix_rect.collidepoint(event.pos):
                        self.running = False

            self.draw_grid()
            pygame.display.flip()

        pygame.quit()
