import numpy as np
import matplotlib.pyplot as plt
import random as rd
from math import sqrt, pi, exp

####################################################################
## Lecture et affichage de l'image
####################################################################

image_a_traiter = 'images/mario.png'


# La fonction lit l'image et retourne les information pixel par pixel dans un tableau (image)
def read_picture(photo):
    image = np.array(plt.imread(photo))
    picture = [[(0, 0, 0) for _ in range(len(image[0]))] for _ in range(len(image))]
    # picture est un tablau avec 3 dimentions :
    # [Hauteur photo], [Largeur photo] et l'information [R, G, B, "a"] du pixel
    for y in range(len(image)):
        for x in range(len(image[y])):
            r = float(image[y][x][0])
            g = float(image[y][x][1])
            b = float(image[y][x][2])
            if r > 1 or g > 1 or b > 1:  # On transforme le tableau avec des valeurs RGB entre 0 et 1 (sans alpha)
                r = r / 255
                g = g / 255
                b = b / 255
            picture[y][x] = (r, g, b)
    return picture


read_image = read_picture(image_a_traiter)

print("Affichage de l'image...")
plt.figure(1)
image = plt.imshow(read_image)
image.axes.get_xaxis().set_visible(False)
image.axes.get_yaxis().set_visible(False)
plt.show()



####################################################################
## Résolution et échantillonage
####################################################################


# Cette fonction récupère la couleur de 1 pixel tout les 'résolution' pixel et retourne l'image pixélisé
def echantillonage(photo, resolution):
    hauteur = int(len(photo) / resolution)
    largeur = int(len(photo[0]) / resolution)
    # new_image est un tableau avec 3 dimentions : [la hauteur, [la largeur et la couleur [R, G, B]]]
    new_image = np.array([[[0., 0., 0.] for j in range(largeur)] for i in range(hauteur)])
    for y in range(hauteur):
        for x in range(largeur):
            new_image[y][x] = photo[y * resolution][x * resolution]
    return new_image


print("Pixélisation en cours...")
plt.figure(2)
image = plt.imshow(echantillonage(read_image, 5))
image.axes.get_xaxis().set_visible(False)
image.axes.get_yaxis().set_visible(False)
plt.show()



####################################################################
## Mise en niveau de gris
####################################################################


# Cette fonction remplace la valeur RGB de chaque pixel par la même valeur (couleur)
def mise_en_gris(photo):
    for y in range(len(photo)):
        for x in range(len(photo[y])):
            couleur = photo[y][x][0] * 0.2125 + photo[y][x][1] * 0.7154 + photo[y][x][2] * 0.0721
            photo[y][x] = [couleur, couleur, couleur]
    return photo



print("Mise en noir et blanc...")
plt.figure(3)
image = plt.imshow(mise_en_gris(read_image))
image.axes.get_xaxis().set_visible(False)
image.axes.get_yaxis().set_visible(False)
plt.show()


####################################################################
## Floutage
####################################################################


filtre_moy = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]


def Floutage(photo, filtre):
    haut = 0  # int((len(filtre) - 1) / 2)  # Le centre du filtre est sur le pixel ciblé. Si on remplace la valeur par 0, le
    gauche = 0  # int((len(filtre[0]) - 1) / 2)  # coin haut-gauche du filtre est sur le pixel ciblé (filtre Gaussien)
    r, g, b = 0., 0., 0.  # r, g, b et count sont des valeurs float nulle
    count = 0.
    photo_floutee = np.copy(photo)  # On crée une copy du tableau photo sous le nom photo_floutee
    for y in range(len(photo)):
        for x in range(len(photo[y])):  # Pour chaque pixel de l'image :
            for hauteur in range(len(filtre)):
                for largeur in range(len(filtre[0])):  # Répété en fonction de la taille du filtre
                    try:  # On essaye de récupérer la couleur de chaque pixel dans le filtre
                        r += photo[y - haut + hauteur][x - gauche + largeur][0] * filtre[hauteur][largeur]
                        g += photo[y - haut + hauteur][x - gauche + largeur][1] * filtre[hauteur][largeur]
                        b += photo[y - haut + hauteur][x - gauche + largeur][2] * filtre[hauteur][largeur]
                        count += filtre[hauteur][largeur]
                    except:  # Si il n'y a pas de pixel aux coordonnés, il passe au suivant
                        pass
            r = r / count
            g = g / count
            b = b / count
            photo_floutee[y][x] = [r, g, b]  # On modifie le pixel par les nouvelles valeurs obtenues
            r, g, b = 0., 0., 0.
            count = 0.
    return photo_floutee


# Cett fonction crée un tableu avec 2 dimentions et avec les valeurs du filtre de Gauss
def FiltreGauss(sigma, taille):
    filtre = np.array([[((1 / (taille ** 2)) / (sigma * sqrt(2 * pi))) * exp(-((x ** 2 + y ** 2) / (2 * (sigma ** 2))))
                        for x in range(taille)] for y in range(taille)])
    return filtre



print("Floutage en cours...")
plt.figure(4)
image = plt.imshow(Floutage(read_image, FiltreGauss(1000, 7)))
image.axes.get_xaxis().set_visible(False)
image.axes.get_yaxis().set_visible(False)
plt.show()



####################################################################
# Déterioration de l'image avec ajout de bruit
####################################################################


