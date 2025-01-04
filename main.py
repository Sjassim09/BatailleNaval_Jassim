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

class InterfaceBatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")
        self.label_tour = tk.Label(root, text="Placement des navires")
        self.label_tour.grid(row=0, column=0, columnspan=10)
        
        self.frame_joueur = tk.Frame(root)
        self.frame_joueur.grid(row=1, column=0, columnspan=10)
        
        self.frame_ordinateur = tk.Frame(root)
        self.frame_ordinateur.grid(row=1, column=0, columnspan=10)
        self.frame_ordinateur.grid_forget()
        
        self.grille_joueur = [[tk.Button(self.frame_joueur, width=2, height=1, command=lambda x=i, y=j: self.placer_navire_joueur(x, y)) for j in range(10)] for i in range(10)]
        self.grille_ordinateur = [[tk.Button(self.frame_ordinateur, width=2, height=1, command=lambda x=i, y=j: self.tirer(x, y)) for j in range(10)] for i in range(10)]
        
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].grid(row=i, column=j)
        
        self.bouton_commencer = tk.Button(root, text="Commencer le jeu", command=self.afficher_plateau_jeu, state="disabled")
        self.bouton_commencer.grid(row=2, column=0, columnspan=10)
        
        self.orientation = "H"  # H pour horizontal, V pour vertical
        self.root.bind("<space>", self.changer_orientation)
        
        self.nouvelle_partie()

    def nouvelle_partie(self):
        print("Nouvelle partie démarrée")
        self.label_tour.config(text="Placement des navires")
        self.joueur = Joueur("Joueur")
        self.ordinateur = Ordinateur()
        self.navires_a_placer = [("Porte-avions", 5), ("Croiseur", 4), ("Destroyer", 3), ("Sous-marin", 2), ("Sous-marin", 2)]
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].config(bg="SystemButtonFace")
        self.placer_navires_joueur()

    def changer_orientation(self, event):
        self.orientation = "V" if self.orientation == "H" else "H"
        self.label_tour.config(text=f"Orientation: {'Horizontale' if self.orientation == 'H' else 'Verticale'}")

    def placer_navires_joueur(self):
        if self.navires_a_placer:
            nom, taille = self.navires_a_placer[0]
            self.navire_en_cours = Navire(nom, taille)
            self.label_tour.config(text=f"Placez votre {nom} (taille {taille}) - Orientation: {'Horizontale' if self.orientation == 'H' else 'Verticale'}")
        else:
            self.label_tour.config(text="Tous les navires sont placés !")
            self.bouton_commencer.config(state="normal")

    def placer_navire_joueur(self, x, y):
        if self.navire_en_cours:
            if self.orientation == "H":
                positions = [(x, y + i) for i in range(self.navire_en_cours.taille)]
            else:
                positions = [(x + i, y) for i in range(self.navire_en_cours.taille)]
            
            if all(0 <= pos[0] < 10 and 0 <= pos[1] < 10 and self.grille_joueur[pos[0]][pos[1]].cget('bg') == 'SystemButtonFace' for pos in positions):
                for pos in positions:
                    self.grille_joueur[pos[0]][pos[1]].config(bg='blue')
                self.joueur.plateau.placer_navire(self.navire_en_cours, positions)
                self.navires_a_placer.pop(0)
                self.placer_navires_joueur()

    def afficher_plateau_jeu(self):
        self.frame_joueur.grid_forget()
        self.frame_ordinateur.grid(row=1, column=0, columnspan=10)
        self.label_tour.config(text="À vous de jouer !")

    def tirer(self, x, y):
        resultat = self.ordinateur.plateau.verifier_tir(x, y)
        self.grille_ordinateur[x][y].config(text=resultat[0], state="disabled")
        if resultat == "Coulé":
            self.label_tour.config(text="Navire coulé !")
        elif resultat == "Touché":
            self.label_tour.config(text="Navire touché !")
        else:
            self.label_tour.config(text="Manqué !")

# Fonction principale
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()