# Flashcat_isnprojet_2025 : Votre assistant personnalisé pour l'apprentissage du vocabulaire

Ce projet est un logiciel conçu pour vous aider à mémoriser du vocabulaire. Vous pouvez importer vos propres listes de mots (par exemple, français-anglais, ou toute autre langue que vous apprenez), puis les étudier et les réviser à l'aide d'un système similaire aux flashcards (cartes mémoire). Il organise également intelligemment votre plan de révision en fonction de vos progrès.

## I. Démarrage rapide

Ce guide vous aidera à installer les dépendances nécessaires et à lancer le programme Flashcat_isnprojet_2025. Nous partons du principe que Python est déjà installé sur votre système (version recommandée : Python 3.6 ou ultérieure).

### 1. Obtenir les fichiers du projet

Vous avez deux manières d'obtenir les fichiers du projet :

**Méthode 1 : Via Git Clone (recommandé si vous êtes familier avec Git)**

1.  **Installer Git** : Si Git n'est pas encore installé sur votre ordinateur, veuillez d'abord le télécharger depuis le site officiel de Git (git-scm.com) et l'installer.
2.  **Ouvrir un terminal/invite de commandes/Git Bash**.
3.  **Clôner le dépôt** : Entrez la commande suivante, en remplaçant `[adresse_du_dépôt]` par l'URL réelle du dépôt Git du projet (par exemple `https://github.com/nomdutilisateur/nomdudepot.git`) :
    ```bash
    git clone [adresse_du_dépôt]
    ```
    Appuyez sur Entrée. Git téléchargera tous les fichiers du projet dans un dossier portant le nom du dépôt (par exemple `Flashcat_isnprojet_2025`) dans votre répertoire actuel.

**Méthode 2 : Télécharger l'archive ZIP**

1.  **Télécharger les fichiers du projet** : Vous devez télécharger l'archive ZIP complète du projet à partir du lien du dépôt GitHub qui vous a été fourni. Sur la page GitHub, il y a généralement un bouton vert "Code", cliquez dessus, puis sélectionnez "Download ZIP" (Télécharger ZIP).
2.  **Décompresser les fichiers** : Une fois le téléchargement terminé, trouvez le fichier ZIP (généralement dans votre dossier "Téléchargements"), faites un clic right dessus et sélectionnez "Extraire tout..." ou "Extract All...". Choisissez un emplacement facile à retrouver pour le dossier décompressé (par exemple, le Bureau ou Documents). Après la décompression, vous obtiendrez un dossier contenant tous les fichiers du projet, dont le nom est généralement `Flashcat_isnprojet_2025-main` ou similaire.

### 2. Installer les dépendances (pip)

Avant de lancer le programme, vous devez installer les bibliothèques Python nécessaires.

1.  **Ouvrir un terminal/invite de commandes** :
    * Windows : Appuyez sur la touche `Win`, tapez `cmd` et ouvrez l'invite de commandes.
    * macOS/Linux : Ouvrez le programme "Terminal".

2.  **Accéder au dossier du projet** :
    Utilisez la commande `cd` pour naviguer jusqu'au dossier du projet que vous venez d'obtenir. Par exemple, si vous avez cloné ou décompressé le projet dans un dossier nommé `Flashcat_isnprojet_2025` sur votre Bureau :
    * Windows : `cd Desktop\Flashcat_isnprojet_2025` (adaptez le chemin selon votre emplacement)
    * macOS/Linux : `cd Desktop/Flashcat_isnprojet_2025` (adaptez le chemin selon votre emplacement)
    Entrez la commande et appuyez sur Entrée.

3.  **Installer Pillow** :
    Flashcat_isnprojet_2025 utilise la bibliothèque Pillow pour le traitement des images (notamment pour les avatars). Installez-la en exécutant la commande suivante dans votre terminal, **dans le dossier du projet** :

    ```bash
    pip install Pillow
    ```

    `tkinter`, `csv`, `json`, `os`, `subprocess`, et `sys` sont des modules intégrés à Python et ne nécessitent pas d'installation supplémentaire.

### 3. Lancer le programme Flashcat_isnprojet_2025

Dans le même terminal ou invite de commandes, assurez-vous d'être toujours dans le bon dossier du projet, puis entrez la commande suivante et appuyez sur Entrée :

