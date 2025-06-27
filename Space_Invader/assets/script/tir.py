import pygame


class Blaster:

    def __init__(self, damage, speed, position, angle, image):
        self.damage = damage
        self.speed = speed
        self.position = position
        self.angle = angle
        self.image = self.rotate_image(image)

    def rotate_image(self, image):
        image = pygame.transform.rotate(image, self.angle)
        return image


class Missile:

    def __init__(self, damage, speed, position, cible, image):
        self.damage = damage
        self.speed = speed
        self.position = position
        self.cible = cible
        self.image = image
