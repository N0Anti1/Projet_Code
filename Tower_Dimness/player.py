# -*- coding: cp1252 -*-

import pygame
import animation


class Entity(animation.AnimateSprite):

    def __init__(self, name, x, y, speed):
        super().__init__(name)
        self.name = name
        self.position = [x, y]
        self.speed = speed
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width / 2, self.rect.height / 2)
        self.old_position = self.position.copy()
        self.direction = f"{self.name}_down"

    def save_location(self):
        self.old_position = self.position.copy()

    def update_animation(self, direction):
        self.animate(direction)

    def move_player(self, direction):
        self.save_location()
        if direction == "RIGHT":
            self.position[0] += self.speed
            self.direction = f"{self.name}_right"
            self.update_animation(self.direction)
        elif direction == "LEFT":
            self.position[0] -= self.speed
            self.direction = f"{self.name}_left"
            self.update_animation(self.direction)
        if direction == "DOWN":
            self.position[1] += self.speed
            self.direction = f"{self.name}_down"
            self.update_animation(self.direction)
        elif direction == "UP":
            self.position[1] -= self.speed
            self.direction = f"{self.name}_up"
            self.update_animation(self.direction)

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):

    def __init__(self):
        super().__init__("player", 0, 0, 2)
        self.inventory = ""
        self.objet_stocker = ""
        self.durability = 1
        self.degat = 1
        self.life = 3
        self.last_damage = 0

    def consume(self):
        self.durability -= self.degat
        if self.durability <= 0:
            self.inventory = ""
            self.objet_stocker = ""


class Inventaire:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.images = {
            "cadre": self.load_image("cadre"),
            "Epee": self.load_image("Epee"),
            "Cle": self.load_image("Cle"),
            "Champignon": self.load_image("Champignon"),
            "Hache": self.load_image("Hache")
        }

    def draw(self, item):
        if item != "":
            self.screen.blit(self.images[item], (0, 0))
        self.screen.blit(self.images["cadre"], (0, 0))

    def load_image(self, name):
        image = pygame.image.load(f"assets/items/{name}.png")
        image = pygame.transform.scale(image, (int(self.screen.get_height() / 10), int(self.screen.get_height() / 10)))
        return image


class NPC(Entity):

    def __init__(self, name, nb_points, dialog):
        super().__init__(name, 0, 0, 1)
        self.name = name
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.current_point = 0

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_player("DOWN")
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_player("UP")
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_player("RIGHT")
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_player("LEFT")

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)


class Items(pygame.sprite.Sprite):

    def __init__(self, link, name, index, degat, screen=pygame.Surface, x=-1000, y=-1000):
        super().__init__()
        self.link = link
        self.name = name
        self.index = index
        self.degat = degat
        self.screen = screen
        self.image = pygame.image.load(f"assets/items/{link}.png")
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(x, y, self.rect.width, self.rect.height)

    def update(self):
        self.rect.topleft = self.position


class Enemy(pygame.sprite.Sprite):

    def __init__(self, name, x, y, speed, life, zone):
        super().__init__()

        self.sprite_sheet = pygame.image.load(f"assets/sprites/{name}.png")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey((0, 0, 0))

        self.name = name
        self.speed = speed
        self.life = life
        self.zone_rect = zone
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width / 2, self.rect.height / 2)
        self.old_position = self.position.copy()
        self.direction = f"{self.name}_right"

        # définir un dictionnaire qui va contenir les images chargés de chaques sprite
        self.animation = {
            f"{name}_left": self.load_animation_image(0),
            f"{name}_right": self.load_animation_image(1),
        }
        self.current_image = 0
        self.images = self.animation.get(self.direction)

    # Méthode pour animer le sprite
    def animate(self):
        self.images = self.animation.get(self.direction)

        # Passer à l'image suivante
        self.current_image += 0.2
        if self.current_image >= len(self.images):
            self.current_image = 0

        # Modifier l'image précédente
        self.image = self.images[int(self.current_image)]

    def get_image(self, x, y):
        image = pygame.Surface((16, 16))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16))
        return image

    # définir une fonction pour charger les images d'un sprite
    def load_animation_image(self, y_position):
        # charger les images du sprite
        images = []

        # boucler sur chaque image
        for num in range(0, 12):

            image_path = self.get_image(num * 16, y_position * 16)
            image_path.set_colorkey((0, 0, 0))
            images.append(image_path)

        # renvoyer le contenu de la liste d'image
        return images

    def save_location(self):
        self.old_position = self.position.copy()

    def update_animation(self):
        self.animate()

    def move(self, direction, collision: list[pygame.Rect]):
        if direction == "RIGHT":
            new_rect = pygame.Rect(self.position[0] + self.speed, self.position[1], self.rect.width, self.rect.height)
            if new_rect.collidelist(collision) <= -1:
                self.position[0] += self.speed
                self.direction = f"{self.name}_right"
        elif direction == "LEFT":
            new_rect = pygame.Rect(self.position[0] - self.speed, self.position[1], self.rect.width, self.rect.height)
            if new_rect.collidelist(collision) <= -1:
                self.position[0] -= self.speed
            self.direction = f"{self.name}_left"
        elif direction == "DOWN":
            new_rect = pygame.Rect(self.position[0], self.position[1] + self.speed, self.rect.width, self.rect.height)
            if new_rect.collidelist(collision) <= -1:
                self.position[1] += self.speed
        elif direction == "UP":
            new_rect = pygame.Rect(self.position[0], self.position[1] - self.speed, self.rect.width, self.rect.height)
            if new_rect.collidelist(collision) <= -1:
                self.position[1] -= self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.update_animation()

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_damage(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()
