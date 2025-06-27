# -*- coding: cp1252 -*-

import pygame


class DialogBox:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        box = pygame.image.load("assets/dialogs/dialog_box.png")
        self.box = pygame.transform.scale(box, (int(self.screen.get_width() / 1.25), int(self.screen.get_height() / 6)))
        self.box2 = pygame.transform.scale(box, (50, int(self.box.get_width() / 35)))
        gris = pygame.image.load("assets/dialogs/pouce_gris.png")
        vert = pygame.image.load("assets/dialogs/pouce_vert.png")
        rouge = pygame.image.load("assets/dialogs/pouce_rouge.png")
        self.gris = pygame.transform.scale(gris, (int(self.box.get_height() / 2), int(self.box.get_height() / 2)))
        self.vert = pygame.transform.scale(vert, (int(self.box.get_height() / 2), int(self.box.get_height() / 2)))
        self.rouge = pygame.transform.scale(rouge, (int(self.box.get_height() / 2), int(self.box.get_height() / 2)))

        self.X_POSITION = (self.screen.get_width() - self.box.get_width()) / 2
        self.Y_POSITION = self.screen.get_height() - (self.box.get_height() * 1.25)

        self.reading = False
        self.name = ""
        self.message = True
        self.choice = "NONE"
        self.objet = ""
        self.index_objet = ""

        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("assets/dialogs/dialog_font.ttf", int(self.box.get_width() / 35))

    def execute(self):
        if self.reading:
            if self.letter_index >= len(self.texts[self.text_index]) and self.message:
                self.next_text()
            else:
                self.letter_index = 2 * len(self.texts[self.text_index])
        else:
            self.reading = True
            self.text_index = 0
            self.letter_index = 0

    def render(self):
        if self.reading:
            # Afficher la boîte de dialogue
            self.screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            if self.name != "":
                name = self.font.render(self.name[0].upper() + self.name[1:], False, (0, 0, 0))
                self.box2 = pygame.transform.scale(self.box2, (int(name.get_width() * 1.25), int(self.box.get_width() / 35 * 1.25)))
                self.screen.blit(self.box2, (self.X_POSITION + name.get_width() / 2, self.Y_POSITION - name.get_height() / 2))
                self.screen.blit(name, (self.X_POSITION + self.box2.get_width() / 2, self.Y_POSITION - name.get_height() / 2))

            # Afficher le texte
            new_text = self.texts[self.text_index].split("\n")
            for ligne in range(len(new_text)):
                start = 0
                if ligne >= 1:
                    for last_ligne in range(ligne):
                        start += len(new_text[last_ligne])
                if self.letter_index >= start:
                    text = self.font.render(new_text[ligne][0:self.letter_index - start], False, (0, 0, 0))
                    if text.get_width() > self.box.get_width() * 0.8:
                        good_cut = self.letter_index - 1
                        for lettre in range(len(new_text[ligne][:self.letter_index - 1])):
                            if new_text[ligne][lettre] == " ":
                                nt = self.font.render(new_text[ligne][0:lettre], False, (0, 0, 0))
                                if nt.get_width() < self.box.get_width() * 0.8:
                                    good_cut = lettre
                        self.texts[self.text_index] = self.texts[self.text_index][:start + good_cut] + "\n" + self.texts[self.text_index][start + good_cut + 1:]
                    self.screen.blit(text, (self.X_POSITION + self.box.get_width() / 10, self.Y_POSITION + self.box.get_height() / 10 + ligne * text.get_height()))

            if not self.message:
                if self.choice == "LEFT":
                    self.screen.blit(self.rouge, (self.X_POSITION, self.Y_POSITION + self.gris.get_height() / 2))
                    self.screen.blit(self.gris, (self.X_POSITION + self.box.get_width() - self.gris.get_width(),
                                                 self.Y_POSITION + self.gris.get_height() / 2))
                elif self.choice == "RIGHT":
                    new_gris = pygame.transform.rotate(self.gris, 180)
                    self.screen.blit(new_gris, (self.X_POSITION, self.Y_POSITION + self.gris.get_height() / 2))
                    self.screen.blit(self.vert, (self.X_POSITION + self.box.get_width() - self.gris.get_width(),
                                                 self.Y_POSITION + self.gris.get_height() / 2))
                else:
                    self.screen.blit(self.gris, (self.X_POSITION + self.box.get_width() - self.gris.get_width(),
                                                 self.Y_POSITION + self.gris.get_height() / 2))
                    new_gris = pygame.transform.rotate(self.gris, 180)
                    self.screen.blit(new_gris, (self.X_POSITION, self.Y_POSITION + self.gris.get_height() / 2))

            self.letter_index += 1

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            if self.message:
                # fermer le dialogue
                self.reading = False
                self.name = ""
            else:
                self.message = True
                self.texts = [f"Tu as pris l'objet \"{self.name}\"!"]
                self.reading = False
                self.name = ""
                self.execute()
