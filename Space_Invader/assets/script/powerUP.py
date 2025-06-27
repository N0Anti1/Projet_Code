import random

import pygame


class PowerUP:

    def __init__(self, position, screen, data):
        self.position = position
        self.screen = screen
        self.data = data
        self.powers = {
            "health": {"image": pygame.Surface((32, 32)), "proba": 10}
        }
        self.name = "health"
        name = [key for key in self.data.powers.keys()]
        proba = [self.data.powers[key]["proba"] for key in name]
        rand = random.randint(0, 100)
        for n in range(len(name)):
            rand -= proba[n]
            if rand <= 0:
                self.name = name[n]
                break
        self.image = self.data.powers[self.name]["image"]