```bash
python AppFenetre.py
```

(Sur certains systèmes, si la commande `python` ne fonctionne pas, essayez `python3 AppFenetre.py`)

Si tout se passe bien, vous devriez voir une fenêtre de programme intitulée "Accueil" apparaître.

## IV. Fonctionnalités principales de Flashcat_isnprojet_2025 et étapes d'utilisation

Maintenant que le programme est lancé, voyons comment l'utiliser.

1.  **Présentation de l'interface principale ("Accueil")** :

    * **Réglage** : Configurer le programme, l'action la plus importante étant d'importer votre liste de vocabulaire.
    * **Jouer** : Choisir une session d'étude et commencer à apprendre les mots.
    * **Carte** : Visualiser votre progression globale d'apprentissage.
    * **Quitter** : Fermer le programme.
    * **Avatar et nom d'utilisateur en haut à droite** : Cliquez pour modifier votre nom d'utilisateur et votre avatar.
    * **Jour actuel** : Affiche le jour en cours. Le programme simule les jours pour planifier les révisions.
    * **+1 jour** : Fait avancer manuellement le programme au jour suivant, ce qui affecte les mots à réviser.

2.  **Première utilisation : Configurer la liste de vocabulaire (très important \!)**

    * Cliquez sur le bouton **"Réglage"** sur l'interface principale.
    * Dans la fenêtre "Réglage" qui s'ouvre, cliquez sur le bouton **"Upload CSV" (Téléverser CSV)**.
    * Une boîte de dialogue de sélection de fichier s'ouvrira. Vous devez choisir un fichier de liste de vocabulaire au format CSV.
        * Le projet inclut deux fichiers d'exemple : `ex_Français_English.csv` (vocabulaire français-anglais) et `ex_TJgaokao.csv` (vocabulaire pour un examen spécifique, probablement chinois-anglais). Vous pouvez commencer par essayer avec ces fichiers.
        * Un fichier CSV est un fichier texte simple que vous pouvez ouvrir avec Excel ou un éditeur de texte. Chaque ligne représente un mot, et le mot et sa traduction sont séparés par un point-virgule `;`. Par exemple : `bonjour;hello`.
    * Une fois le fichier CSV sélectionné, son chemin d'accès s'affichera sous le bouton "Upload CSV".
    * **Remarque importante** : Selon la description du projet, après avoir téléversé un nouveau fichier CSV, la progression est automatiquement réinitialisée. Si vous souhaitez simplement utiliser un fichier précédemment téléversé, assurez-vous que le chemin est correct, puis cliquez sur **"Sauvegarder"** et fermez la fenêtre des réglages.

3.  **Personnalisation (optionnel)**

    * Sur l'interface principale "Accueil", cliquez sur l'avatar circulaire en haut à droite ou sur le nom d'utilisateur en dessous (par défaut "Guo").
    * La fenêtre "Profil" s'ouvrira.
    * **Modifier le nom d'utilisateur** : Dans le champ de saisie à côté de "Username:", entrez le nom que vous souhaitez.
    * **Téléverser un avatar** : Cliquez sur le bouton "Upload Avatar" et choisissez une image que vous aimez comme avatar.
    * Une fois les modifications terminées, cliquez sur **"Sauvegarder"**.

4.  **Commencer à apprendre ("Jouer")**

    * Assurez-vous d'avoir téléversé et sauvegardé une liste de vocabulaire CSV dans "Réglage".
    * Cliquez sur le bouton **"Jouer"** sur l'interface principale.
    * Une fenêtre "🎯 Choisir une session" s'ouvrira. Les mots sont divisés en plusieurs "Session" (par default, 5 mots par session). Les sessions déjà terminées apparaîtront en gris et ne seront pas cliquables.
    * Choisissez un bouton de session que vous souhaitez étudier (par exemple "Session 1").
    * Une nouvelle fenêtre d'apprentissage s'ouvrira (titrée par exemple "Session 1"), c'est l'interface pour mémoriser les mots :
        * **Affichage du mot** : Généralement, un mot est affiché en premier (par exemple, en anglais).
        * **Afficher la signification** : Cliquez sur ce bouton pour afficher la traduction du mot (par exemple, en français).
        * **Boutons de feedback** : Après avoir vu la réponse, cliquez en fonction de votre maîtrise :
            * **Je connais** : Indique que vous connaissez déjà ce mot.
            * **Je suis incertain** : Indique que vous avez une vague idée, mais que vous ne le maîtrisez pas complètement.
            * **Je ne connais pas** : Indique que vous ne le connaissez pas du tout ou que vous vous êtes trompé.
        * Le programme enregistrera votre apprentissage en fonction de vos réponses. Les mots mal répondus ou incertains réapparaîtront plus tard pour révision.
        * Une fois tous les mots d'une session terminés, un message s'affichera : "Session terminée avec succès \!". Vous pouvez alors fermer cette fenêtre d'apprentissage.

