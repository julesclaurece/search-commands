# ripgrep (rg) — cours complet

`ripgrep` (commande `rg`) est un remplaçant moderne de `grep`, écrit en Rust. Mêmes idées de base (chercher un motif dans des fichiers), mais avec des choix par défaut différents et plus intelligents pour un usage "dans un projet de code".

## 1. Introduction — en quoi rg diffère de grep

| Comportement | grep | ripgrep |
|---|---|---|
| Recherche dans un dossier | il faut `-r` | **récursif par défaut** |
| Fichiers ignorés | aucun | ignore automatiquement `.gitignore`, `.git/`, fichiers binaires |
| Casse | sensible par défaut | **sensible par défaut aussi** — le smart-case existe (`-S`) mais n'est pas activé automatiquement |
| Numéros de ligne | il faut `-n` | affichés par défaut (dans un terminal) |
| Vitesse | correcte | très rapide (parallélisme, filtre les fichiers ignorés avant de les lire) |

Syntaxe de base :

```bash
rg MOTIF
```

Sans préciser de fichier ni de dossier, `rg` cherche récursivement depuis le dossier courant.

```bash
rg "TODO"
```

Cherche "TODO" dans tous les fichiers du dossier courant et ses sous-dossiers, **en respectant `.gitignore`** (donc pas dans `node_modules/`, `.git/`, etc. si ces règles existent).

## 2. Options d'affichage

| Option | Effet |
|---|---|
| `-n` / `-N` (`--no-line-number`) | force/désactive les numéros de ligne (déjà actifs par défaut dans un terminal) |
| `-c` (`--count`) | nombre de lignes correspondantes par fichier |
| `--count-matches` | nombre total d'occurrences (peut différer de `-c` si plusieurs matches par ligne) |
| `-l` (`--files-with-matches`) | seulement les noms de fichiers avec au moins un match |
| `--files-without-match` | seulement les fichiers SANS match |
| `-o` (`--only-matching`) | affiche uniquement la partie qui matche |
| `-H` | force l'affichage du nom de fichier même s'il n'y en a qu'un |
| `--color=always/never/auto` | contrôle la coloration |

```bash
rg -c "error" app.log
rg -l "error" .
rg -o "user_[0-9]+"
```

## 3. Options de matching

| Option | Effet |
|---|---|
| `-i` (`--ignore-case`) | force l'insensibilité à la casse |
| `-s` (`--case-sensitive`) | force la sensibilité à la casse (désactive le smart-case) |
| `-S` (`--smart-case`) | explicite le comportement par défaut |
| `-v` (`--invert-match`) | inverse le match |
| `-w` (`--word-regexp`) | mot entier |
| `-x` (`--line-regexp`) | ligne entière |
| `-F` (`--fixed-strings`) | motif littéral, pas une regex |

```bash
rg -i "error"          # ERROR, Error, error...
rg -S "error"           # smart-case : motif tout en minuscules → insensible à la casse
rg -S "Error"           # smart-case : motif avec majuscule → redevient sensible à la casse
rg -w "cat"
rg -F "3.14.15"
```

**Piège à connaître** : par défaut, `rg "error"` est **sensible** à la casse, exactement comme `grep "error"` — il ne matche pas "ERROR" ou "Error". C'est `-S` (smart-case) qui change ce comportement, pas le défaut de `rg`. Beaucoup de tutoriels présentent le smart-case comme le comportement par défaut de ripgrep : ce n'est plus le cas sur les versions récentes (testé ici en 15.2.0) — mieux vaut vérifier avec `rg --help` sur ta propre version.

## 4. Contexte

Identique à grep :

| Option | Effet |
|---|---|
| `-A N` | N lignes après |
| `-B N` | N lignes avant |
| `-C N` | N lignes avant et après |

```bash
rg -A 2 "Exception" app.log
rg -C 3 "connexion refusée" server.log
```

