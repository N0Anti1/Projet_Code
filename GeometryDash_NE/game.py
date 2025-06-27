import pygame


class GeometryDash:

    def __init__(self):
        self.running = True
        self.LARGEUR = 800
        self.HAUTEUR = 500
        self.size = 40
        self.screen = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR))

        # >>>>> Terrain >>>>>
        self.terrain = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 2],
        ]
        self.terrain_size = len(self.terrain[0])
        for y in range(self.HAUTEUR//self.size+1):
            if y == len(self.terrain):
                self.terrain.append([])
            for x in range(self.terrain_size):
                if x == len(self.terrain[y]):
                    self.terrain[y].append(0)
        self.player_position = [2, 1]
        self.images = {
            "terrain": self.load_image("terrain"),
            "pique": self.load_image("pique"),
            "player": self.load_image("player"),
            "background": self.load_image("background"),
        }
        # <<<<< Terrain <<<<<
        # >>>>> Caméra >>>>>
        self.ScrollPosition = 0
        self.speed = 5
        self.countSpeed = 0

        self.fallBlock = 0
        self.jump = 0
        self.jumpSpeed = self.speed*2
        # <<<<< Caméra <<<<<

        self.run()

    def load_image(self, path):
        image = pygame.image.load(f"assets/{path}.png")
        if path == "background":
            image = pygame.transform.scale(image, (self.LARGEUR, self.HAUTEUR))
        else:
            image = pygame.transform.scale(image, (self.size, self.size))
        return image

    def draw(self):
        self.screen.blit(self.images["background"], (0, 0))
        for y in range(len(self.terrain)):
            for x in range(len(self.terrain[y])):
                if self.terrain[y][x] == 1:
                    self.screen.blit(self.images["terrain"], (x*self.size-self.ScrollPosition, self.HAUTEUR-self.size*(y+1)))
                elif self.terrain[y][x] == 2:
                    self.screen.blit(self.images["pique"], (x*self.size-self.ScrollPosition, self.HAUTEUR-self.size*(y+1)))
                if [x, y] == self.player_position:
                    self.screen.blit(self.images["player"], (2*self.size, self.HAUTEUR-(self.player_position[1]+1)*self.size+self.fallBlock*self.size/(self.jumpSpeed)))

    def move(self, direction):
        Xplus, Yplus = direction

        x, y = self.player_position
        # Déplacement horizontal
        if self.terrain[y][x+Xplus] == 0:
            self.player_position = [x+Xplus, y]
        elif self.terrain[y][x+Xplus] == 2:
            print("mort")
        elif self.terrain[y][x+Xplus] == 1:
            print("mort")

        x, y = self.player_position
        # Déplacement vertical
        if self.terrain[y+Yplus][x] == 0:
            self.player_position = [x, y+Yplus]
        elif self.terrain[y+Yplus][x] == 2:
            print("mort")

    def update(self):
        self.countSpeed += 1
        if self.countSpeed % self.speed == 0:
            self.move((1, 0))
        self.ScrollPosition += self.size/self.speed
        x, y = self.player_position
        if self.jump <= 0:
            if self.terrain[y-1][x] != 1:
                self.jump -= 1
                self.fallBlock -= self.jump
                if self.fallBlock > self.jumpSpeed:
                    self.fallBlock = 0
                    self.move((0, -1))
            else:
                self.jump = 0
        else:
            if self.terrain[y+1][x] != 1:
                self.fallBlock -= self.jump
                self.jump -= 1
                if abs(self.fallBlock) > self.jumpSpeed:
                    self.fallBlock = 0
                    self.move((0, 1))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jump = 10

            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
