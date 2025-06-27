# -*- coding: cp1252 -*-

import os.path
import time
import random


class Encodeur:

    def __init__(self, message_entrant, message_sortant):

        self.message_entrant = message_entrant
        self.message_sortant = message_sortant

        self.dictionnaire = {
            "à": "Ã ", "è": "Ã¨", "ì": "Ã¬", "ò": "Ã²", "ù": "Ã¹", "À": "Ã€", "È": "Ãˆ", "Ì": "ÃŒ", "Ò": "Ã’", "Ù": "Ã™",
            "á": "Ã¡", "é": "Ã©", "í": "Ã­", "ó": "Ã³",
            "â": "Ã¢", "ê": "Ãª", "î": "Ã®", "ô": "Ã´", "û": "Ã»", "Â": "Ã‚", "Ê": "ÃŠ", "Î": "ÃŽ", "Ô": "Ã”", "Û": "Ã›",
            "ã": "Ã£", "ñ": "Ã±", "õ": "Ãµ", "Õ": "Ã•", "Ã": "Ãƒ", "Ñ": "Ã‘",
            "ä": "Ã¤", "ë": "Ã«", "ï": "Ã¯", "ö": "Ã¶", "Ö": "Ã–", "Ü": "Ãœ", "Ÿ": "Å¸",
            "å": "Ã¥", "Å": "Ã…",
            "æ": "Ã¦", "Æ": "Ã†", "œ": "Å“", "Œ": "Â’",
            "ç": "Ã§", "Ç": "Ã‡",
            "ø": "Ã¸", "Ø": "Ã˜",
            "¿": "Â¿", "¡": "Â¡", "ß": "ÃŸ", "§": "Â§", "µ": "Âµ", "£": "Â£", "¨": "Â¨", "°": "Â°", "²": "Â²", "¤": "Â¤",
            "'": "â€™"
        }

        self.lettre_code = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "?", ".", "/", ",", ";", ":", "!", "&", "#", "{", "}", "(", ")", "[", "]", "-", "_", "|", "@", "=", "+"
        ]

    def encoder(self):
        replace_truc = self.lettre_code.copy()
        with open(self.message_entrant, "r") as coder:
            message = coder.read()
            for lettre in self.dictionnaire:
                if self.dictionnaire[lettre] in message:
                    message = message.replace(self.dictionnaire[lettre], lettre)

        seeds = int(time.time() / 2)
        random.seed(seeds)

        ch0 = random.choice(replace_truc)
        replace_truc.remove(ch0)
        ch1 = random.choice(replace_truc)
        replace_truc.remove(ch1)
        chnm = random.choice(replace_truc)
        replace_truc.remove(chnm)
        chsl = random.choice(replace_truc)
        replace_truc.remove(chsl)

        char = []
        decode = []
        melange = []
        for i in range(32, 854):
            if i >= 127:
                i += 34
            char.append(i)
            decode.append(i)

        for i in range(len(decode)):
            rand = random.choice(decode)
            decode.remove(rand)
            melange.append(rand)

        new_message = ""
        for lettre in range(len(message)):
            try:
                place = char.index(ord(message[lettre]))
                mot_coder = bin(melange[place]).replace("0b", chnm)
                new_mot_coder = f"{chnm}"
                for lettre in mot_coder:
                    if lettre == "0":
                        new_mot_coder += ch0
                    elif lettre == "1":
                        new_mot_coder += ch1
                truc1 = []
                for chiffre in new_mot_coder:
                    truc1.append(chiffre)
                truc2 = ""
                for t in truc1:
                    truc2 += t
                new_message += truc2
            except ValueError:
                new_message += chsl

        new_message_new = ""
        for caractere in range(len(new_message)):
            new_message_new += new_message[caractere]
            if (caractere + 1) % 1000 == 0:
                new_message_new += "\n"

        with open(self.message_sortant, "w+") as file:
            file.write(new_message_new)
            file.close()

        if self.deencoder() != message + "\n":
            print("LE mEssaGE est MAl cODé")

    def deencoder(self):
        replace_truc = self.lettre_code.copy()

        temps = int(os.path.getmtime(self.message_sortant) / 2)
        random.seed(temps)

        ch0 = random.choice(replace_truc)
        replace_truc.remove(ch0)
        ch1 = random.choice(replace_truc)
        replace_truc.remove(ch1)
        chnm = random.choice(replace_truc)
        replace_truc.remove(chnm)
        chsl = random.choice(replace_truc)
        replace_truc.remove(chsl)

        char = []
        decode = []
        melange = []
        for i in range(32, 854):
            if i >= 127:
                i += 34
            char.append(i)
            decode.append(i)

        for i in range(len(decode)):
            rand = random.choice(decode)
            decode.remove(rand)
            melange.append(rand)

        message_decode = ""
        with open(self.message_sortant, "r") as file:
            message_coder = file.read().replace("\n", "").split(chsl)
            for phrase in message_coder:
                mots = phrase.split(chnm)
                mots.pop(0)
                for mot in mots:
                    for truc in replace_truc:
                        if truc in mot:
                            mot = mot.replace(truc, "")
                    mot_coder = ""
                    for lettre in mot:
                        if lettre == ch0:
                            mot_coder += "0"
                        elif lettre == ch1:
                            mot_coder += "1"
                    message_decode += chr(char[melange.index(int(mot_coder, 2))])
                message_decode += "\n"
            file.close()
        return message_decode
