class IA_Wordle:

    def __init__(self, taille):

        self.TAILLE = taille

        self.file = open(f'../Wordle/word{self.TAILLE}.txt')
        self.liste = self.file.readlines()
        self.dictionnaire = []

        self.start_word = {
            4: "raie",
            5: "raies",
            6: "taries",
            7: "traines",
            8: "notaires",
            9: "notariees",
            10: "coursaient"
        }

        for index in range(len(self.liste)):
            self.dictionnaire.append(self.liste[index].strip('\n'))

        self.mot_ecrit = [self.start_word[self.TAILLE], "", "", "", "", ""]
        self.ligne = 0

    def verif_word(self, mot_ecrit, mot_choisi):
        sequence = [-1 for _ in range(self.TAILLE)]
        for place in range(self.TAILLE):
            if mot_ecrit[place] == mot_choisi[place]:
                sequence[place] = 2
            elif mot_ecrit[place] in mot_choisi:
                if mot_choisi.count(mot_ecrit[place]) >= mot_ecrit.count(mot_ecrit[place]):
                    sequence[place] = 1
            if sequence[place] == -1:
                sequence[place] = 0
        return sequence

    def change_list(self, sequence):
        new_dico = []
        for all_mots in self.dictionnaire:
            mot = True
            for place in range(self.TAILLE):
                if sequence[place] == 0 and self.mot_ecrit[self.ligne - 1][place] in all_mots:
                    if self.mot_ecrit[self.ligne - 1].count(self.mot_ecrit[self.ligne - 1][place]) <= all_mots.count(self.mot_ecrit[self.ligne - 1][place]):
                        mot = False
                elif sequence[place] == 2 and self.mot_ecrit[self.ligne - 1][place] != all_mots[place]:
                    mot = False
                elif sequence[place] == 1:
                    if self.mot_ecrit[self.ligne - 1][place] not in all_mots:
                        mot = False
                    elif self.mot_ecrit[self.ligne - 1][place] == all_mots[place]:
                        mot = False
            if mot:
                new_dico.append(all_mots)
        self.dictionnaire = new_dico.copy()

    def find_score(self, mot):
        resultat = 0
        nb_occurence = 0
        for all_mots in self.dictionnaire:
            resultat += sum(self.verif_word(mot, all_mots))
            nb_occurence += 1
        return resultat / nb_occurence

    def find_best_word(self):
        valeur_max = 0
        for chaque_mots in range(len(self.dictionnaire)):
            score = self.find_score(self.dictionnaire[chaque_mots])
            if score > valeur_max:
                valeur_max = score
                self.mot_ecrit[self.ligne] = self.dictionnaire[chaque_mots]

    # Version manuelle
    def run(self):
        print(f"Écris le mot {self.start_word[self.TAILLE]}")
        self.mot_ecrit[self.ligne] = input("Quel mot est écrit ?")
        reponse = list(input("Donne la séquence\n"))
        for num in range(len(reponse)):
            reponse[num] = int(reponse[num])
        self.ligne += 1
        self.change_list(reponse)

        while sum(reponse) != 2 * self.TAILLE:
            self.find_best_word()
            print(f"Écris le mot {self.mot_ecrit[self.ligne]}")
            self.mot_ecrit[self.ligne] = input("Quel mot est écrit ?")
            reponse = list(input("Donne la séquence\n"))
            for num in range(len(reponse)):
                reponse[num] = int(reponse[num])
            self.ligne += 1
            self.change_list(reponse)