5.  **Consulter la progression ("Carte")**

    * Cliquez sur le bouton **"Carte"** sur l'interface principale.
    * Une fenêtre s'ouvrira, affichant un graphique et un pourcentage de votre progression globale pour la liste de vocabulaire actuelle. Un point rouge indique votre position actuelle.

6.  **Simuler le passage du temps ("+1 jour")**

    * Les logiciels d'apprentissage utilisent souvent le principe de la "répétition espacée" pour aider à la mémorisation, c'est-à-dire que les mots appris réapparaissent quelques jours plus tard pour être révisés.
    * Cliquez sur le bouton **"+1 jour"** sur l'interface principale, le programme considérera qu'un jour s'est écoulé. Cela mettra à jour l'état de révision des mots. Si vous cliquez dessus après avoir terminé votre session d'aujourd'hui, lorsque vous ouvrirez "Jouer" le lendemain, des mots à réviser pourraient apparaître.

7.  **Réinitialiser la progression de l'apprentissage**

    * Si vous souhaitez recommencer à apprendre une liste de vocabulaire depuis le début, ou si vous changez de liste :
        * Méthode 1 : Dans la fenêtre "Réglage", cliquez sur le bouton **"Initialiser"**. Cela réinitialisera la progression de la liste de vocabulaire actuellement sélectionnée.
        * Méthode 2 : Comme mentionné précédemment, **téléverser un nouveau fichier CSV dans "Réglage" réinitialise automatiquement la progression**.

## V. Description des fichiers (à titre informatif)

Le dossier du projet contient d'autres fichiers que vous n'aurez généralement pas besoin de modifier directement, mais il est bon de savoir à quoi ils servent :

* `profil.json` : Sauvegarde votre nom d'utilisateur et le chemin d'accès à votre image d'avatar.
* `state.json` : Sauvegarde l'état du programme, comme le jour actuel, le chemin du fichier CSV utilisé et les sessions d'étude terminées.
* `level_info.txt` : Enregistre le chemin du fichier CSV en cours d'étude et le numéro de la session sélectionnée ; le programme le gère automatiquement, aucune opération supplémentaire de l'utilisateur n'est requise.
* `ex_Français_English.csv` et `ex_TJgaokao.csv` : Fichiers d'exemples de listes de vocabulaire. Vous pouvez vous référer à leur format pour créer vos propres listes de vocabulaire CSV avec Excel ou un éditeur de texte.

## VI. Remarques importantes

* **Chemins des fichiers** : Essayez de ne pas déplacer le dossier du projet ou les fichiers CSV, sinon le programme pourrait ne pas les retrouver. Si vous les déplacez, vous devrez à nouveau téléverser le fichier CSV dans "Réglage".
* **Fermer le programme** : Une fois votre session d'étude terminée, vous pouvez cliquer sur le bouton "Quitter" de l'interface principale ou simplement fermer la fenêtre.
* **Messages d'erreur** : Si un message d'erreur apparaît pendant l'utilisation (généralement une petite fenêtre), lisez attentivement le message pour voir si vous pouvez en trouver la cause (par exemple, cliquer sur "Jouer" sans avoir sélectionné de fichier CSV).

J'espère que ce tutoriel vous aidera à utiliser Flashcat_isnprojet_2025 sans problème \! C'est un excellent outil d'apprentissage, je vous souhaite de bien apprendre et de voir votre vocabulaire s'enrichir rapidement \!
```