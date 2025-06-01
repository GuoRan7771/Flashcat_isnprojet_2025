import tkinter as tk
import csv
import subprocess
import sys
import math
import os
import json 

# Nombre de mots par session
SESSION_SIZE = 5
STATE_FILE = "state.json" 

class SessionSelecteur(tk.Toplevel):
    """
    Fenêtre permettant de sélectionner une session de révision.

    Cette interface liste toutes les sessions possibles calculées
    à partir d’un fichier CSV de vocabulaire et affiche l’état
    de progression (sessions terminées désactivées).
    """
    def __init__(self, master, csv_path):
        """
        Initialise la fenêtre de sélection de session.

        Args:
            master: Fenêtre principale tkinter.
            csv_path (str): Chemin vers le fichier CSV de mots.
        """
        super().__init__(master)
        self.title("🎯 Choisir une session")
        self.geometry("700x500")
        self.configure(bg="#f0f0f0")
        self.resizable(True, True)
        self.csv_path = csv_path

        # Lecture du nombre total de mots dans le CSV
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                rows = [row for row in csv.reader(f, delimiter=';') if any(cell.strip() for cell in row)]
            total_words = len(rows)
        except:
            total_words = 0

        # Calcul du nombre de sessions nécessaires
        self.levels = max(1, math.ceil(total_words / SESSION_SIZE))
        self.create_ui()

    def is_session_mastered(self,session_num):
        """
        Vérifie si une session a déjà été complétée.

        Args:
            session_num (int): Numéro de la session à vérifier.

        Returns:
            bool: True si la session est marquée comme complétée dans state.json.
        """
        if not os.path.exists(STATE_FILE):
            return False
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                completed_sessions = state.get("session", [])
        except:
            return False
        return session_num in completed_sessions

    def create_ui(self):
        """
        Crée l’interface graphique avec les boutons de sessions
        et une barre de défilement si nécessaire.
        """
        # En-tête de la fenêtre
        tk.Label(
            self,
            text="Sélection de la session",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        ).pack(pady=(15, 10))

        # Conteneur pour Canvas + Scrollbar
        container = tk.Frame(self, bg="#f0f0f0")
        container.pack(fill="both", expand=True, padx=20, pady=(0,10))

        # Canvas pour le scroll
        self.canvas = tk.Canvas(container, bg="#ffffff", highlightthickness=0)
        vsb = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame interne où seront placés les boutons
        grid_frame = tk.Frame(self.canvas, bg="#ffffff")
        self.canvas.create_window((0, 0), window=grid_frame, anchor="nw")

        # Mise à jour de la scrollregion à chaque redimensionnement du frame
        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        grid_frame.bind("<Configure>", on_frame_configure)

        # Binder la molette de la souris pour scroller
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Génération des boutons de sessions en grille
        cols = 6  # Nombre de colonnes
        for i in range(self.levels):
            session_num = i + 1
            row = i // cols
            col = i % cols if row % 2 == 0 else cols - 1 - (i % cols)

            # Désactive le bouton si la session est déjà complétée
            state = "disabled" if self.is_session_mastered(session_num) else "normal"

            btn = tk.Button(
                grid_frame,
                text=f"Session {session_num}",
                width=10,
                height=2,
                font=("Arial", 9, "bold"),
                bg="#ffffff",
                relief="raised",
                bd=1,
                state=state,
                activebackground="#d0e0ff",
                command=lambda n=session_num: self.start_level(n)
            )
            btn.grid(row=row, column=col, padx=6, pady=6)

        # Bouton pour fermer la fenêtre
        tk.Button(
            self,
            text="Fermer",
            command=self.destroy,
            font=("Arial", 10),
            bg="#dddddd",
            relief="raised"
        ).pack(pady=(10, 15))

    def start_level(self, level_num):
        """
        Commence à jouer en notant les infos de session en level_info.txt.
        """
        try:
            # Écriture des informations de session dans level_info.txt
            with open("level_info.txt", "w", encoding="utf-8") as f:
                f.write(f"{self.csv_path}\n{level_num}")
            # Démarrage du script de la session de mots
            subprocess.Popen([sys.executable, "MotFenetre.py"])
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Impossible de démarrer la session:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # on cache la fenêtre principale
    # Exemple : passer le chemin vers votre CSV ici
    selector = SessionSelecteur(root, "votre_fichier.csv")
    selector.mainloop()
