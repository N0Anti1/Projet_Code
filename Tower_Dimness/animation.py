# -*- coding: cp1252 -*-

import pygame


# définir une class qui gère les animations
class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"assets/sprites/{name}.png")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey((0, 0, 0))
        self.state = f"{name}_down"
        self.shoot = False
        self.mort = False

        # définir un dictionnaire qui va contenir les images chargés de chaques sprite
        self.animation = {
            f"{name}_down": self.load_animation_image(0, 0),
            f"{name}_left": self.load_animation_image(1, 0),
            f"{name}_right": self.load_animation_image(2, 0),
            f"{name}_up": self.load_animation_image(3, 0),
            f"{name}_down_active": self.load_animation_image(0, 1),
            f"{name}_left_active": self.load_animation_image(1, 1),
            f"{name}_right_active": self.load_animation_image(2, 1),
            f"{name}_up_active": self.load_animation_image(3, 1),
            "dead": self.load_animation_image(0, 2)
        }
        self.current_image = 0
        self.images = self.animation.get(self.state)

    # Méthode pour animer le sprite
    def animate(self, direction):
        self.state = direction
        if self.shoot:
            self.images = self.animation.get(f"{self.state}_active")
        elif self.mort:
            self.images = self.animation.get("dead")
        else:
            self.images = self.animation.get(self.state)

        # Passer à l'image suivante
        self.current_image += 0.1
        if self.current_image >= len(self.images):
            self.current_image = 0
            self.images = self.animation.get(self.state)
            self.shoot = False
            self.mort = False

        # Modifier l'image précédente
        self.image = self.images[int(self.current_image)]

    def get_image(self, x, y):
        image = pygame.Surface((32, 32))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    # définir une fonction pour charger les images d'un sprite
    def load_animation_image(self, y_position, x_position):
        # charger les images du sprite
        images = []

        # boucler sur chaque image
        for num in range(0, 3):

            image_path = self.get_image(num * 32 + x_position * 96, y_position * 32)
            image_path.set_colorkey((0, 0, 0))
            images.append(image_path)

        # renvoyer le contenu de la liste d'image
        return images
