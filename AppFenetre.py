import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import csv
import json
import os
from SessionSelecteur import SessionSelecteur
import subprocess
import sys
#N'oubilez pip install Pillow

PROFIL_FILE = "profil.json"
STATE_FILE = "state.json"


def make_circle_image(img, size=(100, 100)):
    """
    Redimensionne une image et applique un masque circulaire.

    Parameters:
        img (PIL.Image.Image): Image PIL à transformer.
        size (tuple[int, int], optional): Taille finale (largeur, hauteur). Par défaut (100, 100).

    Returns:
        PIL.Image.Image: Image avec masque circulaire appliqué en alpha.
    """
    img = img.resize(size, Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, *size), fill=255)
    img.putalpha(mask)
    return img


def calculate_progress(csv_path):
    """
    Calcule le pourcentage de progrès dans un fichier CSV.

    Le progrès est défini comme le ratio entre le nombre de lignes marquées "Connait"
    et le nombre total de lignes (hors entête).

    Parameters:
        csv_path (str): Chemin vers le fichier CSV.

    Returns:
        float: Progrès calculé entre 0.0 et 1.0. 0.0 si erreur ou fichier vide.
    """
    if not csv_path:
        return 0.0
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            rows = list(reader)
            total = len(rows) - 1 if rows else 0
            count = sum(1 for row in rows[1:] if len(row) >= 3 and row[2].strip() == 'Connait')
            return count / total if total else 0.0
    except Exception:
        return 0.0


# -----------------------------------------------------------------------------
#  Root window – Accueil
# -----------------------------------------------------------------------------

