import tkinter as tk
from tkinter import *
from random import randint

# déclare la classe Navire pour initialiser le nom, la taille, les positions et les positions touchées des bateaux
class Navire:
    def __init__(self, nom, taille):
        self.nom = nom  # Nom du navire (ex: "Porte-avions")
        self.taille = taille  # Taille du navire (nombre de cases)
        self.positions = []  # Liste des positions occupées par le navire
        self.touche = []  # Liste des positions touchées
    # vérifie si le navire est coulé (toutes les positions touchées)
    def est_coule(self):
        return len(self.touche) == self.taille
    # déclare la classe Plateau pour initialiser la taille, la grille et les navires
    def ajouter_position(self, position):
        self.positions.append(position)
    # vérifie si une position est touchée et l'ajoute à la liste des positions touchées
    def toucher(self, position):
        if position in self.positions and position not in self.touche:
            self.touche.append(position)
            return True
        return False

# déclare la classe Plateau pour initialiser la taille, la grille et les navires
class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [[' ' for _ in range(taille)] for _ in range(taille)]
        self.navires = []
    # place un navire sur le plateau
    def placer_navire(self, navire, positions):
        for pos in positions:
            x, y = pos
            self.grille[x][y] = 'N'  # Marquer la case comme occupée par un navire
        navire.positions = positions
        self.navires.append(navire)
    # vérifie si un tir touche un navire
    def verifier_tir(self, x, y):
        for navire in self.navires:
            if (x, y) in navire.positions:
                navire.toucher((x, y))
                return "Touché" if not navire.est_coule() else "Coulé"
        return "Manqué"

# déclare la classe Joueur pour initialiser le nom et le plateau
class Joueur:
    # déclare la classe Joueur pour initialiser le nom et le plateau
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()
    # déclare la classe Joueur pour initialiser le nom et le plateau
    def tirer(self, adversaire, x, y):
        return adversaire.plateau.verifier_tir(x, y)

# déclare la classe Joueur pour initialiser le nom et le plateau
class Ordi(Joueur):
    # déclare la classe Joueur pour initialiser le nom et le plateau
    def __init__(self):
        super().__init__("Ordinateur")
    # déclare la classe Joueur pour initialiser le nom et le plateau
    def choix_tir(self):
        return randint(0, 9), randint(0, 9)

# déclare la classe InterfaceBatailleNavale pour initialiser la fenêtre et les boutons
class InterfaceBatailleNavale:
    # déclare la classe InterfaceBatailleNavale pour initialiser la fenêtre et les boutons
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")
        self.creer_interface()
    # déclare la classe InterfaceBatailleNavale pour initialiser la fenêtre et les boutons
    def creer_interface(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.grille_joueur = [[tk.Button(self.root, width=3, height=1, command=lambda x=i, y=j: self.jouer_tour(x, y)) for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].grid(row=i, column=j)
    # déclare la classe InterfaceBatailleNavale pour initialiser la fenêtre et les boutons
    def jouer_tour(self, x, y):
        print(f"Tir en ({x}, {y})")

# déclare la classe InterfaceBatailleNavale pour initialiser la fenêtre et les boutons
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()