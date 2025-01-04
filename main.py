import tkinter as tk
from random import randint, choice
from tkinter import messagebox

class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.touchees = []

    def est_coule(self):
        return len(self.touchees) == self.taille

    def ajouter_position(self, position):
        self.positions.append(position)

    def toucher(self, position):
        if position in self.positions and position not in self.touchees:
            self.touchees.append(position)
            return True
        return False

class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [[' ' for _ in range(taille)] for _ in range(taille)]
        self.navires = []

    def placer_navire(self, navire, positions):
        for pos in positions:
            x, y = pos
            self.grille[x][y] = 'N'
        navire.positions = positions
        self.navires.append(navire)

    def verifier_tir(self, x, y):
        for navire in self.navires:
            if (x, y) in navire.positions:
                navire.toucher((x, y))
                return "Touché" if not navire.est_coule() else "Coulé"
        return "Manqué"

    def get_navire(self, x, y):
        for navire in self.navires:
            if (x, y) in navire.positions:
                return navire
        return None

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
            
            valide = True
            for pos_x, pos_y in positions:
                if not (0 <= pos_x < self.taille and 0 <= pos_y < self.taille):
                    valide = False
                    break
                if self.grille[pos_x][pos_y] != ' ':
                    valide = False
                    break
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = pos_x + dx, pos_y + dy
                        if 0 <= nx < self.taille and 0 <= ny < self.taille and self.grille[nx][ny] != ' ':
                            valide = False
                            break
                    if not valide:
                        break
                if not valide:
                    break
            
            if valide:
                self.placer_navire(navire, positions)
                break

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()

    def tirer(self, adversaire, x, y):
        return adversaire.plateau.verifier_tir(x, y)

class Ordinateur(Joueur):
    def __init__(self):
        super().__init__("Ordinateur")
        self.derniers_tirs_reussis = []
        self.placer_navires_aleatoirement()

    def placer_navires_aleatoirement(self):
        navires = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer", 3),
            ("Destroyer", 3),
            ("Sous-marin", 2),
            ("Sous-marin", 2)
        ]
        for nom, taille in navires:
            navire = Navire(nom, taille)
            self.plateau.placement_aleatoire(navire)

class InterfaceBatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")
        self.root.configure(bg="lightgrey")
        self.partie_terminee = False
        
        self.label_tour = tk.Label(root, text="Placement des navires", bg="lightgrey")
        self.label_tour.grid(row=0, column=0, columnspan=20)
        
        self.frame_joueur = tk.Frame(root, bg="#87CEEB")
        self.frame_joueur.grid(row=1, column=0, padx=10, pady=10)
        
        self.frame_ordinateur = tk.Frame(root, bg="#87CEEB")
        self.frame_ordinateur.grid(row=1, column=1, padx=10, pady=10)
        
        self.grille_joueur = [[tk.Button(self.frame_joueur, width=2, height=1, bg="#87CEEB", 
                             command=lambda x=i, y=j: self.placer_navire_joueur(x, y)) 
                             for j in range(10)] for i in range(10)]
        
        self.grille_ordinateur = [[tk.Button(self.frame_ordinateur, width=2, height=1, bg="#87CEEB", 
                                command=lambda x=i, y=j: self.tirer(x, y)) 
                                for j in range(10)] for i in range(10)]
        
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].grid(row=i, column=j)
                self.grille_ordinateur[i][j].grid(row=i, column=j)
        
        self.bouton_commencer = tk.Button(root, text="Commencer le jeu", 
                                        command=self.commencer_jeu, state="disabled", 
                                        bg="lightgrey")
        self.bouton_commencer.grid(row=2, column=0, columnspan=20, pady=10, sticky="ew")
        
        self.bouton_recommencer = tk.Button(root, text="Recommencer la partie", 
                                          command=self.nouvelle_partie, bg="lightgrey")
        self.bouton_recommencer.grid(row=3, column=0, columnspan=20, pady=10, sticky="ew")
        
        self.orientation = "H"
        self.root.bind("<space>", self.changer_orientation)
        
        self.tour_joueur = True
        self.nouvelle_partie()

    def verifier_fin_partie(self):
        tous_navires_joueur_coules = all(navire.est_coule() for navire in self.joueur.plateau.navires)
        tous_navires_ordi_coules = all(navire.est_coule() for navire in self.ordinateur.plateau.navires)

        if tous_navires_joueur_coules:
            self.partie_terminee = True
            self.label_tour.config(text="Vous avez perdu !")
            messagebox.showinfo("Fin de partie", "Vous avez perdu !")
            self.desactiver_grilles()
            return True
        elif tous_navires_ordi_coules:
            self.partie_terminee = True
            self.label_tour.config(text="Vous avez gagné !")
            messagebox.showinfo("Fin de partie", "Vous avez gagné !")
            self.desactiver_grilles()
            return True
        return False

    def desactiver_grilles(self):
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].config(state="disabled")
                self.grille_ordinateur[i][j].config(state="disabled")

    def nouvelle_partie(self):
        self.partie_terminee = False
        self.label_tour.config(text="Placement des navires")
        self.joueur = Joueur("Joueur")
        self.ordinateur = Ordinateur()
        self.navires_a_placer = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer", 3),
            ("Destroyer", 3),
            ("Sous-marin", 2),
            ("Sous-marin", 2)
        ]
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].config(bg="#87CEEB", text="", state="normal")
                self.grille_ordinateur[i][j].config(bg="#87CEEB", text="", state="normal")
        self.bouton_commencer.config(state="disabled")
        self.tour_joueur = True
        self.placer_navires_joueur()

    def changer_orientation(self, event):
        self.orientation = "V" if self.orientation == "H" else "H"
        if self.navires_a_placer:
            nom, taille = self.navires_a_placer[0]
            self.label_tour.config(text=f"Placez votre {nom} (taille {taille}) - "
                                      f"Orientation: {'Verticale' if self.orientation == 'V' else 'Horizontale'}")

    def placer_navires_joueur(self):
        if self.navires_a_placer:
            nom, taille = self.navires_a_placer[0]
            self.navire_en_cours = Navire(nom, taille)
            self.label_tour.config(text=f"Placez votre {nom} (taille {taille}) - "
                                      f"Orientation: {'Horizontale' if self.orientation == 'H' else 'Verticale'}")
        else:
            self.label_tour.config(text="Tous les navires sont placés !")
            self.bouton_commencer.config(state="normal")

    def placer_navire_joueur(self, x, y):
        if self.navire_en_cours:
            if self.orientation == "H":
                positions = [(x, y + i) for i in range(self.navire_en_cours.taille)]
            else:
                positions = [(x + i, y) for i in range(self.navire_en_cours.taille)]
            
            valide = True
            for pos_x, pos_y in positions:
                if not (0 <= pos_x < 10 and 0 <= pos_y < 10):
                    valide = False
                    break
                if self.grille_joueur[pos_x][pos_y].cget('bg') != '#87CEEB':
                    valide = False
                    break
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = pos_x + dx, pos_y + dy
                        if 0 <= nx < 10 and 0 <= ny < 10 and self.grille_joueur[nx][ny].cget('bg') != '#87CEEB':
                            valide = False
                            break
                    if not valide:
                        break
                if not valide:
                    break
            
            if valide:
                for pos in positions:
                    self.grille_joueur[pos[0]][pos[1]].config(bg='darkgrey')
                self.joueur.plateau.placer_navire(self.navire_en_cours, positions)
                self.navires_a_placer.pop(0)
                self.placer_navires_joueur()

    def commencer_jeu(self):
        self.label_tour.config(text="À vous de jouer !")
        self.bouton_commencer.config(state="disabled")

    def tirer(self, x, y):
        if self.partie_terminee:
            return
        if self.tour_joueur and self.grille_ordinateur[x][y].cget('bg') not in ['red', 'darkblue', 'black']:
            resultat = self.joueur.tirer(self.ordinateur, x, y)
            if resultat == "Touché" or resultat == "Coulé":
                self.grille_ordinateur[x][y].config(bg='red')
                if resultat == "Coulé":
                    navire = self.ordinateur.plateau.get_navire(x, y)
                    if navire:
                        for pos in navire.positions:
                            self.grille_ordinateur[pos[0]][pos[1]].config(bg='black')
                self.label_tour.config(text=f"{resultat} !")
                if self.verifier_fin_partie():
                    return
            else:
                self.grille_ordinateur[x][y].config(bg='darkblue')
                self.label_tour.config(text="Manqué !")
                self.tour_joueur = False
                self.root.after(1000, self.tour_ordinateur)

    def tour_ordinateur(self):
        if self.partie_terminee:
            return
        if not self.tour_joueur:
            x, y = randint(0, 9), randint(0, 9)
            while self.grille_joueur[x][y].cget('bg') in ['red', 'darkblue', 'black']:
                x, y = randint(0, 9), randint(0, 9)
            
            resultat = self.ordinateur.tirer(self.joueur, x, y)
            if resultat == "Touché" or resultat == "Coulé":
                self.grille_joueur[x][y].config(bg='red')
                if resultat == "Coulé":
                    navire = self.joueur.plateau.get_navire(x, y)
                    if navire:
                        for pos in navire.positions:
                            self.grille_joueur[pos[0]][pos[1]].config(bg='black')
                self.label_tour.config(text=f"L'ordinateur a {resultat.lower()} un navire !")
                
                if self.verifier_fin_partie():
                    return
                
                if resultat != "Coulé":
                    self.root.after(1000, self.tour_ordinateur)
                else:
                    self.tour_joueur = True
            else:
                self.grille_joueur[x][y].config(bg='darkblue')
                self.label_tour.config(text="L'ordinateur a manqué !")
                self.tour_joueur = True

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()