class Accueil(tk.Tk):
    def __init__(self):
        """
        Initialise la fenêtre principale Accueil de l'application.
        Charge l'état (jour + chemin CSV) et le profil utilisateur.
        Initialise les boutons et l'affichage de l'avatar et du jour courant.
        """
        super().__init__()
        self.title("Accueil")                    # Titre de la fenêtre
        self.geometry("500x400")                 # Taille initiale

        # Chargement du state (day + csv_path)
        state = self.load_state()
        self.reglage = {"csv_path": state.get("csv_path", "")}
        self.profil = self.load_profil()

        # Références aux fenêtres secondaires
        self._reglage_win = None
        self._profil_win = None
        self.jouer_windows = []

        # Boutons principaux
        btn_kwargs = {"width": 10, "height": 2}
        tk.Button(self, text="Réglage", command=self.open_reglage, **btn_kwargs).place(x=55, y=45)
        tk.Button(self, text="Jouer", command=self.open_jouer, **btn_kwargs).place(x=210, y=160)
        tk.Button(self, text="Carte", command=self.open_carte, **btn_kwargs).place(x=210, y=230)
        tk.Button(self, text="Quitter", command=self.destroy, **btn_kwargs).place(x=210, y=300)

        # Affichage de l’avatar et du nom d’utilisateur
        frame = tk.Frame(self, width=60, height=80)
        frame.place(x=370, y=30)
        self.avatar_canvas = tk.Canvas(frame, width=60, height=60, highlightthickness=0)
        self.avatar_canvas.pack()
        self.avatar_canvas.create_oval(0, 0, 60, 60, fill="white", outline="")
        self.avatar_canvas.bind("<Button-1>", self.open_profil)

        self.profil_label = tk.Label(frame, text=self.profil["username"], cursor="hand2")
        self.profil_label.pack(pady=(0,5))
        self.profil_label.bind("<Button-1>", self.open_profil)

        # Chargement de l’avatar si existant
        if self.profil.get("avatar_path") and os.path.exists(self.profil["avatar_path"]):
            try:
                img = make_circle_image(Image.open(self.profil["avatar_path"]), size=(60, 60))
                self.set_avatar(img)
            except Exception:
                pass

        # Affichage du “jour actuel” avec possibilité d’incrément
        self.day_var = tk.StringVar()
        self.update_day_label()
        self.bind("<FocusIn>", lambda e: self.update_day_label())
        tk.Label(self, textvariable=self.day_var, font=("Arial", 12)).place(x=200, y=45)
        tk.Button(self, text="+1 jour", command=self.increment_day, width=8).place(x=215, y=80)

    
    def load_state(self):
        """
        Charge l'état courant depuis le fichier JSON STATE_FILE.

        Returns:
            dict: Dictionnaire avec les clés "day" et "csv_path" si existants, sinon dict vide.
        """
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
   
    def load_profil(self):
        """
        Charge les données du profil utilisateur depuis PROFIL_FILE.

        Returns:
            dict: Dictionnaire contenant "username" (str), "avatar_img" (PIL.Image ou None),
                  et "avatar_path" (str ou None).
        """
        if os.path.exists(PROFIL_FILE):
            with open(PROFIL_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                "username": data.get("username", "Guo"),
                "avatar_img": None,
                "avatar_path": data.get("avatar_path")
            }
        else:
            return {
                "username": "Guo",
                "avatar_img": None,
                "avatar_path": None
            }

    def save_profil(self):
        """
        Sauvegarde le profil utilisateur (nom et chemin avatar) dans le fichier JSON PROFIL_FILE.
        """
        data = {
            "username": self.profil.get("username"),
            "avatar_path": self.profil.get("avatar_path")
        }
        with open(PROFIL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def open_reglage(self):
        """
        Ouvre la fenêtre de réglage si elle n'existe pas, sinon la met au premier plan.
        """
        if self._reglage_win and self._reglage_win.winfo_exists():
            self._reglage_win.lift(); return
        self._reglage_win = ReglageWindow(self)

    def open_profil(self, *_):
        """
        Ouvre la fenêtre de profil utilisateur si elle n'existe pas, sinon la met au premier plan.

        Parameters:
            *_ (tuple): Arguments d'événement ignorés.
        """
        if self._profil_win and self._profil_win.winfo_exists():
            self._profil_win.lift(); return
        self._profil_win = ProfilWindow(self)

    def open_jouer(self):
        """
        Ouvre la fenêtre de sélection de session si un fichier CSV est chargé,
        sinon affiche un avertissement.
        """
        if not self.reglage["csv_path"]:
            messagebox.showwarning("Avertissement", "Veuillez d'abord importer un fichier CSV dans Réglage.")
            return
        try:
            SessionSelecteur(self, self.reglage["csv_path"])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture de la sélection des niveaux:\n{e}")

    def open_carte(self):
        """
        Ouvre la fenêtre de carte avec affichage du progrès calculé à partir du CSV.
        """
        path = self.reglage.get("csv_path", "")
        progress = calculate_progress(path)
        CarteWindow(self, progress=progress)

    def set_avatar(self, pil_img):
        """
        Met à jour l'avatar utilisateur affiché dans l'interface.

        Parameters:
            pil_img (PIL.Image.Image): Image PIL de l'avatar à afficher.
        """
        self.profil["avatar_img"] = pil_img
        thumb = pil_img.resize((60, 60), Image.LANCZOS)
        self._thumb = ImageTk.PhotoImage(thumb)
        self.avatar_canvas.delete("all")
        self.avatar_canvas.create_image(30, 30, image=self._thumb)

    def broadcast_refresh(self):
        """
        Met à jour l'affichage du nom utilisateur et rafraîchit les fenêtres de jeu ouvertes.
        """
        self.profil_label.config(text=self.profil["username"])
        for w in list(self.jouer_windows):
            if w.winfo_exists():
                w.update_stats()
            else:
                self.jouer_windows.remove(w)

    def get_current_day(self):
        """
        Récupère le jour courant depuis le fichier STATE_FILE.

        Returns:
            int: Jour courant (par défaut 1 si erreur).
        """
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("day", 1)
        except:
            return 1

    def update_day_label(self):
        """
        Met à jour l'étiquette affichant le jour courant dans l'interface.
        """
        self.day_var.set(f"Jour actuel : {self.get_current_day()}")

    def increment_day(self):
        """
        Incrémente le jour courant dans STATE_FILE et met à jour les données du CSV
        en fonction du nouveau jour. Met à jour l'affichage du jour courant.
        """
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except:
            state = {"day": 1, "csv_path": self.reglage.get("csv_path", "")}
        state["day"] = state.get("day", 1) + 1
        # Préserve csv_path
        if "csv_path" not in state:
            state["csv_path"] = self.reglage.get("csv_path", "")
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        # Mise à jour des données du CSV pour le jour
        path = self.reglage.get("csv_path", "")
        if path:
            try:
                rows = []
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f, delimiter=';')
                    for row in reader:
                        if len(row) < 5:
                            row += ['NonConnait', '0', '0']
                        if int(row[3]) > 0:
                            row[4] = str(int(row[4]) + 1)
                        rows.append(row)
                with open(path, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerows(rows)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de mettre à jour les jours : {e}")
        self.update_day_label()

# -----------------------------------------------------------------------------
#  ReglageWindow
# -----------------------------------------------------------------------------

class ReglageWindow(tk.Toplevel):
    def __init__(self, master):
        """
        Initialise la fenêtre de réglage.

        Parameters:
            master (Accueil): Fenêtre parente Accueil.
        """
        super().__init__(master); self.master=master; self.title("Réglage")
        self.geometry("300x400")

        # Frame pour le bouton "Initialiser"
        init_frame = tk.Frame(self)
        init_frame.pack(pady=(15, 5))  
        btn_init = tk.Button(init_frame, text="Initialiser", width=18, height=2, command=self.run_initialiser)
        btn_init.pack()

        # CSV upload
        row = tk.Frame(self)
        row.pack(pady=15)
        btn_upload = tk.Button(row, text="Upload CSV", width=18, height=2, command=self.upload_csv)
        btn_upload.pack()

        # CSV path
        self.csv_path = tk.StringVar(value=master.reglage["csv_path"])
        path_label = tk.Label(self, textvariable=self.csv_path, wraplength=180, justify="center", fg="blue")
        path_label.pack(pady=(0, 15))

        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        btn_save = tk.Button(btn_frame, text="Sauvegarder", width=18, height=2, command=self.save)
        btn_close = tk.Button(btn_frame, text="Fermer", width=18, height=2, command=self.destroy)
        btn_save.grid(row=0, column=0, padx=10)
        btn_close.grid(row=1, column=0, padx=10, pady=20)

    def run_initialiser(self):
        """
        Lance un script externe d'initialisation (initialiser.py).
        """
        try:
            subprocess.Popen([sys.executable, "InitialisationCSV.py"])
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Échec de l'initialisation : {e}")

    def upload_csv(self):
        """
        Ouvre un dialogue pour sélectionner un fichier CSV et met à jour le chemin dans la fenêtre principale.
        """
        p = filedialog.askopenfilename(parent=self, title="Choisissez CSV", filetypes=[("CSV", "*.csv")])
        if p:
            self.csv_path.set(p)
            self.master.reglage["csv_path"] = p
            self.lift()
            


    def save(self):
        """
        Sauvegarde le fichier CSV actuellement sélectionné.
        """
        # Met à jour le chemin CSV en mémoire
        self.master.reglage.update({"csv_path": self.csv_path.get()})
        self.run_initialiser()  # Lance l'initialisation après le chargement du CSV
        # Sauvegarde dans le state.json
        try:
            state = {}
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    state = json.load(f)
            state["csv_path"] = self.csv_path.get()
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
        self.master.broadcast_refresh()
        messagebox.showinfo("Réglage","Modifications sauvegardées")

# -----------------------------------------------------------------------------
#  ProfilWindow
# -----------------------------------------------------------------------------

class ProfilWindow(tk.Toplevel):
    def __init__(self, master):
        """
        Initialise la fenêtre de profil utilisateur.

        Parameters:
            master (Accueil): Fenêtre parente Accueil.
        """
        super().__init__(master)
        self.master = master
        self.title("Profil")
        self.configure(padx=20, pady=20)

        data = master.profil

        # Frame
        center_frame = tk.Frame(self)
        center_frame.pack(expand=True)

        # Header
        self.av_can = tk.Canvas(center_frame, width=100, height=100, highlightthickness=0)
        self.av_can.pack(pady=(5, 0))
        self.av_can.create_oval(0, 0, 100, 100, fill="#eee", outline="")

        if data["avatar_img"]:
            self._av = ImageTk.PhotoImage(data["avatar_img"])
            self.av_can.create_image(50, 50, image=self._av)

        # Upload button
        tk.Button(center_frame, text="Upload Avatar", command=self.upload_avatar).pack(pady=(0, 30))

        # Username label+input
        user_frame = tk.Frame(center_frame)
        user_frame.pack(pady=(0, 10))
        tk.Label(user_frame, text="Username:").pack(side="left", padx=(0, 5))
        self.user = tk.StringVar(value=data["username"])
        tk.Entry(user_frame, textvariable=self.user, width=20).pack(side="left")

        # ---- Load mastery stats from CSV ----
        csv_path = self.master.reglage.get("csv_path", "")
        known = unknown = 0
        if csv_path and os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=';')
                    for row in reader:
                        if len(row) >= 3:
                            if row[2].strip() == "Connait":
                                known += 1
                            else:
                                unknown += 1
            except Exception:
                pass

        # Stats
        stats_frame = tk.Frame(self)
        stats_frame.pack(pady=10)

        fixed_width = 5

        lf1 = tk.LabelFrame(stats_frame, text="Maîtrises", labelanchor='n')
        lf1.grid(row=1, column=0, padx=10)
        label1 = tk.Label(lf1, text=str(known), font=("Arial", 12), width=fixed_width, anchor='center')
        label1.pack(padx=15, pady=10)

        lf2 = tk.LabelFrame(stats_frame, text="Non appris", labelanchor='n')
        lf2.grid(row=1, column=1, padx=10)
        label2 = tk.Label(lf2, text=str(unknown), font=("Arial", 12), width=fixed_width, anchor='center')
        label2.pack(padx=15, pady=10)

        # Save & Close Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Sauvegarder", width=15, height=2, command=self.save).pack(side="left", padx=10, pady=(0,20))
        tk.Button(btn_frame, text="Fermer", width=15, height=2, command=self.destroy).pack(side="left", padx=10, pady=(0,20))

    def upload_avatar(self):
        """
        Ouvre un dialogue pour sélectionner une image d'avatar,
        la transforme en image circulaire et l'affiche.
        """
        p = filedialog.askopenfilename(title="Choisissez image", filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
        if not p:
            return
        img = make_circle_image(Image.open(p), size=(100, 100))
        self._av = ImageTk.PhotoImage(img)
        self.av_can.delete("all")
        self.av_can.create_image(50, 50, image=self._av)
        self.master.set_avatar(img)
        self.master.profil["avatar_path"] = p
        self.master.save_profil()

    def save(self):
        """
        Sauvegarde le nom d'utilisateur et le chemin d'avatar dans le profil principal,
        puis met à jour l'affichage et ferme la fenêtre.
        """
        self.master.profil.update({"username": self.user.get()})
        self.master.save_profil()
        self.master.broadcast_refresh()
        messagebox.showinfo("Profil", "Modifications sauvegardées")

# -----------------------------------------------------------------------------
#  CarteWindow 
# -----------------------------------------------------------------------------

class CarteWindow(tk.Toplevel):
    """
        Fenêtre secondaire affichant une carte de progression.

        Affiche une image de carte sur laquelle une ligne rouge indique le trajet,
        et un point rouge avec le texte "Vous êtes ici !" indique la position actuelle
        en fonction de la progression fournie.

        Attributs :
            progress (float) : Valeur entre 0.0 et 1.0 représentant le pourcentage de progression.

        Paramètres :
            master (tk.Tk ou tk.Toplevel) : La fenêtre parente.
            progress (float) : Valeur entre 0.0 et 1.0 indiquant la progression sur la carte.
    """
    def __init__(self, master=None, progress=0.0):
        super().__init__(master)
        self.title("Carte")
        self.progress=progress
        img=Image.open("carte.jpg")

        ow,oh=img.size
        sw,sh=self.winfo_screenwidth()*0.9,self.winfo_screenheight()*0.9
        if ow>sw or oh>sh:
            img=img.resize((int(ow*min(sw/ow,sh/oh)),int(oh*min(sw/ow,sh/oh))),Image.LANCZOS)
        w,h=img.size
        self.geometry(f"{w}x{h+80}")

        carte=tk.Canvas(self,width=w,height=h)
        carte.pack()
        self._bg=ImageTk.PhotoImage(img)
        carte.create_image(0,0,anchor="nw",image=self._bg)
        carte.create_line(291,135,348,378,fill="red",width=2)
        mx=291+(348-291)*(1-progress);my=135+(378-135)*(1-progress)
        carte.create_oval(mx-6,my-6,mx+6,my+6,fill="red",outline="")
        carte.create_text(mx,my-10,text="Vous êtes ici !",font=("Arial",12,"bold"),fill="red")

        tk.Label(self,text=f"Progrès: {int(progress*100)} %").pack(pady=(5,0))
        tk.Button(self,text="Fermer",command=self.destroy).pack(pady=5)


if __name__ == "__main__":
    Accueil().mainloop()
