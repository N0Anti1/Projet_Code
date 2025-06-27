class IA_Demineur:

    def __init__(self, largeur, hauteur):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur

        self.vide = []
        self.pioche = []
        self.pioche1 = []
        self.pioche2 = []
        self.pioche3 = []
        self.pioche4 = []
        self.pioche5 = []
        self.pioche6 = []
        self.pioche7 = []
        self.pioche8 = []
        self.drapeau = []

    def information(self, clic, pioche: tuple[int, int], valeur):
        if clic == "gauche":
            if valeur == 1:
                self.vide.append(pioche)
                self.pioche1.append(pioche)
            elif valeur == 2:
                self.vide.append(pioche)
                self.pioche2.append(pioche)
            elif valeur == 3:
                self.vide.append(pioche)
                self.pioche3.append(pioche)
            elif valeur == 4:
                self.vide.append(pioche)
                self.pioche4.append(pioche)
            elif valeur == 5:
                self.vide.append(pioche)
                self.pioche5.append(pioche)
            elif valeur == 6:
                self.vide.append(pioche)
                self.pioche6.append(pioche)
            elif valeur == 7:
                self.vide.append(pioche)
                self.pioche7.append(pioche)
            elif valeur == 8:
                self.vide.append(pioche)
                self.pioche8.append(pioche)
            else:
                self.vide.append(pioche)
                self.pioche.append(pioche)
        elif clic == "droit":
            if valeur == 1:
                self.drapeau.append(pioche)
            else:
                self.drapeau.remove(pioche)

    # PHASE 1

    def count(self, x, y, valeur):
        vide = 0
        drapeau = 0
        inconnu = 0
        for i in range(3):
            for j in range(3):
                if (x + i - 1, y + j - 1) in self.vide:
                    vide += 1
                elif (x + i - 1, y + j - 1) in self.drapeau:
                    drapeau += 1
                elif 0 > x + i - 1 or 0 > y + j - 1:
                    vide += 1
                elif self.LARGEUR <= x + i - 1 or self.HAUTEUR <= y + j - 1:
                    vide += 1
                else:
                    inconnu += 1
        if drapeau == valeur:
            return "pioche"
        elif inconnu + drapeau == valeur:
            return "drapeau"
        else:
            return "JSP"

    def quoi_faire(self, x, y):
        quoi_faire = []
        for i in range(3):
            for j in range(3):
                if (x + i - 1, y + j - 1) in self.pioche:
                    quoi_faire.append(1)
                elif (x + i - 1, y + j - 1) in self.vide:
                    if (x + i - 1, y + j - 1) in self.pioche1:
                        num_valeur = 1
                    elif (x + i - 1, y + j - 1) in self.pioche2:
                        num_valeur = 2
                    elif (x + i - 1, y + j - 1) in self.pioche3:
                        num_valeur = 3
                    elif (x + i - 1, y + j - 1) in self.pioche4:
                        num_valeur = 4
                    elif (x + i - 1, y + j - 1) in self.pioche5:
                        num_valeur = 5
                    elif (x + i - 1, y + j - 1) in self.pioche6:
                        num_valeur = 6
                    elif (x + i - 1, y + j - 1) in self.pioche7:
                        num_valeur = 7
                    elif (x + i - 1, y + j - 1) in self.pioche8:
                        num_valeur = 8
                    else:
                        print("PASS")
                        num_valeur = 10
                    if self.count(x + i - 1, y + j - 1, num_valeur) == "pioche":
                        quoi_faire.append(1)
                    elif self.count(x + i - 1, y + j - 1, num_valeur) == "drapeau":
                        quoi_faire.append(2)
                    else:
                        quoi_faire.append(3)
                else:
                    quoi_faire.append(3)

        quoi_faire.sort()
        if quoi_faire[0] == 1:
            return "pioche"
        elif quoi_faire[0] == 2:
            return "drapeau"
        else:
            return "JSP"

    # PHASE 2

    def look(self, x: int, y: int):
        drapeau = 0
        case_liee = []
        for i in range(3):
            for j in range(3):
                if (x + i - 1, y + j - 1) not in self.vide:
                    if (x + i - 1, y + j - 1) not in self.drapeau:
                        if x + i - 1 >= 0 and y + j - 1 >= 0:
                            if self.LARGEUR > x + i - 1 and self.HAUTEUR > y + j - 1:
                                case_liee.append((x + i - 1, y + j - 1))
                    else:
                        drapeau += 1
        return case_liee, drapeau

    def reflechi(self):
        tableau_vide = []
        valeur_case_liee = []
        for num in range(len(self.vide)):
            case_liee = self.look(self.vide[num][0], self.vide[num][1])
            tableau_vide.append(case_liee[0])
            if self.vide[num] in self.pioche1:
                valeur_case_liee.append(1 - case_liee[1])
            elif self.vide[num] in self.pioche2:
                valeur_case_liee.append(2 - case_liee[1])
            elif self.vide[num] in self.pioche3:
                valeur_case_liee.append(3 - case_liee[1])
            elif self.vide[num] in self.pioche4:
                valeur_case_liee.append(4 - case_liee[1])
            elif self.vide[num] in self.pioche5:
                valeur_case_liee.append(5 - case_liee[1])
            elif self.vide[num] in self.pioche6:
                valeur_case_liee.append(6 - case_liee[1])
            elif self.vide[num] in self.pioche7:
                valeur_case_liee.append(7 - case_liee[1])
            elif self.vide[num] in self.pioche8:
                valeur_case_liee.append(8 - case_liee[1])
            else:
                valeur_case_liee.append(0)

        quoi_faire = []
        # Pour chaques cases numéroté qui ont pas toutes leurs mines : tableau_vide[p]
        for p in range(len(tableau_vide)):
            if tableau_vide[p] != 0:
                # Tableau de valeur pour chaques case alentour
                case_alentour = []
                valeur_alentour = []
                # pour chaques cases qui sont liées à la case ciblée : tableau_vide[p][t]
                for t in range(len(tableau_vide[p])):
                    x = tableau_vide[p][t][0]
                    y = tableau_vide[p][t][1]
                    # On regarde toutes les cases autour de la case inconnu à la case ciblée : ij
                    for i in range(3):
                        for j in range(3):
                            ij = (x + i - 1, y + j - 1)
                            # Si la case en ij n'est pas la case initiale ou une case inconnu :
                            if ij in self.vide and ij != tableau_vide[p][t]:
                                place = self.vide.index(ij)
                                # On regarde si la case numéroté alentour n'a pas toutes ses mines :
                                if valeur_case_liee[place] != 0:
                                    # Pour toutes les cases inconnus de cette case à proximité qui sont aussi à côté
                                    # de notre case de base :
                                    for a in range(len(tableau_vide[place])):
                                        if tableau_vide[place][a] in tableau_vide[p]:
                                            # ajouter la valeur (mines restantes / place libre) pour chaques cases
                                            # inconnus :
                                            if ij not in case_alentour:
                                                case_alentour.append(ij)
                                                valeur_alentour.append(float(valeur_case_liee[place] / len(tableau_vide[place])))
                                            else:
                                                # index == place dans le tableau
                                                index = case_alentour.index(ij)
                                                valeur_alentour[index] = valeur_alentour[index] + float(valeur_case_liee[place] / len(tableau_vide[place]))
                # Pour chaques valeurs récupérer, on regarde si on retrouve une proba de 1 sur une case :
                for val in range(len(valeur_alentour)):
                    valeur_restante = valeur_case_liee[p] - (valeur_alentour[val] / 2)
                    # Si la valeur de toutes les cases d'une même zone est entière, ça veut dire qu'il reste une case
                    # avec une autre proba à 1 ou à 0 :
                    if valeur_restante.is_integer() and valeur_restante >= 0:
                        if valeur_restante == 0:
                            for where in range(len(tableau_vide[p])):
                                if tableau_vide[p][where] not in tableau_vide[self.vide.index(case_alentour[val])]:
                                    quoi_faire.append(tableau_vide[p][where])
                                    quoi_faire.append("creuse")
                        elif len(tableau_vide[p]) - len(tableau_vide[self.vide.index(case_alentour[val])]) == valeur_restante:
                            for where in range(len(tableau_vide[p])):
                                if tableau_vide[p][where] not in tableau_vide[self.vide.index(case_alentour[val])]:
                                    quoi_faire.append(tableau_vide[p][where])
                                    quoi_faire.append("drapeau")
        return quoi_faire

    def clean(self):
        quoi_faire = []
        for l in range(self.LARGEUR):
            for h in range(self.HAUTEUR):
                if (l, h) not in self.vide and (l, h) not in self.drapeau:
                    quoi_faire.append((l, h))
        return quoi_faire