def deterioration(photo, taux):
    nb_lignes, nb_col, nb_coul = np.shape(photo)
    # Normalisation de l'image
    photo_abimee = np.copy(photo)
    for i in range(nb_lignes):
        for j in range(nb_col):
            nb_aleatoire = rd.random()
            if nb_aleatoire < taux / 100:
                photo_abimee[i, j] = photo_abimee[i, j] * nb_aleatoire
    return photo_abimee



print("Détérioration en cours...")
plt.figure(5)
image_det = deterioration(read_image, 10)
image = plt.imshow(image_det)
image.axes.get_xaxis().set_visible(False)
image.axes.get_yaxis().set_visible(False)
plt.show()



####################################################################
## Filtrage anti-bruit
####################################################################


# Cette fonction va récupérer tout les pixels dans une zone (taille du filtre) et faire la médiane des valeurs
# pour supprimer les défaults
def FiltreMedian(photo, taille):
    filtre = np.array([[1 for _ in range(taille)] for _ in range(taille)])  # création d'un tableau avec 2 dimentions
    haut = int((len(filtre) - 1) / 2)  # Le centre du filtre est sur le pixel central
    gauche = int((len(filtre[0]) - 1) / 2)  # (ou haut gauche pour des nombres pairs)
    r, g, b = [], [], []  # r, g et b sont des tableau vides
    photo_corigee = np.copy(photo)
    for y in range(len(photo)):
        for x in range(len(photo[y])):
            for hauteur in range(len(filtre)):
                for largeur in range(len(filtre[0])):
                    try:  # On ajoute les valeurs de rouge, vert et bleu qui sont dans le filtre
                        r.append(photo[y - haut + hauteur][x - gauche + largeur][0])
                        g.append(photo[y - haut + hauteur][x - gauche + largeur][1])
                        b.append(photo[y - haut + hauteur][x - gauche + largeur][2])
                    except:
                        pass
            # On récupère la valeur médiane de chaque tableau de couleur et on l'ajoute au pixel de la photo corigé
            rouge = np.median(r)
            vert = np.median(g)
            bleu = np.median(b)
            photo_corigee[y][x] = [rouge, vert, bleu]
            r, g, b = [], [], []
    return photo_corigee



print("Réparation en cours...")
plt.figure(6)
image = plt.imshow(FiltreMedian(image_det, 5))
image.axes.get_xaxis().set_visible(False)
image.axes.get_yaxis().set_visible(False)
plt.show()



####################################################################
## Détection de contours
####################################################################


i = 2

filtre_horizontal = [
    [-1, 0, 1],
    [-i, 0, i],
    [-1, 0, 1]
]

filtre_vertical = [
    [-1, -i, -1],
    [0, 0, 0],
    [1, i, 1]
]


# Cette fonction mesure la différence de couleur entre chaque pixel et combine la valeur trouvée par
# le filtre horizontal et vertical pour renvoyer une image avec les contour des formes de l'image
def Contour(photo, GradX, GradY):
    r, g, b = 0., 0., 0.
    diviseur = GradX[0][2] + GradX[1][2] + GradX[2][2]
    photoH = np.copy(photo)  # tableau avec le filtre horizontal
    photoV = np.copy(photo)  # tableau avec le filtre vertical
    photo_contour = np.copy(photo)  # tableau avec le filtre horizontal combiné à celui vertical
    for _ in range(2):  # On répète deux fois l'opération (pour l'horizontal et le vertical)
        if _ == 1:  # On défini des variables pour ne pas écrire dux fois le même code
            photo_actu = photoH
            tableau = GradX
        else:
            photo_actu = photoV
            tableau = GradY
        for y in range(len(photo)):
            for x in range(len(photo[y])):
                for hauteur in range(3):
                    for largeur in range(3):
                        try:
                            r += photo[y - 1 + hauteur][x - 1 + largeur][0] * tableau[hauteur][largeur]
                            g += photo[y - 1 + hauteur][x - 1 + largeur][1] * tableau[hauteur][largeur]
                            b += photo[y - 1 + hauteur][x - 1 + largeur][2] * tableau[hauteur][largeur]
                        except:
                            pass
                r = abs(r) / diviseur
                g = abs(g) / diviseur
                b = abs(b) / diviseur
                photo_actu[y][x] = [r, g, b]
                r, g, b = 0., 0., 0.
    for y in range(len(photo_contour)):  # On combine les deux filtres
        for x in range(len(photo_contour[y])):
            if photoH[y][x][0] >= photoV[y][x][0]:
                photo_contour[y][x][0] = photoH[y][x][0]
            else:
                photo_contour[y][x][0] = photoV[y][x][0]
            if photoH[y][x][1] >= photoV[y][x][1]:
                photo_contour[y][x][1] = photoH[y][x][1]
            else:
                photo_contour[y][x][1] = photoV[y][x][1]
            if photoH[y][x][2] >= photoV[y][x][2]:
                photo_contour[y][x][2] = photoH[y][x][2]
            else:
                photo_contour[y][x][2] = photoV[y][x][2]
    return photo_contour


def fonction_test(image, taux):
    new_image = np.copy(image)
    for y in range(len(image)):
        for x in range(len(image[y])):
            if image[y][x][0] * 100 >= taux or image[y][x][1] * 100 >= taux or image[y][x][2] * 100 >= taux:
                new_image[y][x] = [1, 1, 1]
            else:
                new_image[y][x] = image[y][x]
    return new_image


tableau_image = Contour(read_image, filtre_horizontal, filtre_vertical)

print("Détourage en cours...")
plt.figure(7)
image = plt.imshow(tableau_image)
image.axes.get_xaxis().set_visible(False)
image.axes.get_yaxis().set_visible(False)
plt.show()

