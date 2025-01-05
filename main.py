import tkinter as tk # Importation de la bibliothèque tkinter
from random import randint, choice # Importation des fonctions randint et choice de la bibliothèque random
from tkinter import messagebox # Importation de la fonction messagebox de la bibliothèque tkinter

class Navire: # Initialisation de la classe Navire
    def __init__(self, nom, taille): # Initialisation des attributs de la classe Navire
        self.nom = nom # Nom du navire
        self.taille = taille # Taille du navire
        self.positions = [] # Liste des positions du navire
        self.touchees = [] # Liste des positions touchées du navire

    def est_coule(self): # Méthode qui permet de vérifier si le navire est coulé
        return len(self.touchees) == self.taille # Retourne True si le nombre de positions touchées est égal à la taille du navire

    def ajouter_position(self, position): # Méthode qui permet d'ajouter une position à la liste des positions du navire
        self.positions.append(position) # Ajout de la position à la liste des positions

    def toucher(self, position): # Méthode qui permet de toucher une position du navire
        if position in self.positions and position not in self.touchees: # Si la position est dans la liste des positions et n'est pas déjà touchée
            self.touchees.append(position) # Ajout de la position à la liste des positions touchées
            return True # Retourne True
        return False    # Retourne False

class Plateau: # Initialisation de la classe Plateau
    def __init__(self, taille=10): # Initialisation des attributs de la classe Plateau
        self.taille = taille # Taille du plateau
        self.grille = [[' ' for _ in range(taille)] for _ in range(taille)] # Initialisation de la grille du plateau
        self.navires = [] # Liste des navires du plateau

    def placer_navire(self, navire, positions): # Méthode qui permet de placer un navire sur le plateau
        for pos in positions: # Pour chaque position dans la liste des positions
            x, y = pos # Récupération des coordonnées x et y
            self.grille[x][y] = 'N' # Placement du navire sur la grille
        navire.positions = positions # Ajout des positions du navire à la liste des positions
        self.navires.append(navire) # Ajout du navire à la liste des navires    

    def verifier_tir(self, x, y): # Méthode qui permet de vérifier un tir sur le plateau
        for navire in self.navires: # Pour chaque navire dans la liste des navires
            if (x, y) in navire.positions: # Si la position est dans la liste des positions du navire
                navire.toucher((x, y)) # Toucher la position du navire
                return "Touché" if not navire.est_coule() else "Coulé" # Retourner "Touché" si le navire n'est pas coulé, sinon "Coulé"
        return "Manqué" # Retourner "Manqué" si le tir est raté

    def get_navire(self, x, y): # Méthode qui permet de récupérer un navire à une position donnée
        for navire in self.navires: # Pour chaque navire dans la liste des navires
            if (x, y) in navire.positions: # Si la position est dans la liste des positions du navire
                return navire # Retourner le navire
        return None # Retourner None si aucun navire n'est trouvé

    def placement_aleatoire(self, navire): # Méthode qui permet de placer un navire aléatoirement sur le plateau
        orientation = choice(["H", "V"]) # Choix aléatoire de l'orientation du navire
        while True: 
            if orientation == "H": # Si l'orientation est horizontale
                x = randint(0, self.taille - 1) # Génération aléatoire de la coordonnée x
                y = randint(0, self.taille - navire.taille) # Génération aléatoire de la coordonnée y
                positions = [(x, y + i) for i in range(navire.taille)] # Création de la liste des positions 
            else: 
                x = randint(0, self.taille - navire.taille) # Génération aléatoire de la coordonnée x
                y = randint(0, self.taille - 1) # Génération aléatoire de la coordonnée y
                positions = [(x + i, y) for i in range(navire.taille)]  # Création de la liste des positions
            
            valide = True # Initialisation de la variable valide à True
            for pos_x, pos_y in positions: # Pour chaque position dans la liste des positions
                if not (0 <= pos_x < self.taille and 0 <= pos_y < self.taille): # Si la position n'est pas dans le plateau
                    valide = False # La position n'est pas valide
                    break 
                if self.grille[pos_x][pos_y] != ' ': # Si la position n'est pas vide
                    valide = False # La position n'est pas valide
                    break 
                for dx in [-1, 0, 1]: # Pour chaque déplacement en x
                    for dy in [-1, 0, 1]: # Pour chaque déplacement en y
                        nx, ny = pos_x + dx, pos_y + dy # Calcul des nouvelles coordonnées
                        if 0 <= nx < self.taille and 0 <= ny < self.taille and self.grille[nx][ny] != ' ': # Si la nouvelle position n'est pas vide
                            valide = False # La position n'est pas valide
                            break 
                    if not valide: # Si la position n'est pas valide
                        break 
                if not valide:  # Si la position n'est pas valide
                    break
            
            if valide:
                self.placer_navire(navire, positions) # Placement du navire sur le plateau
                break