## 5. Plusieurs motifs

| Option | Effet |
|---|---|
| `-e MOTIF` | motif supplémentaire (répétable) |
| `-f FICHIER` | motifs lus depuis un fichier |

```bash
rg -e "error" -e "warning"
rg -f motifs.txt
```

## 6. Filtrage de fichiers (le point fort de rg)

C'est ici que `rg` dépasse largement `grep` : pas besoin d'outils externes (`find | xargs grep`), tout est intégré.

| Option | Effet |
|---|---|
| `-t TYPE` (`--type`) | ne cherche que dans un type de fichier connu (ex. `py`, `js`, `md`) |
| `-T TYPE` (`--type-not`) | exclut un type de fichier |
| `--type-list` | liste tous les types reconnus |
| `-g GLOB` (`--glob`) | inclut/exclut par motif glob (`!` pour exclure) |
| `--iglob` | comme `-g` mais insensible à la casse |
| `--hidden` | inclut les fichiers/dossiers cachés (`.env`, `.github/`...) |
| `--no-ignore` | ignore les règles `.gitignore` (cherche partout) |
| `-u`, `-uu`, `-uuu` | réduit progressivement le filtrage (`-uu` = comme `--no-ignore --hidden`, `-uuu` = comme `grep -r` complet) |
| `--max-depth N` | limite la profondeur de récursion |

```bash
# sans filtre, project/ contient 2 TODO : src/app.py ET README.md
rg "TODO"

rg -t py "TODO"                 # ne garde que src/app.py (README.md n'est pas un .py)
rg -T md "TODO"                 # ne garde que src/app.py (README.md est exclu, lui, explicitement)
rg -g "*.log" "error"           # équivalent à --include, à lancer dans data/ (app.log, server.log)
rg -g "!vendor/*" "password"    # équivalent à --exclude, à lancer dans data/project/ : trouve notes.txt, exclut vendor/lib.py
rg --hidden "API_KEY"           # project/.env est normalement invisible ; --hidden le fait apparaître
rg -uu "TODO"                   # trouve aussi node_modules/lib.js et debug.log, ignorés par défaut par .gitignore
```

## 7. Remplacement (`-r`) — que grep n'a pas

`grep` ne modifie jamais le texte affiché ; `rg` peut réécrire l'affichage à la volée (pas le fichier lui-même) :

```bash
rg "error" -r "ERROR"
# affiche les lignes avec "error" remplacé par "ERROR" dans la sortie (le fichier n'est PAS modifié)

rg "user_(\d+)" -r 'id:$1'
# utilise un groupe capturé ($1) dans le remplacement
```

Pour modifier réellement les fichiers, il faut combiner avec `sed` ou l'option `--passthru` en pipeline — ce sera vu dans la section `sed`.

## 8. Contrôle du volume et scripting

| Option | Effet |
|---|---|
| `-m N` (`--max-count`) | s'arrête après N matches par fichier |
| `-q` (`--quiet`) | pas de sortie, seulement le code de sortie |
| `--max-filesize TAILLE` | ignore les fichiers plus gros que TAILLE (ex. `1M`) |

```bash
rg -m 1 "ERROR" app.log
rg -q "FAILED" test_results.txt && echo "trouvé"
```

## 9. Recherche multiligne

`grep` ne sait chercher un motif qui s'étend sur plusieurs lignes qu'avec des astuces (`-z`, PCRE limité). `rg` a une vraie option dédiée :

| Option | Effet |
|---|---|
| `-U` (`--multiline`) | permet à `.` et aux ancres de franchir les sauts de ligne |
| `--multiline-dotall` | `.` matche aussi le saut de ligne lui-même (à utiliser avec `-U`) |

```bash
rg -U "Exception[\s\S]*?at com.example.App.main"
# capture depuis "Exception" jusqu'à cette ligne précise, même sur plusieurs lignes
```

## 10. Regex : moteur Rust vs PCRE2

