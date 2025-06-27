import random
import time
from math import radians
import pygame
from Dodge_It.dodge_it import DodgeIt
from ray import Ray

pygame.init()


class NEAT:

    def __init__(self, screen_size: tuple[int, int], name):
        # constantes
        self.NOM_JEU = "DodgeIt"
        self.TAILLE_FORM_W = 380
        self.TAILLE_FORM_H = 385
        self.screen = pygame.display.set_mode(screen_size)
        self.game = DodgeIt(self.screen)
        self.NAME = name

        self.TAILLE_TILE = 14 / (1280 / screen_size[0])  # taille d'une tile DANS LE JEU
        self.TAILLE_VUE_W = screen_size[0]  # taille de ce que je vois le script
        self.TAILLE_VUE_H = screen_size[1]
        # nombre de tiles scannée par le réseau de neurone en largeur
        self.NB_TILE_W = int(self.TAILLE_VUE_W / self.TAILLE_TILE) + 1
        # nombre de tiles scannée par le réseau de neurone en hauteur
        self.NB_TILE_H = int(self.TAILLE_VUE_H / self.TAILLE_TILE) + 1
        self.NB_INPUT = 4  # nb de neurones input, c'est chaque case du jeu en fait
        self.NB_OUTPUT = 3  # nb de neurones output, c'est à dire les touches de la manette

        self.NB_HIDDEN_PAR_LIGNE = 10  # nombre de neurone hidden par ligne (affichage uniquement)
        self.NB_INPUT_PAR_LIGNE = 20  # nombre de neurone hidden par ligne (affichage uniquement)
        self.TAILLE_INPUT = 15  # en pixel, uniquement pour l'affichage
        self.TAILLE_HIDDEN = 10  # en pixel, uniquement pour l'affichage
        self.TAILLE_OUTPUT_W = 96  # en pixel, uniquement pour l'affichage
        self.TAILLE_OUTPUT_H = 32  # en pixel, uniquement pour l'affichage
        self.ENCRAGE_X_INPUT = 20
        self.ENCRAGE_Y_INPUT = 4 * self.TAILLE_OUTPUT_H
        self.ENCRAGE_X_HIDDEN = self.ENCRAGE_X_INPUT + 20 + self.NB_INPUT_PAR_LIGNE * self.TAILLE_INPUT
        self.ENCRAGE_Y_HIDDEN = 4 * self.TAILLE_OUTPUT_H
        self.ENCRAGE_X_OUTPUT = self.ENCRAGE_X_HIDDEN + 20 + self.NB_HIDDEN_PAR_LIGNE * self.TAILLE_HIDDEN
        self.ENCRAGE_Y_OUTPUT = 4 * self.TAILLE_OUTPUT_H
        self.ESPACE_Y_OUTPUT = self.TAILLE_OUTPUT_H + 5  # entre chaque output l'espace qu'il y a
        self.police = pygame.font.Font('Dodge_It/Anton-Regular.ttf', self.TAILLE_OUTPUT_H)

        self.NB_NEURONE_MAX = 100000  # pour le reseau de neurone, hors input et output
        self.NB_INDIVIDU_POPULATION = 100  # nombre d'individus créés quand création d'une nouvelle population
        self.NB_FRAME_RESET = 600

        # constante pour trier les especes des populations
        self.EXCES_COEF = 0.50
        self.POIDSDIFF_COEF = 0.92
        self.DIFF_LIMITE = 1.00

        # mutation
        self.CHANCE_MUTATION_RESET_CONNEXION = 0.5  # % de chance que le poids de la connexion soit totalement reset
        self.POIDS_CONNEXION_MUTATION_AJOUT = -0.40  # poids ajouté à la mutation de la connexion si pas CHANCE_MUTATION_RESET_CONNEXION. La valeur peut être passée negative
        self.CHANCE_MUTATION_POIDS = 0.60
        self.CHANCE_MUTATION_CONNEXION = 0.1
        self.CHANCE_MUTATION_NEURONE = 0.80

        # doit correspondre aux inputs de la manette dans l'émulateur
        self.lesBoutons = [
            {"nom": "SPACE"},
            {"nom": "RIGHT"},
            {"nom": "LEFT"}
        ]
        self.nbGeneration = 1  # pour suivre on est à la cb de generation
        self.nbInnovation = 0  # nombre d'innovations global pour les connexions, important pour le réseau de neurone
        self.fitnessMax = 0  # fitness max atteinte
        self.lesAnciennesPopulation = []  # stock les anciennes populations
        self.lesEspeces = []
        self.laPopulation = []
        self.idPopulation = 0  # quel id de la population est en train de passer dans la boucle
        self.points_base = 0  # points de la partie
        self.nbFrame = 0  # nb de frame actuellement
        self.nbFrameStop = 0  # permettra de reset le jeu au besoin
        self.fitnessInit = 0  # fitness à partir de laquelle le réseau actuel commence est init
        self.anc_fitness_max = 0

    # créé un neurone
    def newNeurone(self):
        neurone = {
            "valeur": 0,
            "id": 0,
            "type": ""
        }
        return neurone

    # ajoute un neurone a un reseau de neurone, fait que pour les neurones qui doivent exister
    def ajouterNeurone(self, unReseau: dict, id, type, valeur):
        neurone = self.newNeurone()
        neurone["valeur"] = valeur
        neurone["id"] = id
        neurone["type"] = type
        unReseau["lesNeurones"][id] = neurone

    # créé un reseau de neurone
    def newReseau(self):
        reseau = {"nbNeurone": 0,  # taille des neurones rajouté par l'algo (hors input output du coup)
                  "fitness": 1,  # beaucoup de division, pour eviter de faire l'irreparable
                  "idEspeceParent": 0,
                  "lesNeurones": {},
                  "lesConnexions": {}}

        # On ajoute les inputs
        for j in range(self.NB_INPUT):
            self.ajouterNeurone(reseau, j, "input", 1)

        # ensuite, les outputs
        for j in range(self.NB_INPUT, self.NB_INPUT + self.NB_OUTPUT):
            self.ajouterNeurone(reseau, j, "output", 0)

        return reseau

    # créé une population
    def newPopulation(self):
        population = []
        for i in range(self.NB_INDIVIDU_POPULATION):
            population.append(self.newReseau().copy())
        return population

    # créé une connexion
    def newConnexion(self):
        connexion = {
            "entree": 0,
            "sortie": 0,
            "actif": True,
            "poids": 0,
            "innovation": 0,
            "allume": False  # pour le dessin, si true ça veut dire que le resultat de la connexion est different de 0
        }
        return connexion

    # créé une espece (un regroupement de reseaux, d'individus)
    def newEspece(self):
        espece = {"nbEnfant": 0,  # combien d'enfant cette espece a créé
                  "fitnessMoyenne": 0,  # fitness moyenne de l'espece
                  "fitnessMax": 0,  # fitness max atteinte par l'espece
                  "lesReseaux": []}  # tableau qui regroupe les reseaux
        return espece

    # genere un poids aléatoire (pour les connexions) egal à 1 ou -1
    def genererPoids(self):
        var = 1
        if random.random() >= 0.5:
            var = -1
        return var

    # ajoute une connexion a un reseau de neurone
    def ajouterConnexion(self, unReseau, entree, sortie):
        connexion = self.newConnexion()
        connexion["actif"] = True
        connexion["entree"] = entree
        connexion["sortie"] = sortie
        connexion["poids"] = self.genererPoids()
        connexion["innovation"] = self.nbInnovation
        unReseau["lesConnexions"][self.nbInnovation] = connexion
        self.nbInnovation += 1

    # modifie les connexions d'un reseau de neurone
    def mutationPoidsConnexions(self, unReseau):
        for i in range(len(unReseau["lesConnexions"])):
            if unReseau["lesConnexions"][i]["actif"]:
                if random.random() < self.CHANCE_MUTATION_RESET_CONNEXION:
                    unReseau["lesConnexions"][i]["poids"] = self.genererPoids()
                else:
                    if random.random() >= 0.5:
                        unReseau["lesConnexions"][i]["poids"] = unReseau["lesConnexions"][i][
                                                                    "poids"] - self.POIDS_CONNEXION_MUTATION_AJOUT
                    else:
                        unReseau["lesConnexions"][i]["poids"] = unReseau["lesConnexions"][i][
                                                                    "poids"] + self.POIDS_CONNEXION_MUTATION_AJOUT

    def mutationAjouterConnexion(self, unReseau):
        liste = []

        # randomisation + copies des neuronnes dans une liste
        for i in unReseau["lesNeurones"]:
            pos = random.randint(0, len(liste))
            liste.insert(pos, unReseau["lesNeurones"][i])

        # la je vais lister tous les neurones et voir si une paire n'a pas de connexion
        # si une connexion peut être créée on la crée et on stop
        traitement = False
        for i in range(len(liste)):
            for j in range(len(liste)):
                if i != j:
                    neurone1 = liste[i]
                    neurone2 = liste[j]

                    if (neurone1["type"] == "input" and neurone2["type"] == "output") or (
                            neurone1["type"] == "hidden" and neurone2["type"] == "hidden") or (
                            neurone1["type"] == "hidden" and neurone2["type"] == "output"):
                        # si on en est là, c'est que la connexion peut se faire, juste à tester si y pas deja une connexion
                        dejaConnexion = False
                        for k in range(len(unReseau["lesConnexions"])):
                            if unReseau["lesConnexions"][k]["entree"] == neurone1["id"] and \
                                    unReseau["lesConnexions"][k]["sortie"] == neurone2["id"]:
                                dejaConnexion = True
                                break
                        if not dejaConnexion:
                            # nouvelle connexion, traitement terminé
                            traitement = True
                            self.ajouterConnexion(unReseau, neurone1["id"], neurone2["id"])

                if traitement:
                    break
            if traitement:
                break

        if not traitement:
            print("impossible de recreer une connexion")

    def mutationAjouterNeurone(self, unReseau):
        if len(unReseau["lesConnexions"]) == 0:
            print("Impossible d'ajouter un neurone entre 2 connexions si pas de connexion")
            return None

        if unReseau["nbNeurone"] == self.NB_NEURONE_MAX:
            print("Nombre de neurone max atteint")
            return None

        # randomisation de la liste des connexions
        listeIndice = []
        listeRandom = []

        # je créé une liste d'entier de 1 à la taille des connexions
        for i in range(len(unReseau["lesConnexions"])):
            listeIndice.append(i)

        # je randomise la liste que je viens de créer dans listeRandom
        for i in listeIndice:
            pos = random.randint(0, len(listeRandom))
            listeRandom.insert(pos, listeIndice[i])

        for i in range(len(listeRandom)):
            if unReseau["lesConnexions"][listeRandom[i]]["actif"]:
                unReseau["lesConnexions"][listeRandom[i]]["actif"] = False
                indice = unReseau["nbNeurone"] + self.NB_INPUT + self.NB_OUTPUT
                self.ajouterNeurone(unReseau, indice, "hidden", 1)
                self.ajouterConnexion(unReseau, unReseau["lesConnexions"][listeRandom[i]]["entree"], indice)
                self.ajouterConnexion(unReseau, indice, unReseau["lesConnexions"][listeRandom[i]]["sortie"])
                unReseau["nbNeurone"] = unReseau["nbNeurone"] + 1
                break

    def mutation(self, unReseau):
        rand = random.random()
        if rand < self.CHANCE_MUTATION_POIDS:
            self.mutationPoidsConnexions(unReseau)
        if rand < self.CHANCE_MUTATION_CONNEXION:
            self.mutationAjouterConnexion(unReseau)
        if rand < self.CHANCE_MUTATION_NEURONE:
            self.mutationAjouterNeurone(unReseau)

    def getDisjoint(self, unReseau1, unReseau2):
        nbPareil = 0
        for i in range(len(unReseau1["lesConnexions"])):
            for j in range(len(unReseau2["lesConnexions"])):
                if unReseau1["lesConnexions"][i]["innovation"] == unReseau2["lesConnexions"][j]["innovation"]:
                    nbPareil += 1

        # oui ça marche
        return len(unReseau1["lesConnexions"]) + len(unReseau2["lesConnexions"]) - 2 * nbPareil

    def getDiffPoids(self, unReseau1, unReseau2):
        nbConnexion = 0
        total = 0
        for i in range(len(unReseau1["lesConnexions"])):
            for j in range(len(unReseau2["lesConnexions"])):
                if unReseau1["lesConnexions"][i]["innovation"] == unReseau2["lesConnexions"][j]["innovation"]:
                    nbConnexion += 1
                    total += abs(unReseau1["lesConnexions"][i]["poids"] - unReseau2["lesConnexions"][j]["poids"])

        # si aucune connexion en commun c'est qu'ils sont trop differents
        # puis si on laisse comme ça on va diviser par 0 et on va lancer mario maker
        if nbConnexion == 0:
            return 100000

        return total / nbConnexion

    def getScore(self, unReseauTest, unReseauRep):
        return (self.EXCES_COEF * self.getDisjoint(unReseauTest, unReseauRep)) / max(
            len(unReseauTest["lesConnexions"]) + len(unReseauRep["lesConnexions"]),
            1) + self.POIDSDIFF_COEF * self.getDiffPoids(unReseauTest, unReseauRep)

    def trierPopulation(self, laPopulation):
        self.lesEspeces = []
        self.lesEspeces.append(self.newEspece())

        # la premiere espèce créée et le dernier element de la premiere population
        # comme ça, j'ai déjà une première espèce créée
        self.lesEspeces[0]["lesReseaux"].append(laPopulation[-1].copy())

        for i in range(len(laPopulation) - 1):
            trouve = False
            for j in range(len(self.lesEspeces)):
                indice = random.randint(0, len(self.lesEspeces[j]["lesReseaux"]) - 1)
                rep = self.lesEspeces[j]["lesReseaux"][indice]
                # il peut être classé
                if self.getScore(laPopulation[i], rep) < self.DIFF_LIMITE:
                    self.lesEspeces[j]["lesReseaux"].append(laPopulation[i].copy())
                    trouve = True
                    break

            # si pas trouvé, il faut créer une espèce pour l'individu
            if not trouve:
                self.lesEspeces.append(self.newEspece())
                self.lesEspeces[-1]["lesReseaux"].append(laPopulation[i].copy())

        return self.lesEspeces

    def get_fitness(self, espece: dict):
        return espece.get("fitness")

    def choisirParent(self, uneEspece):
        if len(uneEspece) == 0:
            print("uneEspece vide dans choisir parent ??")
        # il est possible que l'espece ne contienne qu'un seul reseau, dans ce cas là on va pas plus loin
        if len(uneEspece) == 1:
            return uneEspece[0]

        fitnessTotal = 0
        for i in range(len(uneEspece)):
            fitnessTotal += uneEspece[i]["fitness"]

        limite = random.randint(0, fitnessTotal)
        total = 0
        for i in range(len(uneEspece)):
            total += uneEspece[i]["fitness"]
            # si la somme des fitness cumulés depasse total, on renvoie l'espece qui a fait depasser la limite
            if total >= limite:
                return uneEspece[i].copy()

        print("impossible de trouver un parent ?")
        return None

    def crossover(self, unReseau1, unReseau2):
        # quel est le meilleur des deux ?
        leBon = unReseau1
        leNul = unReseau2
        if leBon["fitness"] < leNul["fitness"]:
            leBon = unReseau2
            leNul = unReseau1

        # le nouveau réseau va hériter de la majorité des attributs du meilleur
        leReseau = leBon.copy()

        # sauf pour les connexions où y a une chance que le nul lui donne ses genes
        for i in range(len(leReseau["lesConnexions"])):
            for j in range(len(leNul["lesConnexions"])):
                # si 2 connexions partagent la meme innovation, la connexion du nul peut venir la remplacer
                if leReseau["lesConnexions"][i]["innovation"] == leNul["lesConnexions"][j]["innovation"]:
                    if random.random() > 0.5:
                        leReseau["lesConnexions"][i] = leNul["lesConnexions"][j]

        leReseau["fitness"] = 1
        return leReseau

    def nouvelleGeneration(self, laPopulation, lesEspeces):
        laNouvellePopulation = self.newPopulation()
        # nombre d'indivu à creer au total
        nbIndividuACreer = self.NB_INDIVIDU_POPULATION
        # indice qui va servir à savoir OU en est le tab de la nouvelle espece
        indiceNouvelleEspece = 0

        # il est possible que l'ancien meilleur ait un meilleur fitness
        # que celui de la nouvelle population (une mauvaise mutation ça arrive très souvent)
        # dans ce cas je le supprime par l'ancien meilleur histoire d'être SUR d'avoir des enfants
        # toujours du plus bon
        fitnessMaxPop = 0
        fitnessMaxAncPop = 0
        ancienPlusFort = []
        for i in range(len(laPopulation)):
            if fitnessMaxPop < laPopulation[i]["fitness"]:
                fitnessMaxPop = laPopulation[i]["fitness"]

        # on test que s'il y a deja une ancienne population evidemment
        if len(self.lesAnciennesPopulation) > 0:
            # je vais checker TOUTES les anciennes population pour la fitness la plus élevée
            # vu que les reseaux vont REmuter, il est possible qu'ils fassent moins bon !
            for i in range(len(self.lesAnciennesPopulation)):
                for j in range(len(self.lesAnciennesPopulation[i])):
                    if fitnessMaxAncPop < self.lesAnciennesPopulation[i][j]["fitness"]:
                        fitnessMaxAncPop = self.lesAnciennesPopulation[i][j]["fitness"]
                        ancienPlusFort = self.lesAnciennesPopulation[i][j].copy()

        if fitnessMaxAncPop > fitnessMaxPop:
            # comme ça je suis sur que le meilleur dominera totalement
            for i in range(len(lesEspeces)):
                for j in range(len(lesEspeces[i]["lesReseaux"])):
                    lesEspeces[i]["lesReseaux"][j] = ancienPlusFort.copy()

            print("mauvaise population je reprends la meilleur et ça redevient la base de la nouvelle pop")

        self.lesAnciennesPopulation.append(laPopulation.copy())

        # calcul fitness pour chaque espece
        nbIndividuTotal = 0
        fitnessMoyenneGlobal = 0  # fitness moyenne de TOUS les individus de toutes les especes
        leMeilleur = self.newReseau()  # je dois le remettre avant tout, on va essayer de trouver ou il est
        for i in range(len(lesEspeces)):
            lesEspeces[i]["fitnessMoyenne"] = 0
            lesEspeces[i]["fitnessMax"] = 0
            for j in range(len(lesEspeces[i]["lesReseaux"])):
                lesEspeces[i]["fitnessMoyenne"] = lesEspeces[i]["fitnessMoyenne"] + lesEspeces[i]["lesReseaux"][j][
                    "fitness"]
                fitnessMoyenneGlobal += lesEspeces[i]["lesReseaux"][j]["fitness"]
                nbIndividuTotal += 1

                if lesEspeces[i]["fitnessMax"] < lesEspeces[i]["lesReseaux"][j]["fitness"]:
                    lesEspeces[i]["fitnessMax"] = lesEspeces[i]["lesReseaux"][j]["fitness"]
                    if leMeilleur["fitness"] < lesEspeces[i]["lesReseaux"][j]["fitness"]:
                        leMeilleur = lesEspeces[i]["lesReseaux"][j].copy()

            lesEspeces[i]["fitnessMoyenne"] = lesEspeces[i]["fitnessMoyenne"] / len(lesEspeces[i]["lesReseaux"])

        fitnessMoyenneGlobal /= nbIndividuTotal

        # tri des especes pour que les meilleurs place leurs enfants avant tout
        lesEspeces.sort(key=self.get_fitness, reverse=True)

        # chaque espece va créer un certain nombre d'individu dans la nouvelle population en fonction de si l'espece a un bon fitness ou pas
        for i in range(len(lesEspeces)):
            nbIndividuEspece = round(
                len(lesEspeces[i]["lesReseaux"]) * lesEspeces[i]["fitnessMoyenne"] / fitnessMoyenneGlobal)
            nbIndividuACreer -= nbIndividuEspece
            if nbIndividuACreer < 0:
                nbIndividuEspece += nbIndividuACreer
                nbIndividuACreer = 0
            lesEspeces[i]["nbEnfant"] = nbIndividuEspece

            for j in range(nbIndividuEspece):
                if indiceNouvelleEspece > self.NB_INDIVIDU_POPULATION:
                    break

                unReseau = self.crossover(self.choisirParent(lesEspeces[i]["lesReseaux"]),
                                          self.choisirParent(lesEspeces[i]["lesReseaux"]))

                # on stop la mutation à ce stade
                self.mutation(unReseau.copy())

                unReseau["idEspeceParent"] = i
                laNouvellePopulation[indiceNouvelleEspece] = unReseau.copy()
                laNouvellePopulation[indiceNouvelleEspece]["fitness"] = 1
                indiceNouvelleEspece += 1

            if indiceNouvelleEspece > self.NB_INDIVIDU_POPULATION:
                break

        # si une espece n'a pas fait d'enfant, je la delete
        for i in range(len(lesEspeces)):
            if lesEspeces[i]["nbEnfant"] == 0:
                lesEspeces[i] = None
        return laNouvellePopulation

    def getIndiceLesInputs(self, x, y):
        return x + (y * self.NB_TILE_W)

    def getLesSprites(self):
        lesSprites = {}
        j = 0
        for i in range(len(self.game.death_point)):
            lesSprites[j] = {"x": self.game.death_point[i][0], "y": self.game.death_point[i][1]}
            j += 1

        return lesSprites

    def getLesInputs(self):
        lesInputs = []
        balle = self.game.ball
        radius = self.game.point_radius
        new_line = [[[(mur[0] - radius, mur[1]), (mur[0] + radius, mur[1])],
                     [(mur[0], mur[1] - radius), (mur[0], mur[1] + radius)]] for mur in self.game.death_point]
        objectif = self.game.apple
        wall = []
        for line in new_line:
            wall.append(line[0])
            wall.append(line[1])
        wall.append([(objectif[0] - radius, objectif[1]), (objectif[0] + radius, objectif[1])])
        wall.append([(objectif[0], objectif[1] - radius), (objectif[0], objectif[1] + radius)])
        for i in range(self.NB_INPUT):
            ray = Ray(self.screen, balle, radians(i * 360 / self.NB_INPUT), wall)
            lesInputs.append(ray.endPoint())

        """lesInputs = {}
        for i in range(self.NB_TILE_W):
            for j in range(self.NB_TILE_H):
                lesInputs[self.getIndiceLesInputs(i, j)] = 0

        lesSprites = self.getLesSprites()
        for i in range(len(lesSprites)):
            lesInputs[self.getIndiceLesInputs(int(lesSprites[i]["x"] / self.TAILLE_TILE),
                                              int(lesSprites[i]["y"] / self.TAILLE_TILE))] = -1

        lesInputs[self.getIndiceLesInputs(int(self.game.apple[0] / self.TAILLE_TILE),
                                          int(self.game.apple[1] / self.TAILLE_TILE))] = 1"""

        return lesInputs

    def sigmoid(self, x):
        resultat = x / (1 + abs(x))
        if resultat >= 0.5:
            return True
        return False

    def dessinerUnReseau(self, unReseau):
        # je commence par les inputs
        lesInputs = self.getLesInputs()
        lesPositions = {}  # va retenir toutes les positions des neurones affichées, ça sera plus facile pour les connexions

        for i in range(self.NB_INPUT):

                xT = self.ENCRAGE_X_INPUT + (self.TAILLE_INPUT + 1) * (i % self.NB_INPUT_PAR_LIGNE)
                yT = self.ENCRAGE_Y_INPUT + (self.TAILLE_INPUT + 1) * int(i / self.NB_INPUT_PAR_LIGNE)

                couleurFond = "white"
                if lesInputs[i] < 0:
                    couleurFond = ((lesInputs[i] + 1) * 255, (lesInputs[i] + 1) * 255, (lesInputs[i] + 1) * 255)
                elif lesInputs[i] > 0:
                    couleurFond = ((lesInputs[i] + 1) * 100, (lesInputs[i] + 1) * 100, 255)

                pygame.draw.rect(self.screen, couleurFond, (xT, yT, self.TAILLE_INPUT, self.TAILLE_INPUT))

                lesPositions[i] = {
                    "x": xT + self.TAILLE_INPUT / 2,
                    "y": yT + self.TAILLE_INPUT / 2
                }

        for i in range(self.NB_OUTPUT):
            xT = self.ENCRAGE_X_OUTPUT
            yT = self.ENCRAGE_Y_OUTPUT + self.ESPACE_Y_OUTPUT * i
            nomT = self.police.render(self.lesBoutons[i]["nom"], True, 0)
            indice = i + self.NB_INPUT

            if self.sigmoid(unReseau["lesNeurones"][indice]["valeur"]):
                pygame.draw.rect(self.screen, (255, 255, 255), (xT, yT, self.TAILLE_OUTPUT_W, self.TAILLE_OUTPUT_H))
            else:
                pygame.draw.rect(self.screen, 0, (xT, yT, self.TAILLE_OUTPUT_W, self.TAILLE_OUTPUT_H))
            self.screen.blit(nomT, (xT + self.TAILLE_OUTPUT_W, yT))

            lesPositions[indice] = {
                "x": xT + self.TAILLE_OUTPUT_W / 2,
                "y": yT + self.TAILLE_OUTPUT_H / 2
            }

        for i in range(unReseau["nbNeurone"]):
            xT = self.ENCRAGE_X_HIDDEN + (self.TAILLE_HIDDEN + 1) * (i % self.NB_HIDDEN_PAR_LIGNE)
            yT = self.ENCRAGE_Y_HIDDEN + (self.TAILLE_HIDDEN + 1) * int(i / self.NB_HIDDEN_PAR_LIGNE)
            # tous les 10 j'affiche le restant des neurones en dessous

            indice = i + self.NB_INPUT + self.NB_OUTPUT
            pygame.draw.rect(self.screen, 0, (xT, yT, self.TAILLE_HIDDEN, self.TAILLE_HIDDEN), 2)

            lesPositions[indice] = {
                "x": xT + self.TAILLE_HIDDEN / 2,
                "y": yT + self.TAILLE_HIDDEN / 2
            }

        # affichage des connexions
        for i in range(len(unReseau["lesConnexions"])):
            if unReseau["lesConnexions"][i]["actif"] and i % 10 == 0:
                pixel = 0
                alpha = 255
                if unReseau["lesConnexions"][i]["poids"] > 0:
                    pixel = 255
                if not unReseau["lesConnexions"][i]["allume"]:
                    alpha = 25

                couleur = (pixel, pixel, pixel, alpha)

                try:
                    pygame.draw.line(self.screen, couleur, (lesPositions[unReseau["lesConnexions"][i]["entree"]]["x"],
                                                            lesPositions[unReseau["lesConnexions"][i]["entree"]]["y"]),
                                     (lesPositions[unReseau["lesConnexions"][i]["sortie"]]["x"],
                                      lesPositions[unReseau["lesConnexions"][i]["sortie"]]["y"]))
                except KeyError:
                    pass

    def dessinerLesInfos(self):
        message = self.police.render(
            f"Géneration : {self.nbGeneration}    Ind : {self.idPopulation + 1}    Nb Espèce : {len(self.lesEspeces)}    ",
            True, 0)
        message3 = self.police.render(f"Nb Neurones Cachés : {self.laPopulation[self.idPopulation]['nbNeurone']}", True,
                                      0)
        message2 = self.police.render(
            f"Fitness : {self.laPopulation[self.idPopulation]['fitness']}    (max = {self.fitnessMax})    ", True, 0)
        message4 = self.police.render(f"Nb Connexions : {len(self.laPopulation[self.idPopulation]['lesConnexions'])}",
                                      True, 0)
        pygame.draw.rect(self.screen, (230, 220, 210),
                         (0, 0, self.screen.get_width(), 10 + message.get_height() + message2.get_height()))

        self.screen.blit(message, (10, 10))
        self.screen.blit(message2, (10, 10 + message.get_height()))
        self.screen.blit(message3, (10 + message.get_width(), 10))
        self.screen.blit(message4, (10 + message.get_width(), 10 + message3.get_height()))

    def majReseau(self, unReseau):
        # mise à jour des inputs
        lesInputs = self.getLesInputs()
        for i in range(self.NB_INPUT):
            unReseau["lesNeurones"][i]["valeur"] = lesInputs[i]

    def feedForward(self, unReseau):
        # avant de continuer, je reset à 0 les neurones de sortie
        for i in range(len(unReseau["lesConnexions"])):
            if unReseau["lesConnexions"][i]["actif"]:
                unReseau["lesNeurones"][unReseau["lesConnexions"][i]["sortie"]]["valeur"] = 0
                unReseau["lesNeurones"][unReseau["lesConnexions"][i]["sortie"]]["allume"] = False

                """for i in range(len(unReseau["lesConnexions"])):
                    if unReseau["lesConnexions"][i]["actif"]:"""
                # avantTraitement = unReseau["lesNeurones"][unReseau["lesConnexions"][i]["sortie"]]["valeur"]
                unReseau["lesNeurones"][unReseau["lesConnexions"][i]["sortie"]]["valeur"] = unReseau["lesNeurones"][unReseau["lesConnexions"][i]["entree"]]["valeur"] * unReseau["lesConnexions"][i]["poids"]

                # on ""allume"" le lien si la connexion a fait une modif
                if unReseau["lesNeurones"][unReseau["lesConnexions"][i]["sortie"]]["valeur"] != 0:
                    unReseau["lesConnexions"][i]["allume"] = True
                else:
                    unReseau["lesConnexions"][i]["allume"] = False

    def sauvegarderUnReseau(self, unReseau, file):
        file.write(f"{unReseau['nbNeurone']}\n")
        file.write(f"{unReseau['fitness']}\n")
        file.write(f"{unReseau['idEspeceParent']}\n")

        for i in range((unReseau['nbNeurone'])):
            indice = self.NB_INPUT + self.NB_OUTPUT + i
            # pas besoin d'écrire le type, je ne sauvegarde que les hiddens
            file.write(f"{unReseau['lesNeurones'][indice]['id']}|")
            file.write(f"{unReseau['lesNeurones'][indice]['valeur']}\n")

        file.write(f"{len(unReseau['lesConnexions'])}\n")
        for i in range(len(unReseau['lesConnexions'])):
            actif = 0
            if unReseau["lesConnexions"][i]["actif"]:
                actif = 1
            file.write(f"{unReseau['lesConnexions'][i]['entree']}|")
            file.write(f"{unReseau['lesConnexions'][i]['sortie']}|")
            file.write(f"{actif}|")
            file.write(f"{unReseau['lesConnexions'][i]['poids']}|")
            file.write(f"{unReseau['lesConnexions'][i]['innovation']}\n")

    def sauvegarderPopulation(self, best, first=False):
        chemin_time = time.localtime()
        day = f"{chemin_time.tm_mday}" if len(f"{chemin_time.tm_mday}") == 2 else f"0{chemin_time.tm_mday}"
        mon = f"{chemin_time.tm_mon}" if len(f"{chemin_time.tm_mon}") == 2 else f"0{chemin_time.tm_mon}"
        hour = f"{chemin_time.tm_hour}" if len(f"{chemin_time.tm_hour}") == 2 else f"0{chemin_time.tm_hour}"
        min = f"{chemin_time.tm_min}" if len(f"{chemin_time.tm_min}") == 2 else f"0{chemin_time.tm_min}"
        sec = f"{chemin_time.tm_sec}" if len(f"{chemin_time.tm_sec}") == 2 else f"0{chemin_time.tm_sec}"
        end = 'B' if best else 'F' if first else ''
        path = f"{self.NAME}_{day}{mon}{chemin_time.tm_year}-{hour}{min}{sec}_{self.nbGeneration}{end}.txt"
        file = open(f"save_gen/{path}", "w+")

        # sauvegarde classique de la population
        file.write(f"{self.nbGeneration}\n")
        file.write(f"{self.nbInnovation}\n")
        file.write(f"{self.fitnessMax}\n")

        for i in range(len(self.laPopulation)):
            self.sauvegarderUnReseau(self.laPopulation[i], file)

        # et là je sauvegarde le plus fort, c'est important pour pas perdre les progrès
        lePlusFort = self.newReseau()
        for i in range(len(self.laPopulation)):
            if lePlusFort["fitness"] < self.laPopulation[i]["fitness"]:
                lePlusFort = self.laPopulation[i].copy()

        # check aussi dans l'ancienne population (si plus fort, il ne peut être que là)
        if len(self.lesAnciennesPopulation) > 0:
            for i in range(len(self.lesAnciennesPopulation)):
                for j in range(len(self.lesAnciennesPopulation[i])):
                    if i == 1:
                        self.sauvegarderUnReseau(self.lesAnciennesPopulation[i][j], file)
                    if lePlusFort["fitness"] < self.lesAnciennesPopulation[i][j]["fitness"]:
                        lePlusFort = self.lesAnciennesPopulation[i][j].copy()

        self.sauvegarderUnReseau(lePlusFort, file)
        if not first:
            file.write("fini")
        else:
            file.write("first")
        file.close()
        return f"{path}"

    def ChargerReseau(self, save, count_line, population):
        for i in range(self.NB_INDIVIDU_POPULATION):
            reseau = self.newReseau()
            reseau["nbNeurone"] = int(save[i * 4 + 3 + count_line])
            reseau["fitness"] = int(save[i * 4 + 4 + count_line])
            reseau["idEspeceParent"] = int(save[i * 4 + 5 + count_line])

            if int(save[i * 4 + 3 + count_line]) > 0:
                for j in range(int(save[i * 4 + 3 + count_line])):
                    neurone = self.newNeurone()
                    tab = save[i * 4 + 6 + count_line + j].split("|")
                    neurone["id"] = int(tab[0])
                    neurone["valeur"] = float(tab[1])
                    neurone["type"] = "hidden"
                    reseau["lesNeurones"][self.NB_INPUT + self.NB_OUTPUT + j] = neurone
            count_line += int(save[i * 4 + 3 + count_line])

            if int(save[i * 4 + 6 + count_line]) > 0:
                for j in range(int(save[i * 4 + 6 + count_line])):
                    connection = self.newConnexion()
                    tab = save[i * 4 + j + 7 + count_line].split("|")
                    connection["entree"] = int(tab[0])
                    connection["sortie"] = int(tab[1])
                    connection["actif"] = True if tab[2] == "1" else False
                    connection["poids"] = float(tab[3])
                    connection["innovation"] = int(tab[4])
                    reseau["lesConnexions"][j] = connection
            count_line += int(save[i * 4 + 6 + count_line])
            population.append(reseau.copy())
        count_line += self.NB_INDIVIDU_POPULATION * 4
        return count_line

    def ChargerPopulation(self, path):
        file = open(f"save_gen/{path}", "r")

        save = []
        for ligne in file.readlines():
            save.append(ligne.strip("\n"))

        first_save = False
        if save[-1] == "first":
            first_save = True
        elif save[-1] != "fini":
            print("Sauvegarde Corrompu")
        self.nbGeneration = int(save[0])
        self.nbInnovation = int(save[1])
        self.fitnessMax = int(save[2])
        self.laPopulation = []

        count_line = 0
        count_line = self.ChargerReseau(save, count_line, self.laPopulation)

        if not first_save:
            self.lesAnciennesPopulation = [[]]
            count_line = self.ChargerReseau(save, count_line, self.lesAnciennesPopulation[0])

        reseau = self.newReseau()
        reseau["nbNeurone"] = int(save[3 + count_line])
        reseau["fitness"] = int(save[4 + count_line])
        reseau["idEspeceParent"] = int(save[5 + count_line])

        if int(save[3 + count_line]) > 0:
            for j in range(int(save[3 + count_line])):
                neurone = self.newNeurone()
                tab = save[6 + count_line].split("|")
                neurone["id"] = int(tab[0])
                neurone["valeur"] = float(tab[1])
                neurone["type"] = "hidden"
                reseau["lesNeurones"][self.NB_INPUT + self.NB_OUTPUT + j] = neurone
        count_line += int(save[3 + count_line])

        for j in range(int(save[6 + count_line])):
            connection = self.newConnexion()
            tab = save[j + 7 + count_line].split("|")
            connection["entree"] = int(tab[0])
            connection["sortie"] = int(tab[1])
            connection["actif"] = True if tab[2] == "1" else False
            connection["poids"] = float(tab[3])
            connection["innovation"] = int(tab[4])
            reseau["lesConnexions"][j] = connection
        self.laPopulation[0] = reseau.copy()
        file.close()

    def copier(self, orig):
        orig_type = type(orig)
        if orig_type == list:
            copy = []
            for orig_key, orig_value in orig:
                copy[self.copier(orig_key)] = self.copier(orig_value)
        elif orig_type == dict:
            copy = {}
            for orig_key, orig_value in orig.items():
                copy[self.copier(orig_key)] = self.copier(orig_value)
        else:  # number, string, boolean, etc
            copy = orig
        return copy

    def appliquerLesBoutons(self, unReseau):
        lesBoutonsT = {}
        for i in range(self.NB_OUTPUT):
            lesBoutonsT[self.lesBoutons[i]["nom"]] = self.sigmoid(unReseau["lesNeurones"][self.NB_INPUT + i]["valeur"])

        for touche in lesBoutonsT:
            if lesBoutonsT[touche]:
                if touche == "SPACE":
                    self.game.fall -= 3 / (1280 / self.game.screen.get_width())
                if touche == "LEFT":
                    self.game.speed -= .3 / (1280 / self.screen.get_width())
                if touche == "RIGHT":
                    self.game.speed += .3 / (1280 / self.screen.get_width())

    def reset(self):
        self.game.lose = False
        self.points_base = 0
        self.lancerNiveau()
        self.idPopulation += 1
        save = False
        # si on en est là, on va refaire une generation
        if self.idPopulation >= len(self.laPopulation):
            for i in range(len(self.laPopulation)):
                if self.laPopulation[i]["fitness"] >= self.anc_fitness_max:
                    self.anc_fitness_max = self.laPopulation[i]["fitness"]
                    save = True

            print("Sauvegarde de l'espèce...")
            name_save = self.sauvegarderPopulation(save, True if self.nbGeneration == 1 else False)
            print(f"Sauvegarde fini sous le nom : {name_save}")

            self.idPopulation = 0
            self.nbGeneration += 1
            self.lesEspeces = self.trierPopulation(self.laPopulation)
            self.laPopulation = self.nouvelleGeneration(self.laPopulation, self.lesEspeces)
            print(f"Initialisation de la fitness...")
            for pop in self.laPopulation:
                pop["fitness"] = 0
            print(f"Début de l'expérience {self.nbGeneration}")

    def lancerNiveau(self):
        self.game.reset()

    def run(self, path_load=None):

        estAccelere = False
        estAfficheReseau = True
        estAfficheInfo = True

        print("lancement du script")

        self.lancerNiveau()

        if type(path_load) == str:
            self.ChargerPopulation(path_load)
        else:
            self.laPopulation = self.newPopulation()

            self.mutation(self.laPopulation[0])

            for i in range(1, len(self.laPopulation)):
                # self.laPopulation[i] = self.laPopulation[0].copy()
                self.mutation(self.laPopulation[i])

            print("mutation terminé")
            self.lesEspeces = self.trierPopulation(self.laPopulation)
            self.laPopulation = self.nouvelleGeneration(self.laPopulation, self.lesEspeces)
            print(f"Initialisation de la fitness...")
            for pop in self.laPopulation:
                pop["fitness"] = 0
            print("Début de l'expérience 1")
            self.sauvegarderPopulation(False, True)

        clock = pygame.time.Clock()
        while self.game.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.fall -= 3 / (1280 / self.game.screen.get_width())

            self.game.update()

            self.majReseau(self.laPopulation[self.idPopulation])
            self.feedForward(self.laPopulation[self.idPopulation])
            self.appliquerLesBoutons(self.laPopulation[self.idPopulation])

            if estAfficheReseau:
                self.dessinerUnReseau(self.laPopulation[self.idPopulation])
            if estAfficheInfo:
                self.dessinerLesInfos()

            if self.laPopulation[self.idPopulation]["fitness"] - self.game.point * self.NB_FRAME_RESET > self.NB_FRAME_RESET:
                self.reset()
            elif self.game.lose:
                self.reset()
            else:
                self.laPopulation[self.idPopulation]["fitness"] += 1
                """if self.game.point > self.points_base:
                    self.laPopulation[self.idPopulation]["fitness"] = self.NB_FRAME_RESET * self.game.point
                    self.points_base = self.game.point"""
                if self.fitnessMax < self.laPopulation[self.idPopulation]["fitness"]:
                    self.fitnessMax = self.laPopulation[self.idPopulation]["fitness"]

            if not estAccelere:
                clock.tick(60)
            pygame.display.flip()


neat = NEAT((1280, 720), "BEST")
neat.run()
