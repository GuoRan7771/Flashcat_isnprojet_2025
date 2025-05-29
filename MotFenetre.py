import csv
import json
import tkinter as tk
from tkinter import messagebox
import os

# Constantes
STATE_FILE_TXT = 'level_info.txt'                   # Chemin du CSV et numéro de session
DAILY_REVIEW_LIMIT = None                       # Pas de limite quotidienne
SESSION_SIZE = 5                                # Nombre de nouveaux mots par session
KNOWN_INTERVALS = [1, 2, 4, 7, 15, 30]          # Intervalles de révision pour les mots connus
STATE_FILE= 'state.json' 

class Word:
    def __init__(self, english, french, mastery='NonConnait', times=0, days_since=0):
        self.english = english
        self.french = french
        self.mastery = mastery
        self.times = int(times)
        self.days_since = int(days_since)

    def is_due(self):
        # Détermine si le mot doit être revu
        if self.times == 0:
            return False
        if self.mastery == 'Connait':
            idx = self.times - 1
            threshold = KNOWN_INTERVALS[idx] if idx < len(KNOWN_INTERVALS) else KNOWN_INTERVALS[-1]
        elif self.mastery == 'Incertain':
            idx = self.times - 2
            threshold = KNOWN_INTERVALS[idx] if 0 <= idx < len(KNOWN_INTERVALS) else 1
        else:
            threshold = 1
        return self.days_since >= threshold

    def to_csv_row(self):
        return [self.french, self.english, self.mastery, str(self.times), str(self.days_since)]

class WordBank:
    def __init__(self, words):
        self.words = words
        
    @classmethod
    def load_csv(cls, filename):
        words = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) < 5:
                    row += ['NonConnait', '0', '0']
                french, english, mastery, times, days_since = row
                words.append(Word(english.strip(), french.strip(), mastery.strip(), times, days_since))
        return cls(words)

    def save_csv(self, filename):
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for word in self.words:
                writer.writerow(word.to_csv_row())

    def increment_days(self):
        for w in self.words:
            if w.times > 0:
                w.days_since += 1

    def get_words_for_session(self, session_number):
        start_idx = (session_number - 1) * SESSION_SIZE
        session_words = self.words[start_idx : start_idx + SESSION_SIZE]
        review_candidates = [w for w in self.words if w.is_due()]
        return review_candidates + [w for w in session_words if w.times == 0]

def load_session_info():
    try:
        with open(STATE_FILE_TXT, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            csv_path = lines[0].strip()
            session_number = int(lines[1].strip())
            return csv_path, session_number
    except:
        return 'mots_initialises.csv', 1

def record_session_completion(session_number):
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
    else:
        state = {}

    completed_sessions = set(state.get("session", []))
    completed_sessions.add(session_number)

    state["session"] = sorted(completed_sessions)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        
def increment_state_day():
    
   
    STATE_JSON = 'state.json'
    try:
        if os.path.exists(STATE_JSON):
            with open(STATE_JSON, 'r', encoding='utf-8') as sf:
                data = json.load(sf)
        else:
            data = {}
        current_day = data.get('day', 0)
        data['day'] = current_day + 1
        with open(STATE_JSON, 'w', encoding='utf-8') as sf:
            json.dump(data, sf, indent=2)
    except Exception:
        
        pass


def main():
    CSV_FILE, session_number = load_session_info()
    wb = WordBank.load_csv(CSV_FILE)
    wb.increment_days()
    today_words = wb.get_words_for_session(session_number)
    current_list = today_words.copy()
    retry_list = []
    # Liste pour enregistrer premier clic non-connait/incertain
    first_feedback = []  # tuples (Word, 'Incertain'/'NonConnait')

    # Fenêtre Tkinter
    root = tk.Tk()
    root.title(f"Session {session_number}")

    eng_var, fr_var, prog_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
    label_eng = tk.Label(root, textvariable=eng_var, font=("Arial", 22))
    label_fr  = tk.Label(root, textvariable=fr_var,  font=("Arial", 14))
    label_prog= tk.Label(root, textvariable=prog_var,font=("Arial", 10))
    btn_show   = tk.Button(root, text="Afficher la signification", width=25, height=2)
    btn_known  = tk.Button(root, text="Je connais", width=25, height=2)
    btn_fuzzy  = tk.Button(root, text="Je suis incertain", width=25, height=2)
    btn_unknown= tk.Button(root, text="Je ne connais pas", width=25, height=2)

    label_eng.grid(row=0, column=0, columnspan=3, pady=10)
    label_fr.grid(row=1, column=0, columnspan=3, pady=5)
    btn_known.grid(row=3, column=0, padx=5, pady=10)
    btn_fuzzy.grid(row=3, column=1, padx=5, pady=10)
    btn_unknown.grid(row=3, column=2, padx=5, pady=10)
    label_prog.grid(row=4, column=0, columnspan=3, pady=5)

    idx = 0

    def show_word(i):
        nonlocal idx
        w = current_list[i]
        eng_var.set(w.english)
        fr_var.set("")
        btn_show.grid(row=2, column=0, columnspan=3, pady=5)
        btn_show.config(state=tk.NORMAL)
        idx = i
        prog_var.set(f"Mot {i+1}/{len(current_list)}")

    def reveal():
        fr_var.set(current_list[idx].french)
        btn_show.config(state=tk.DISABLED)

    def feedback(response):
        w = current_list[idx]
        # Enregistrer premier non-connait/incertain
        if response != 'Je connais' and all(w is not fb[0] for fb in first_feedback):
            val = 'Incertain' if response == 'Je suis incertain' else 'NonConnait'
            first_feedback.append((w, val))
        # Mettre à jour état pour session
        if response == 'Je connais':
            w.mastery = 'Connait'
            w.times += 1
            w.days_since = 0
        elif response == 'Je suis incertain':
            w.mastery = 'Incertain'
            retry_list.append(w)
        else:
            w.mastery = 'NonConnait'
            retry_list.append(w)
        next_word()

    def next_word():
        nonlocal idx
        if idx + 1 < len(current_list):
            show_word(idx + 1)
        else:
            if retry_list:
                messagebox.showinfo("Renforcement", "Répétons les mots non maîtrisés !")
                current_list.clear()
                current_list.extend(retry_list)
                retry_list.clear()
                show_word(0)
            else:
                record_session_completion(session_number)
                increment_state_day()
                messagebox.showinfo("Fini", "Session terminée avec succès !")
                root.destroy()

    btn_show.config(command=reveal)
    btn_known.config(command=lambda: feedback("Je connais"))
    btn_fuzzy.config(command=lambda: feedback("Je suis incertain"))
    btn_unknown.config(command=lambda: feedback("Je ne connais pas"))

    if current_list:
        show_word(0)
    else:
        messagebox.showinfo("Info", "Aucun mot pour cette session.")
        increment_state_day()
        root.destroy()

    root.mainloop()
    # Avant de sauvegarder, restaurer mastery des premiers feedback
    for w, val in first_feedback:
        w.mastery = val
    wb.save_csv(CSV_FILE)

if __name__ == '__main__':
    main()

 