Par défaut, `rg` utilise le moteur **regex de Rust** — proche d'ERE, mais **sans lookahead/lookbehind/backreferences** (par choix de performance). Pour ces fonctionnalités, il faut explicitement demander PCRE2 :

| Option | Effet |
|---|---|
| (par défaut) | moteur Rust : rapide, garanties de performance, pas de lookaround/backreferences |
| `-P` (`--pcre2`) | bascule vers PCRE2 : lookahead, lookbehind, backreferences, comme `grep -P` |

```bash
rg '(?<=id=)\d+'          # ÉCHOUE : lookbehind non supporté par le moteur par défaut
rg -P '(?<=id=)\d+'       # fonctionne : PCRE2 activé
```

Classes de caractères POSIX, `\d`, `\w`, `\s`, ancres `^$`, `\b` : tous disponibles nativement, sans `-P`.

## 11. Autres commandes utiles

| Option | Effet |
|---|---|
| `--files` | liste les fichiers que `rg` regarderait (sans chercher de motif) — pratique pour vérifier ce qui est ignoré |
| `--stats` | affiche des statistiques de recherche (fichiers scannés, matches, temps) |
| `--json` | sortie structurée en JSON (pour scripts/outils) |
| `-z` (`--search-zip`) | cherche aussi dans les fichiers compressés (`.gz`, `.bz2`...) |
| `--sort path` | trie les résultats par chemin (par défaut l'ordre n'est pas garanti à cause du parallélisme) |

```bash
rg --files                # utile pour déboguer un .gitignore trop agressif
rg --files -g "*.py"      # liste juste les .py trouvés
rg --stats "TODO"
```

## 12. Options avancées supplémentaires

| Option | Effet |
|---|---|
| `-a` (`--text`) | traite les fichiers binaires comme du texte (équivalent `grep -a`) |
| `-L` (`--follow`) | suit les liens symboliques (ignorés par défaut) |
| `--column` | affiche aussi le numéro de colonne du match, pas seulement la ligne |
| `--debug` | explique quels fichiers sont cherchés/ignorés et pourquoi — le meilleur outil pour déboguer un `.gitignore` trop agressif |
| `-0` (`--null-data`) | sépare les résultats par un octet NUL au lieu d'un saut de ligne, pour un pipeline sûr avec `xargs -0` (noms de fichiers avec espaces) |
| `--type-add` | étend un type existant ou en crée un nouveau (ex. regrouper `.css`/`.js` sous un type `web`) |
| `--type-clear` | vide la liste de motifs d'un type avant de le redéfinir avec `--type-add` |
| `--passthru` | affiche TOUTES les lignes du fichier, pas seulement celles qui matchent — les matches sont juste mis en évidence |

```bash
rg -a "secret" binaire.dat

rg --column "TODO" script.py
# script.py:12:7:    # TODO: gérer le cas d'erreur si le fichier est vide
# (ligne 12, colonne 7)

rg -l "TODO" -t py -0 . | xargs -0 -I{} echo "fichier: {}"

rg --type-add 'web:*.{css,js}' -t web "width" .

rg --passthru "TODO" script.py
# affiche tout le fichier, avec TODO mis en évidence au lieu de n'afficher que sa ligne

rg --debug "TODO" . 2>&1 | head -5
# journal détaillé : config lue, dossier de départ, fichiers ignorés et pourquoi
```

## 13. Combinaisons utiles

```bash
# TODO dans le code source, en excluant les tests, triés par chemin
rg -t py "TODO" -g "!test_*" --sort path

# Toutes les erreurs/warnings, insensible à la casse, seulement dans les .log
rg -i "(error|warning)" -g "*.log"

# Compter les occurrences par fichier
rg -c "import requests" -t py

# Chercher même dans les fichiers ignorés par .gitignore (utile pour un audit sécurité)
rg -uu "password|secret|api_key"
```
