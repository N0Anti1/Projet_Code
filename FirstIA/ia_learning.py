import numpy

# Tableau de toutes les entrées (valeurs connu) sous la forme NbEntrée x NbValeurParEntrée
# x_entrer = numpy.array(([3, 1.5], [2, 1], [4, 1.5], [3, 1], [3.5, 0.5], [2, 0.5], [5.5, 1], [1, 1], [2, 1.5]), dtype=float)
x_entrer = numpy.array(([3, 1.5], [2, 1], [4, 1.5], [3, 1], [3.5, 0.5], [2, 0.5], [5.5, 1], [1, 1], [4, 1.5]),
                       dtype=float)

# Tableau de toutes les sorties connus
y = numpy.array(([1, 0, 1, 0, 1, 0, 1, 0]),
                dtype=float)  # 1 == Rouge, 2 == Bleu

# On transforme toutes les valeurs comme nombre compris entre 0 et 1 en divisant par le plus grand nombre
# Ex: On va faire [3/5.5, 1.5/1.5], [2/5.5, 1/1.5], ...
# Car 5.5 et 1.5 sont respectivement les plus grandes valeurs
x_entrer = x_entrer / numpy.amax(x_entrer, axis=0)

# On récupères les 8 premières valeurs (x_entrer - [4, 1.5])
X = numpy.split(x_entrer, [8])[0]
# On récupères la valeur à prédire ([4, 1.5])
xPrediction = numpy.split(x_entrer, [8])[1]


class Neural_Network(object):

    def __init__(self):
        self.inputSize = 2  # Nombre de valeurs par entrée Ex: [3, 1.5] == 2 entrées
        self.outputSize = 1  # Nombre de valeurs de sortie (1)
        self.hiddenSize = 3  # Nombre de neurones caché souhaité

        # Applique un poid sur chaque synapse de l'étape 1 et 2 sous forme de tableau
        self.W1 = numpy.random.randn(self.inputSize, self.hiddenSize)  # Matrice 2x3 (entré x caché)
        self.W2 = numpy.random.randn(self.hiddenSize, self.outputSize)  # Matrice 3x1 (caché x sortie)

    # Fonction qui permet d'avancer --> passer de valeur entré à valeur sortie
    def forward(self, Ventree):
        # Produit matriciel ==> On multiplie pour chaque entrée :
        # [Valeur1, Valeur2], ... et [[poids1, poid2, poid3], [poid4, poid5, poid6]
        # On fait donc z = [V1 * poid1 + V2 * poid4, V1 * poid2 + V2 * poid5, V1 * poid3 + V2 * poid6]
        # On obtient donc un tableau de NbEntrée x NeuronesCachés (8 x 3)
        z = numpy.dot(Ventree, self.W1)
        # Transforme les valeurs obtenue pour les placer dans les neurones cachés
        # Remarque: Numpy permet de faire des calculs directement sur chaque membre de la matrice
        self.z2 = self.sigmoid(z)
        z3 = numpy.dot(self.z2, self.W2)
        output = self.sigmoid(z3)
        return output

    # Transforme un nombre en un autre compris entre 0 et 1
    def sigmoid(self, s):
        return 1 / (1 + numpy.exp(-s))

    # Retourne la dérivée de la fonction sigmoid
    def sigmoidPrime(self, s):
        return s * (1 - s)

    def backward(self, Ventree, Vobjectif, Vobtenue):
        # delta représente l'erreur entre la valeur prévu et la valeur obtenu (Vobjectif et Vsortie)
        output_error = []
        for i in range(len(Vobjectif)):
            output_error.append(Vobjectif[i] - Vobtenue[i])
        o_delta = output_error * self.sigmoidPrime(Vobtenue)

        # Multiplication matricielle entre W2 et l'erreur
        z2_error = o_delta.dot(self.W2.T)
        # Calcul de l'erreur entre les neurones cachés et les valeurs d'entrées
        z2_delta = z2_error * self.sigmoidPrime(self.z2)

        # On recalcule les poids en a partir de l'erreur reconnu
        # == entrée dot erreur delta (si pas dernier, doit la calculer)
        # o_delta.dot(Le_poid_suivant.T) * self.sigmoidPrime(Valeur_arrivée)
        self.W1 += Ventree.T.dot(z2_delta)
        self.W2 += self.z2.T.dot(o_delta)

    def train(self, Tentree, Tsortie):
        o = self.forward(Tentree)
        # print(o)
        self.backward(Tentree, Tsortie, o)

    def predict(self, prediction):
        resultat = self.forward(prediction)
        print("Donnée prédite après entrainement:")
        print(f"Entrée :\n{prediction}")
        print(f"Sortie :\n{resultat}")

        if resultat > 0.5:
            print("La fleur est ROUGE\n")
        else:
            print("La fleur est BLEU\n")


NN = Neural_Network()
for i in range(50000):
    if i % 1000 == 0:
        print(f"# {i}")
    # print(f"Valeurs d'entrées :\n{X}")
    # print(f"Sortie actuelle :\n{y}")
    # print(f"Sortie prédite :\n{numpy.matrix.round(NN.forward(X), 2)}")
    # print("\n")
    NN.train(X, y)

print(f"\n\nValeurs d'entrées :\n{X}")
print(f"Sortie actuelle :\n{y}")
print(f"Sortie prédite :\n{numpy.matrix.round(NN.forward(X), 0)}")
NN.predict(xPrediction)
