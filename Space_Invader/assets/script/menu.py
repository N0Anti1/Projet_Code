import pygame


class MenuAccueil:

    def __init__(self, screen: pygame.Surface, data):
        self.screen = screen
        self.data = data
        self.menu = True
        self.menuType = 0
        self.lastMenu = 0

        self.menus = [
            [self.new_message("Jouer", (255, 255, 255)),
             self.new_message("Enemypedia", (255, 255, 255)),
             self.new_message("Quitter le jeu", (255, 255, 255))
             ], [
                self.new_message("Reprendre", (255, 255, 255)),
                self.new_message("Enemypedia", (255, 255, 255)),
                self.new_message("Quitter", (255, 255, 255))
            ], [
                self.new_message("Retour", (255, 255, 255)),
            ],
        ]

        self.between_shadow = self.screen.get_width() / 15
        self.pedia_left = self.between_shadow * 2

    def move_pedia(self, player):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.pedia_left -= player.speed
        elif pressed[pygame.K_LEFT]:
            self.pedia_left += player.speed

    def new_message(self, text, couleur):
        return self.data.font_accueil.render(text, False, couleur)
