import tkinter
from Démineur.main_demineur import Demineur
from Wordle.wordle import Wordle
from Labyrinthe.main_labyrinthe import Laby_2000
from Labyrinthe.labyrinthe_bis import Labyrinthe_Etoile
from Morpion.main_Morpion import Morpion


class Tkinter:

    def __init__(self):
        self.running = True
        self.game_actuel = 1

        self.app = tkinter.Tk()
        self.app.title("Fenêtre de Test")
        self.app.iconbitmap('game.ico')

        self.fullScreenState = True
        self.app.geometry(f"{self.app.winfo_screenwidth()}x{self.app.winfo_screenheight()}")
        self.app.state("zoomed")
        self.app.attributes("-fullscreen", self.fullScreenState)

        self.app.update()
        self.frame_header = tkinter.Frame(self.app, bg='#DDDDDD', width=self.app.winfo_width(), height=self.app.winfo_height()/5)
        self.frame_bibl = tkinter.Frame(self.app, bg="green", width=self.app.winfo_width() * 3 / 4, height=self.app.winfo_height()*4/5)
        self.frame_desc = tkinter.Frame(self.app, width=self.app.winfo_width() / 4, height=self.app.winfo_height()*4/5)

        self.frame_header.grid(row=0, column=0, columnspan=4)
        self.frame_bibl.grid(row=1, column=0, rowspan=3, columnspan=3)
        self.frame_desc.grid(row=1, column=3, rowspan=3)

        # >>>> Gérer la bibliothèque de jeux avec les boutons et la barre de défilement >>>> #

        # Reconfigure la Frame de la zone bibliothèque
        self.frame_bibl.grid_rowconfigure(0, weight=1)
        self.frame_bibl.grid_columnconfigure(0, weight=1)
        self.frame_bibl.grid_propagate(False)

        # Création d'une zone pour faire le défilement des boutons de jeu
        self.canvas_bibl = tkinter.Canvas(self.frame_bibl, bg="yellow")
        self.canvas_bibl.grid(row=0, column=0, sticky="news")

        # Création de la ScrollBar, la barre de défilement
        self.scrollBar_bibl = tkinter.Scrollbar(self.frame_bibl, orient="vertical", command=self.canvas_bibl.yview)
        self.scrollBar_bibl.grid(row=0, column=1, sticky='ns')
        self.canvas_bibl.configure(yscrollcommand=self.scrollBar_bibl.set)

        # Crée une Frame pour stocker les boutons et gérer le défilement
        self.frame_boutons = tkinter.Frame(self.canvas_bibl, bg="blue")
        self.canvas_bibl.create_window((0, 0), window=self.frame_boutons, anchor='nw')

        # Bibliothèque qui gère les différentss jeux, avec les informations les concernant
        self.documentary = {
            1: ["Démineur 3000", tkinter.PhotoImage(file='Image_demineur.png'), "Le but est de détérer tout le champ de mine...\nsans exploser...\nIl faut pour cela faire un clic droit pour placer un drapeau là où il y a des mines, et le faire bien entendu le plus vite possible.\nTOUCHE 'R' pour recommencer"],
            2: ["WORDLE: Le Mot", tkinter.PhotoImage(file='Image_wordle.png'), "L'objectif est de trouver le bon mot. Mais il faut réfléchir, et proposer d'autres mots, qui vont aider à trouver les lettres du bon mot.\nUne lettre verte signifie qu'elle est bien placé et une orange qu'elle est dans le mot mais pas à la bonne place.\nGardez en tête qu'il peut il y avoir deux fois la même lettre dans le même mot..."],
            3: ["Laby 2000", tkinter.PhotoImage(file='Image_laby2000.png'), "Un labyrinthe dans toute sa splendeur, et avec un style des années 2000. Le but est bien entendu de le finir, mais surtout de trouver le chemin le plus court.\nTOUCHE 'R' pour générer un nouveau labyrinthe\nTOUCHE 'A' pour créer le labyrinthe\nTOUCHE 'ESPACE' pour voir la construction du labyrinthe"],
            4: ["Quatrième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 4 description"],
            5: ["Tic Tac Toe", tkinter.PhotoImage(file='Image_morpion.png'), "Un jeu du Morpion à deux joueur classic.\nAssembler une ligne de trois jetons avant l'autre joueur et remportez la partie.\nTOUCHE 'R' pour recommencer"],
            6: ["Sixième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 6 description"],
            7: ["Labyrinthe Étoile", tkinter.PhotoImage(file='Image_labyEtoile.png'), "Un labyrinthe tout ce qu'il y a de plus classic, avec un départ, une arrivée et des murs. Le but est bien évidamment de trouver le chemin le plus court.\nTOUCHE 'R' pour générer un nouveau labyrinthe\nTOUCHE 'A' pour créer le labyrinthe\nTOUCHE 'ESPACE' pour voir la construction du labyrinthe"],
            8: ["Cette fois c'est le titre qui est long", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 8 description"],
            9: ["Neuvième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 9 description"],
            10: ["Dixième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 10 description"],
            11: ["Onzième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 11 description"],
            12: ["Douzième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 12 description"],
            13: ["Treizième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 13 description"],
            14: ["Quatorzième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 14 description"],
            15: ["Quinzième jeu", tkinter.PhotoImage(file='Image_test.png'), "Je suis la 15 description"],
        }
        self.description = tkinter.StringVar()
        self.description.set(self.documentary[1][2])
        self.titre_jeu = tkinter.StringVar()
        self.titre_jeu.set(self.documentary[1][0])

        # Créer un tableau avec les boutons de taille 3XTaille de la bibliothèque
        self.buttons = [[tkinter.Button() for _ in range(3)] for _ in range(int(len(self.documentary)/3))]

        # Affiche tous les boutons en fonction de leurs informations
        for i in range(0, int(len(self.documentary)/3)):
            for j in range(0, 3):
                self.buttons[i][j] = tkinter.Button(self.frame_boutons, text=self.documentary[i*3+j+1][0], font='Roboto.ttf 15', wraplength=self.frame_bibl.winfo_reqwidth()/3, image=self.documentary[i*3+j+1][1], anchor="s", width=self.frame_bibl.winfo_reqwidth()/3, height=self.frame_bibl.winfo_reqheight()/3, compound=tkinter.BOTTOM, overrelief=tkinter.GROOVE)
                self.buttons[i][j].grid(row=i, column=j, sticky='news')
        for i in range(0, int(len(self.documentary)/3)):
            for j in range(0, 3):
                index = i * 3 + j + 1
                if index == 1:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(1)
                elif index == 2:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(2)
                elif index == 3:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(3)
                elif index == 4:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(4)
                elif index == 5:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(5)
                elif index == 6:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(6)
                elif index == 7:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(7)
                elif index == 8:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(8)
                elif index == 9:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(9)
                elif index == 10:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(10)
                elif index == 11:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(11)
                elif index == 12:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(12)
                elif index == 13:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(13)
                elif index == 14:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(14)
                elif index == 15:
                    self.buttons[i][j]['command'] = lambda: self.ChangeGame(15)

        # Update la Frame contenant les boutons pour initialiser la barre de défilement
        self.frame_boutons.update_idletasks()

        # Configure la zone de défilement de la ScrollBar
        self.canvas_bibl.config(scrollregion=self.canvas_bibl.bbox("all"))

        # <<<< Fin de la configuration de la zone Bibliotèque <<<< #

        # >>>> Gérer la zone de description du jeu + Bouton START >>>> #

        self.frame_desc.columnconfigure(0, weight=1)
        self.frame_desc.rowconfigure(0, weight=1)
        self.frame_desc.rowconfigure(1, weight=1)
        self.frame_desc.rowconfigure(2, weight=1)
        self.frame_desc.grid_propagate(False)

        self.show_image = tkinter.Label(self.frame_desc, textvariable=self.titre_jeu, image=self.documentary[1][1], compound=tkinter.BOTTOM, font='Roboto.ttf 30 bold', wraplength=self.frame_desc.winfo_reqwidth())
        self.show_image.grid(row=0, column=0, sticky='n')

        self.show_text = tkinter.Label(self.frame_desc, textvariable=self.description, wraplength=self.frame_desc.winfo_reqwidth(), font='Arial, 12')
        self.show_text.grid(row=1, column=0)

        self.show_play = tkinter.Button(self.frame_desc, text="JOUER", font='Roboto.ttf 30 bold', fg='red', activeforeground='red', borderwidth=5, command=self.StartGame)
        self.show_play.grid(row=2, column=0, sticky='s')

        # <<<< Fin de la configuration de la zone Description <<<< #

        # >>>> Gérer la zone Titre >>>> #

        self.frame_header.columnconfigure(0, weight=1)
        self.frame_header.rowconfigure(0, weight=1)
        self.frame_header.grid_propagate(False)
        self.header_titre = tkinter.Button(self.frame_header, text='Le Jeu Des Jeux', font='Roboto.ttf 50 underline bold', bg='#DDDDDD', borderwidth=0, activebackground='#DDDDDD', overrelief='flat', command=self.credit)
        self.header_titre.grid(column=0, row=0)
        self.header_bouton = tkinter.Button(self.frame_header, text='QUITTER', font='Roboto.ttf 20', activebackground='red', bg='#F0F0F0', overrelief=tkinter.RAISED, command=lambda: self.QUITTER(self.app))
        self.header_bouton.grid(column=0, row=0, sticky='ne')

        # <<<< Fin de la configuration de la zone Titre <<<< #

        self.app.configure(bg="#bebebe")
        self.app.bind("<Escape>", self.quitFullScreen)
        self.app.bind("<F11>", self.SwitchFullScreen)
        self.app.resizable(height=0, width=0)
        self.app.mainloop()

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.app.attributes("-fullscreen", self.fullScreenState)

    def SwitchFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.app.attributes("-fullscreen", self.fullScreenState)

    def QUITTER(self, widget):
        widget.destroy()

    def credit(self):
        new_window = tkinter.Toplevel(width=self.app.winfo_screenwidth()/2, height=self.app.winfo_screenheight()/2)
        new_window.resizable(False, False)
        new_window.title("Crédit")
        new_window.columnconfigure(0, weight=1)
        new_window.rowconfigure(0, weight=1)
        new_window.grid_propagate(False)
        new_window.focus()
        new_window.bind('<FocusOut>', lambda widget: self.QUITTER(new_window))
        label = tkinter.Label(new_window, wraplength=new_window.winfo_reqwidth(), font='Roboto.ttf, 20', text="Cette application a été créée dans le cadre d'un projet en NSI.\nCette version est une version experimentale créée dans le but d'apprendre le fonctionnement du module \"Tkinter\" et \"Pygame\" ainsi que plus largement le langage de programmation Python.\nL'application est bien entendu susceptible de recevoir des mises à jour dans le futur...\nDéveloppeur : Antoine CARREZ 1°5")
        label.grid(column=0, row=0)

    def ChangeGame(self, index):
        self.show_image.configure(image=self.documentary[index][1])
        self.description.set(self.documentary[index][2])
        self.titre_jeu.set(self.documentary[index][0])
        self.game_actuel = index

    def StartGame(self):
        if self.game_actuel == 1:
            game = Demineur()
            game.run()
        elif self.game_actuel == 2:
            game = Wordle()
            game.run()
        elif self.game_actuel == 3:
            game = Laby_2000()
            game.run()
        elif self.game_actuel == 5:
            game = Morpion()
            game.run()
        elif self.game_actuel == 7:
            game = Labyrinthe_Etoile()
            game.run()


fenetre = Tkinter()
