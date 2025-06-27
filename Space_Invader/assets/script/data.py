from dataclasses import dataclass
import pygame


class Data:

    def __init__(self, screen):
        self.screen = screen
        self.un = self.screen.get_height() / 480

        self.powers = {
            "health": {"image": self.load_image("assets/images/powers/health.png", (self.screen.get_height() / 20, self.screen.get_height() / 20)), "proba": 18},
            "max_health": {"image": self.load_image("assets/images/powers/max_health.png", (self.screen.get_height() / 20, self.screen.get_height() / 20)), "proba": 2},
            "damage": {"image": self.load_image("assets/images/powers/damage.png", (self.screen.get_height() / 20, self.screen.get_height() / 20)), "proba": 10},
            "shot_speed": {"image": self.load_image("assets/images/powers/shot_speed.png", (self.screen.get_height() / 20, self.screen.get_height() / 20)), "proba": 10},
            "cooldown": {"image": self.load_image("assets/images/powers/cooldown.png", (self.screen.get_height() / 20, self.screen.get_height() / 20)), "proba": 2},
            "multishot": {"image": self.load_image("assets/images/powers/multishot.png", (self.screen.get_height() / 20, self.screen.get_height() / 20)), "proba": 0},
            "speed": {"image": self.load_image("assets/images/powers/speed.png", (self.screen.get_height() / 20, self.screen.get_height() / 20)), "proba": 10},
            "rien": {"image": 0, "proba": 50}
        }
        self.aura = pygame.transform.scale(pygame.image.load("assets/images/powers/aura.png"), (self.screen.get_height() / 10, self.screen.get_height() / 10))

        self.image_player = [
            self.load_image(f"assets/images/player/player{i + 1}.png",
                            (screen.get_width() / 10, screen.get_height() / 9))
            for i in range(4)
        ]
        self.image_tir = {
            "blaster_vert": pygame.image.load("assets/images/tirs/tir_vert.png"),
            "blaster_rouge": pygame.image.load("assets/images/tirs/tir_rouge.png"),
            "blaster_bleu": pygame.image.load("assets/images/tirs/tir_bleu.png"),
            "blaster_jaune": pygame.image.load("assets/images/tirs/tir_jaune.png"),
            "blaster_violet": pygame.image.load("assets/images/tirs/tir_violet.png"),
            "blaster_blanc": pygame.image.load("assets/images/tirs/tir_blanc.png"),
            "mine": pygame.image.load("assets/images/tirs/mine.png"),
            "boom": pygame.image.load("assets/images/tirs/boom.png")
        }
        self.boom = {
            j*9+i: self.get_boom(i, j) for j in range(9) for i in range(9)
        }
        self.size_enemy = {
            "normal": (screen.get_width() / 15, screen.get_height() / 13),
            "speed": (screen.get_width() / 20, screen.get_height() / 8),
            "tank": (screen.get_width() / 15, screen.get_height() / 13),
            "damage": (screen.get_width() / 20, screen.get_height() / 8),
            "boss1": (screen.get_width() / 7, screen.get_height() / 2.5),
        }
        self.image_enemy = {
            "normal": self.load_image("assets/images/enemy/normal.png", self.size_enemy["normal"]),
            "speed": self.load_image("assets/images/enemy/speed.png", self.size_enemy["speed"]),
            "tank": self.load_image("assets/images/enemy/tank.png", self.size_enemy["tank"]),
            "damage": self.load_image("assets/images/enemy/damage.png", self.size_enemy["damage"]),
            "boss1": self.load_image("assets/images/enemy/boss1.png", self.size_enemy["boss1"]),
        }
        self.image_shadow_enemy = {
            "normal": self.load_image("assets/images/menu/shadow_enemy/normal_shadow.png", self.size_enemy["normal"]),
            "speed": self.load_image("assets/images/menu/shadow_enemy/speed_shadow.png", self.size_enemy["speed"]),
            "tank": self.load_image("assets/images/menu/shadow_enemy/tank_shadow.png", self.size_enemy["tank"]),
            "damage": self.load_image("assets/images/menu/shadow_enemy/damage_shadow.png", self.size_enemy["damage"]),
            "boss1": self.load_image("assets/images/menu/shadow_enemy/boss1_shadow.png", self.size_enemy["boss1"]),
        }

        self.level = {
            0: [[]],
            1: [[(5, "normal")]],
            2: [[(2, "normal"), (5, "normal")]],
            3: [[(7, "normal"), (4, "normal"), (5, "normal")]],
            4: [[(17, "normal")]],
            5: [[(20, "normal")]],
            6: [[(5, "normal"), (5, "speed")]],
            7: [[(5, "normal"), (10, "speed"), (5, "normal")]],
            8: [[(10, "normal"), (5, "speed"), (5, "normal"), (10, "speed")]],
            9: [[(20, "normal"), (20, "speed")]],
            10: [[(7, "normal"), (7, "speed"), (1, "boss1")]],
        }

        self.police = pygame.font.Font(pygame.font.get_default_font(), int(self.screen.get_height() / 30))
        self.font_accueil = pygame.font.Font(pygame.font.get_default_font(), int(self.screen.get_height() / 20))
        self.menu = {
            "image_fond": pygame.transform.scale(pygame.image.load("assets/images/menu/fond_menu.png"), self.screen.get_size()),
        }

    def get_boom(self, x, y):
        image = pygame.Surface((100, 100))
        image.blit(self.image_tir["boom"], (0, 0), (x * 100, y * 100, 100, 100))
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.scale(image, (self.screen.get_height() / 30, self.screen.get_height() / 30))
        return image

    def load_image(self, path, size):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, size)
        return image