# Initialisation de la classe Joueur avec deux méthodes qui permetttent de tirer sur le plateau de l'adversaire et de placer les navires
class Joueur:
    def __init__(self, nom): # Initialisation de la classe Joueur
        self.nom = nom # Initialisation du nom du joueur
        self.plateau = Plateau() # Initialisation du plateau du joueur

    def tirer(self, adversaire, x, y): # Méthode qui permet de tirer sur le plateau de l'adversaire
        return adversaire.plateau.verifier_tir(x, y)    # Retourne le résultat du tir
# Initialisation de la classe Ordinateur qui hérite de la classe Joueur et qui permet de placer les navires aléatoirement
class Ordinateur(Joueur):
    def __init__(self):
        super().__init__("Ordinateur") # Initialisation de la classe Ordinateur
        self.derniers_tirs_reussis = [] # Initialisation de la liste des derniers tirs réussis
        self.placer_navires_aleatoirement() # Appel de la méthode placer_navires_aleatoirement

    def placer_navires_aleatoirement(self): # Méthode qui permet de placer les navires aléatoirement
        navires = [ # Liste des navires
            ("Porte-avions", 5), # Nom et taille du navire
            ("Croiseur", 4), 
            ("Destroyer", 3),
            ("Destroyer", 3),
            ("Sous-marin", 2),
            ("Sous-marin", 2)
        ]
        for nom, taille in navires: # Pour chaque nom et taille dans la liste des navires
            navire = Navire(nom, taille) # Création d'un navire
            self.plateau.placement_aleatoire(navire) # Placement aléatoire du navire sur le plateau

