# Modèle — comment écrire un cours dans ce projet

Méthode utilisée pour `grep.md` et `ripgrep.md`, à réutiliser pour chaque outil listé dans `commande.md` (find, awk, sed, jq...).

## Structure d'un module

Chaque outil vit dans son propre dossier sous `textual-search/<outil>/` (ou l'équivalent dans une autre catégorie) :

```
textual-search/<outil>/
├── <outil>.md       # le cours
├── exercices.md      # la pratique
└── data/              # les fichiers utilisés par les deux
```

## 1. Le cours (`<outil>.md`)

- Un titre `# <outil> — cours complet`, puis un paragraphe d'intro : ce que fait l'outil, en une phrase.
- Si l'outil remplace/complète un outil déjà couvert (ex. ripgrep vs grep), commencer par un **tableau de comparaison** — ça ancre le nouvel outil sur ce que l'utilisateur connaît déjà.
- Découper en sections numérotées **par catégorie d'usage**, pas par option isolée : "Options d'affichage", "Options de matching", "Contexte", "Recherche récursive"... Une option seule ne mérite jamais sa propre section.
- Dans chaque section : un tableau `| Option | Effet |`, puis un ou plusieurs blocs ```bash``` d'exemples réels (pas de pseudo-code).
- Un exemple qui produit un résultat non trivial ou surprenant mérite un commentaire `#` expliquant CE résultat (pas ce que fait l'option, déjà dit dans le tableau).
- Terminer par une section "Combinaisons utiles" : des one-liners réalistes qui enchaînent plusieurs options du cours.

## 2. Vérifier l'exhaustivité avant de considérer le cours fini

Ne jamais supposer qu'un cours est complet de mémoire. Comparer contre la sortie réelle de l'outil :

```bash
<outil> --help
```

Trier les options manquantes en deux paniers :
- **Vraiment utiles** → à ajouter, avec exemple testé (ex. pour rg : `--debug`, `--column`, `-0`...)
- **Niche** → citer en une ligne sans exemple, ou ignorer complètement

Demander à l'utilisateur avant d'ajouter un gros lot — ne pas juste tout balancer.

## 3. Les données (`data/`)

- Ne jamais inventer une structure de données abstraite : lister d'abord **tous les noms de fichiers déjà utilisés dans les exemples du cours** (`app.log`, `access.log`, `script.py`...), puis créer exactement ces fichiers.
- Chaque fichier doit être conçu pour qu'une commande précise du cours produise un résultat **propre et non ambigu** : au moins un cas qui matche, un cas qui ne matche pas mais qui ressemble (piège), et si pertinent un cas qui montre la différence entre deux options proches (ex. `version.txt` avec `3.14.15` / `3X14X15` / `3-14-15` pour illustrer `-F`).
- Générer les fichiers par lots thématiques (pas tous d'un coup), et **tester chaque lot immédiatement** avant de passer au suivant.

## 4. Toujours vérifier en exécutant réellement les commandes

Chaque commande du cours et des exercices doit être testée avant validation — ne jamais faire confiance à ce qu'on pense savoir sur un outil. Deux pièges rencontrés en pratique :

- **Un a priori peut être faux ou dépendre de la version** : le smart-case de ripgrep n'était pas le comportement par défaut sur la version installée, contrairement à ce que disent beaucoup de tutoriels. Toujours vérifier avec `--help` ou `--version` plutôt que d'écrire de mémoire.
- **L'environnement du terminal peut masquer le vrai binaire** : dans ce projet, `grep` et `rg` sont redéfinis par des fonctions shell (snapshot Claude Code) qui changent leur comportement par défaut (ex. `-I` caché). Toujours vérifier avec `which -a <outil>` / `type <outil>`, et tester avec le chemin binaire explicite (`/usr/bin/grep`, `/usr/bin/rg`) pour être sûr de documenter le vrai comportement standard.

## 5. Les exercices (`exercices.md`)

- Même découpage en sections que le cours (numéros alignés).
- Un exercice = un énoncé concret pointant vers un fichier de `data/`, un indice replié, une solution repliée (`<details><summary>...</summary>...</details>`), testée avant d'être écrite.
- Rappeler en haut du fichier de se placer dans `data/` avant de commencer (`cd textual-search/<outil>/data`).

## 6. Rythme de travail

Avancer par petits lots validés un par un (ex. "2-3 fichiers de données", puis "une section du cours") plutôt que tout produire d'un coup — permet de corriger la direction tôt plutôt qu'après coup.
