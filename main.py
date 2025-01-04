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

class InterfaceBatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")
        self.creer_interface()

    def creer_interface(self):
        frame = tk.Frame(self.root)
        frame.pack()
        
        self.label_tour = tk.Label(frame, text="Tour du joueur", font=("Arial", 12))
        self.label_tour.grid(row=0, column=0, columnspan=10)
        
        self.grille_joueur = [[tk.Button(frame, width=3, height=1, command=lambda x=i, y=j: self.jouer_tour(x, y)) for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].grid(row=i+1, column=j)
        
        self.bouton_nouvelle_partie = tk.Button(self.root, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.pack()
    
    def jouer_tour(self, x, y):
        print(f"Tir en ({x}, {y})")
        self.label_tour.config(text="Tour de l'ordinateur")
    
    def nouvelle_partie(self):
        print("Nouvelle partie démarrée")
        self.label_tour.config(text="Tour du joueur")
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].config(bg="SystemButtonFace")

# déclare la classe InterfaceBatailleNavale pour initialiser la fenêtre et les boutons
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()