class InterfaceBatailleNavale: # Initialisation de la classe Interfacequi permet de créer l'interface graphique du jeu et de gérer les événements
    def __init__(self, root): # Initialisation de la classe InterfaceBatailleNavale
        self.root = root # Initialisation de la fenêtre principale
        self.root.title("Bataille Navale") # Titre de la fenêtre
        self.root.configure(bg="lightgrey") # Couleur de fond de la fenêtre
        self.partie_terminee = False # Variable qui permet de savoir si la partie est terminée
        
        self.label_tour = tk.Label(root, text="Placement des navires", bg="lightgrey") # Label qui affiche le tour en cours 
        self.label_tour.grid(row=0, column=0, columnspan=20) # Positionnement du label  
        
        self.frame_joueur = tk.Frame(root, bg="#87CEEB") # Création d'un cadre pour la grille du joueur
        self.frame_joueur.grid(row=1, column=0, padx=10, pady=10) # Positionnement du cadre
        
        self.frame_ordinateur = tk.Frame(root, bg="#87CEEB") # Création d'un cadre pour la grille de l'ordinateur
        self.frame_ordinateur.grid(row=1, column=1, padx=10, pady=10) # Positionnement du cadre
        
        self.grille_joueur = [[tk.Button(self.frame_joueur, width=2, height=1, bg="#87CEEB", # Création de la grille du joueur
                             command=lambda x=i, y=j: self.placer_navire_joueur(x, y)) # Appel de la méthode placer_navire_j
                             for j in range(10)] for i in range(10)] # Création de la grille et de sa taille
        
        self.grille_ordinateur = [[tk.Button(self.frame_ordinateur, width=2, height=1, bg="#87CEEB", # Création de la grille de l'ordinateur
                                command=lambda x=i, y=j: self.tirer(x, y)) # Appel de la méthode tirer
                                for j in range(10)] for i in range(10)] # Création de la grille et de sa taille
        
        for i in range(10): # Boucle pour afficher les boutons de la grille du joueur et de l'ordinateur
            for j in range(10): # Boucle pour afficher les boutons de la grille du joueur et de l'ordinateur
                self.grille_joueur[i][j].grid(row=i, column=j) # Positionnement des boutons de la grille du joueur  
                self.grille_ordinateur[i][j].grid(row=i, column=j) # Positionnement des boutons de la grille de l'ordinateur
        
        self.bouton_commencer = tk.Button(root, text="Commencer le jeu", # Création d'un bouton pour commencer le jeu
                                        command=self.commencer_jeu, state="disabled", # Appel de la méthode commencer_jeu
                                        bg="lightgrey") # Couleur du bouton
        self.bouton_commencer.grid(row=2, column=0, columnspan=20, pady=10, sticky="ew") # Positionnement du bouton
        
        self.bouton_recommencer = tk.Button(root, text="Recommencer la partie", # Création d'un bouton pour recommencer la partie
                                          command=self.nouvelle_partie, bg="lightgrey") # Appel de la méthode nouvelle_partie
        self.bouton_recommencer.grid(row=3, column=0, columnspan=20, pady=10, sticky="ew") # Positionnement du bouton
        
        self.orientation = "H" # Initialisation de l'orientation des navires
        self.root.bind("<space>", self.changer_orientation) # Touche espace pour changer l'orientation
        
        self.tour_joueur = True # Initialisation du tour du joueur
        self.nouvelle_partie() # Appel de la méthode nouvelle_partie
    # Méthode qui permet de vérifier si la partie est terminée et d'afficher un message de fin de partie
    def verifier_fin_partie(self): # Méthode qui permet de vérifier si la partie est terminée
        tous_navires_joueur_coules = all(navire.est_coule() for navire in self.joueur.plateau.navires) # Vérification des navires du joueur
        tous_navires_ordi_coules = all(navire.est_coule() for navire in self.ordinateur.plateau.navires) # Vérification des navires de l'ordinateur

        if tous_navires_joueur_coules: # Si tous les navires du joueur sont coulés
            self.partie_terminee = True # La partie est terminée
            self.label_tour.config(text="Vous avez perdu !") # Affichage du message de fin de partie
            messagebox.showinfo("Fin de partie", "Vous avez perdu !") # Affichage de la boîte de dialogue
            self.desactiver_grilles() # Désactivation des grilles
            return True # Retourne True
        elif tous_navires_ordi_coules: # Si tous les navires de l'ordinateur sont coulés
            self.partie_terminee = True # La partie est terminée
            self.label_tour.config(text="Vous avez gagné !") # Affichage du message de fin de partie
            messagebox.showinfo("Fin de partie", "Vous avez gagné !") # Affichage de la boîte de dialogue   
            self.desactiver_grilles()  # Désactivation des grilles
            return True 
        return False 

    def desactiver_grilles(self): # Méthode qui permet de désactiver les grilles
        for i in range(10):
            for j in range(10): 
                self.grille_joueur[i][j].config(state="disabled") # Désactivation des boutons de la grille du joueur
                self.grille_ordinateur[i][j].config(state="disabled") # Désactivation des boutons de la grille de l'ordinateur
    # Méthode qui permet de commencer une nouvelle partie
    def nouvelle_partie(self): 
        self.partie_terminee = False # La partie n'est pas terminée
        self.label_tour.config(text="Placement des navires") # Affichage du message de placement des navires
        self.joueur = Joueur("Joueur") # Initialisation du joueur
        self.ordinateur = Ordinateur() # Initialisation de l'ordinateur
        self.navires_a_placer = [ # Liste des navires à placer
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer", 3),
            ("Destroyer", 3),
            ("Sous-marin", 2),
            ("Sous-marin", 2)
        ]
        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].config(bg="#87CEEB", text="", state="normal") # Initialisation de la grille du joueur
                self.grille_ordinateur[i][j].config(bg="#87CEEB", text="", state="normal") # Initialisation de la grille de l'ordinate
        self.bouton_commencer.config(state="disabled") # Désactivation du bouton commencer
        self.tour_joueur = True # Initialisation du tour du joueur
        self.placer_navires_joueur() # Appel de la méthode placer_navires_joueur
    # Méthode qui permet de changer l'orientation des navires
    def changer_orientation(self, event): # Méthode qui permet de changer l'orientation des navires
        self.orientation = "V" if self.orientation == "H" else "H" # Changement de l'orientation
        if self.navires_a_placer: # Si des navires sont à placer
            nom, taille = self.navires_a_placer[0] # Récupération du nom et de la taille du navire
            self.label_tour.config(text=f"Placez votre {nom} (taille {taille}) - " # Affichage du message de placement
                                      f"Orientation: {'Verticale' if self.orientation == 'V' else 'Horizontale'}") # Affichage de l'orientation
    # Méthode qui permet de placer les navires du joueur
    def placer_navires_joueur(self): 
        if self.navires_a_placer: # Si des navires sont à placer
            nom, taille = self.navires_a_placer[0] # Récupération du nom et de la taille du navire
            self.navire_en_cours = Navire(nom, taille) # Initialisation du navire en cours
            self.label_tour.config(text=f"Placez votre {nom} (taille {taille}) - " # Affichage du message de placement
                                      f"Orientation: {'Horizontale' if self.orientation == 'H' else 'Verticale'}") # Affichage de l'orientation
        else:
            self.label_tour.config(text="Tous les navires sont placés !") # Affichage du message de fin de placement
            self.bouton_commencer.config(state="normal") # Activation du bouton commencer
    def placer_navire_joueur(self, x, y): # Méthode qui permet de placer un navire sur la grille du joueur
        if self.navire_en_cours: # Si un navire est en cours de placement
            if self.orientation == "H": # Si l'orientation est horizontale
                positions = [(x, y + i) for i in range(self.navire_en_cours.taille)] # Création de la liste des positions
            else: # Si l'orientation est verticale
                positions = [(x + i, y) for i in range(self.navire_en_cours.taille)] # Création de la liste des positions
            
            valide = True
            for pos_x, pos_y in positions: # Pour chaque position dans la liste des positions
                if not (0 <= pos_x < 10 and 0 <= pos_y < 10): # Si la position n'est pas dans la grille
                    valide = False # La position n'est pas valide
                    break 
                if self.grille_joueur[pos_x][pos_y].cget('bg') != '#87CEEB': # Si la position n'est pas vide
                    valide = False # La position n'est pas valide
                    break
                for dx in [-1, 0, 1]: # Pour chaque déplacement en x
                    for dy in [-1, 0, 1]: # Pour chaque déplacement en y
                        nx, ny = pos_x + dx, pos_y + dy # Calcul des nouvelles coordonnées
                        if 0 <= nx < 10 and 0 <= ny < 10 and self.grille_joueur[nx][ny].cget('bg') != '#87CEEB': # Si la nouvelle position n'est pas vide
                            valide = False # La position n'est pas valide
                            break
                    if not valide:
                        break
                if not valide:
                    break
            
            if valide:
                for pos in positions:
                    self.grille_joueur[pos[0]][pos[1]].config(bg='darkgrey') # Changement de couleur de la case
                self.joueur.plateau.placer_navire(self.navire_en_cours, positions) # Placement du navire sur la grille du joueur
                self.navires_a_placer.pop(0) # Suppression du navire de la liste des navires à placer
                self.placer_navires_joueur() # Appel de la méthode placer_navires_joueur

    # Méthode qui permet de commencer le jeu
    def commencer_jeu(self):
        self.label_tour.config(text="À vous de jouer !") # Affichage du message de début de partie
        self.bouton_commencer.config(state="disabled") # Désactivation du bouton commencer

    # Méthode qui permet au joueur de tirer sur la grille de l'ordinateur
    def tirer(self, x, y):
        if self.partie_terminee:
            return
        if self.tour_joueur and self.grille_ordinateur[x][y].cget('bg') not in ['red', 'darkblue', 'black']: # Si c'est le tour du joueur et que la case n'est pas déjà touchée
            resultat = self.joueur.tirer(self.ordinateur, x, y)  # Appel de la méthode tirer
            if resultat == "Touché" or resultat == "Coulé": 
                self.grille_ordinateur[x][y].config(bg='red') # Changement de couleur de la case
                if resultat == "Coulé": 
                    navire = self.ordinateur.plateau.get_navire(x, y) # Récupération du navire touché
                    if navire:
                        for pos in navire.positions: # Pour chaque position dans la liste des positions
                            self.grille_ordinateur[pos[0]][pos[1]].config(bg='black') # Changement de couleur de la case
                self.label_tour.config(text=f"{resultat} !") # Affichage du message de tir réussi
                if self.verifier_fin_partie(): # Appel de la méthode verifier_fin_partie
                    return
            else:
                self.grille_ordinateur[x][y].config(bg='darkblue')  # Changement de couleur de la case
                self.label_tour.config(text="Manqué !")  # Affichage du message de tir raté
                self.tour_joueur = False # Changement de tour 
                self.root.after(1000, self.tour_ordinateur) # Appel de la méthode tour_ordinateur

    # Méthode qui permet à l'ordinateur de jouer
    def tour_ordinateur(self): # Méthode qui permet à l'ordinateur de jouer
        if self.partie_terminee: # Si la partie est terminée
            return
        if not self.tour_joueur: # Si ce n'est pas le tour du joueur
            x, y = randint(0, 9), randint(0, 9) # Génération aléatoire des coordonnées x et y
            while self.grille_joueur[x][y].cget('bg') in ['red', 'darkblue', 'black']: # Tant que la case est déjà touchée  
                x, y = randint(0, 9), randint(0, 9)  # Génération aléatoire des coordonnées x et y
            
            resultat = self.ordinateur.tirer(self.joueur, x, y) # Appel de la méthode tirer
            if resultat == "Touché" or resultat == "Coulé": # Si le tir est réussi ou coulé
                self.grille_joueur[x][y].config(bg='red') # Changement de couleur de la case
                if resultat == "Coulé": 
                    navire = self.joueur.plateau.get_navire(x, y) # Récupération du navire touché
                    if navire:
                        for pos in navire.positions: # Pour chaque position dans la liste des positions
                            self.grille_joueur[pos[0]][pos[1]].config(bg='black') # Changement de couleur de la case
                self.label_tour.config(text=f"L'ordinateur a {resultat.lower()} un navire !") # Affichage du message de tir réussi
                
                if self.verifier_fin_partie(): # Appel de la méthode verifier_fin_partie
                    return
                
                if resultat != "Coulé":
                    self.root.after(1000, self.tour_ordinateur) # Appel de la méthode tour_ordinateur
                else:
                    self.tour_joueur = True # Changement de tour
            else:
                self.grille_joueur[x][y].config(bg='darkblue') # Changement de couleur de la case
                self.label_tour.config(text="L'ordinateur a manqué !") # Affichage du message de tir raté
                self.tour_joueur = True # Changement de tour

# Lancement de l'interface graphique    
if __name__ == "__main__":
    root = tk.Tk() # Création de la fenêtre principale
    app = InterfaceBatailleNavale(root) # Création de l'interface graphique
    root.mainloop() # Lancement de la boucle principale