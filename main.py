import tkinter as tk
from random import randint, choice

# Classe Navire
class Navire:
    # Constructeur de la classe Navire
    def __init__(self, nom, taille):
        self.nom = nom  # Nom du navire (ex: "Porte-avions")
        self.taille = taille  # Taille du navire (nombre de cases)
        self.positions = []  # Liste des positions occupées par le navire
        self.touchees = []  # Liste des positions touchées

    # Fonction pour vérifier si le navire est coulé
    def est_coule(self):
        return len(self.touchees) == self.taille

    # Fonction pour ajouter une position au navire
    def ajouter_position(self, position):
        self.positions.append(position)

    # Fonction pour toucher une position du navire
    def toucher(self, position):
        if position in self.positions and position not in self.touchees:
            self.touchees.append(position)
            return True
        return False

# Classe Plateau
class Plateau:
    # Constructeur de la classe Plateau
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [[' ' for _ in range(taille)] for _ in range(taille)]
        self.navires = []
    # Fonction pour placer un navire sur le plateau
    def placer_navire(self, navire, positions):
        for pos in positions:
            x, y = pos
            self.grille[x][y] = 'N'  # Marquer la case comme occupée par un navire
        navire.positions = positions
        self.navires.append(navire)
    # Fonction pour vérifier un tir sur le plateau
    def verifier_tir(self, x, y):
        for navire in self.navires:
            if (x, y) in navire.positions:
                navire.toucher((x, y))
                return "Touché" if not navire.est_coule() else "Coulé"
        return "Manqué"
    # Fonction pour placer un navire aléatoirement
    def placement_aleatoire(self, navire):
        orientation = choice(["H", "V"])
        while True:
            if orientation == "H":
                x = randint(0, self.taille - 1)
                y = randint(0, self.taille - navire.taille)
                positions = [(x, y + i) for i in range(navire.taille)]
            else:
                x = randint(0, self.taille - navire.taille)
                y = randint(0, self.taille - 1)
                positions = [(x + i, y) for i in range(navire.taille)]
            if all(self.grille[x][y] == ' ' for x, y in positions):
                self.placer_navire(navire, positions)
                break

# Classe Joueur
class Joueur:
    # Constructeur de la classe Joueur
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()
    # Fonction pour tirer sur le plateau de l'adversaire
    def tirer(self, adversaire, x, y):
        return adversaire.plateau.verifier_tir(x, y)
# Classe Ordinateur
class Ordinateur(Joueur):
    # Constructeur de la classe Ordinateur
    def __init__(self):
        super().__init__("Ordinateur")
        self.placer_navires_aleatoirement()
    # Fonction pour choisir les coordonnées de tir aléatoirement
    def choix_tir(self):
        return randint(0, 9), randint(0, 9)
    # Fonction pour placer les navires aléatoirement
    def placer_navires_aleatoirement(self):
        for nom, taille in [("Porte-avions", 5), ("Croiseur", 4), ("Destroyer", 3), ("Sous-marin", 2), ("Sous-marin", 2)]:
            navire = Navire(nom, taille)
            self.plateau.placement_aleatoire(navire)

# Interface graphique
class InterfaceBatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")
        self.joueur = Joueur("Joueur")
        self.ordinateur = Ordinateur()
        self.navires_a_placer = [("Porte-avions", 5), ("Croiseur", 4), ("Destroyer", 3), ("Sous-marin", 2)]
        self.navire_en_cours = None
        self.creer_interface()
    # Fonction pour créer l'interface graphique
    def creer_interface(self):
        frame = tk.Frame(self.root)
        frame.pack()
        
        self.label_tour = tk.Label(frame, text="Placement des navires", font=("Arial", 12))
        self.label_tour.grid(row=0, column=0, columnspan=10)
        
        self.grille_joueur = [[tk.Button(frame, width=3, height=1, command=lambda x=i, y=j: self.placer_navire(x, y)) for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].grid(row=i+1, column=j)
        
        self.bouton_nouvelle_partie = tk.Button(self.root, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.pack()
    # Fonction pour placer un navire sur la grille
    def placer_navire(self, x, y):
        if self.navires_a_placer:
            nom, taille = self.navires_a_placer[0]
            self.navire_en_cours = Navire(nom, taille)
            positions = [(x, y + i) for i in range(taille) if y + i < 10]
            if len(positions) == taille and all(self.joueur.plateau.grille[x][y] == ' ' for x, y in positions):
                self.joueur.plateau.placer_navire(self.navire_en_cours, positions)
                for px, py in positions:
                    self.grille_joueur[px][py].config(bg="gray")
                self.navires_a_placer.pop(0)
            if not self.navires_a_placer:
                self.label_tour.config(text="Début de la partie !")

    # Fonction pour démarrer une nouvelle partie
    def nouvelle_partie(self):
        print("Nouvelle partie démarrée")
        self.label_tour.config(text="Placement des navires")
        self.joueur = Joueur("Joueur")
        self.ordinateur = Ordinateur()
        self.navires_a_placer = [("Porte-avions", 5), ("Croiseur", 4), ("Destroyer", 3), ("Sous-marin", 2), ("Sous-marin", 2)]
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].config(bg="SystemButtonFace")

# Fonction principale
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()