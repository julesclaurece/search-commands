# grep — cours complet

`grep` (Global Regular Expression Print) cherche des lignes correspondant à un motif dans un ou plusieurs fichiers (ou sur l'entrée standard) et les affiche.

## 1. Introduction

Syntaxe de base :

```bash
grep MOTIF FICHIER
```

Exemple :

```bash
grep "error" app.log
```

Affiche toutes les lignes de `app.log` contenant "error".

**Code de sortie** (essentiel pour l'utiliser en script) :
- `0` — au moins une ligne trouvée
- `1` — aucune ligne trouvée
- `2` — erreur (fichier inexistant, option invalide...)

```bash
grep -q "error" app.log && echo "il y a des erreurs"
```

`-q` (quiet) supprime l'affichage, seul le code de sortie est utilisé.

## 2. Options d'affichage

| Option | Effet |
|---|---|
| `-n` | affiche le numéro de ligne |
| `-c` | affiche seulement le nombre de lignes correspondantes |
| `-l` | affiche seulement les noms de fichiers contenant au moins un match |
| `-L` | affiche seulement les noms de fichiers ne contenant **aucun** match |
| `-o` | affiche uniquement la partie de la ligne qui correspond au motif (pas toute la ligne) |
| `-H` | force l'affichage du nom de fichier (utile avec un seul fichier) |
| `-h` | supprime l'affichage du nom de fichier (utile avec plusieurs fichiers) |
| `--color` | colore la partie correspondante |

```bash
grep -n "TODO" script.py
# 12:# TODO: gérer le cas d'erreur

grep -c "error" app.log
# 3

grep -l "error" *.log
# app.log
# server.log

grep -o "user_[0-9]\+" access.log
# user_42
# user_17
```

## 3. Options de matching

| Option | Effet |
|---|---|
| `-i` | insensible à la casse |
| `-v` | inverse le match (affiche les lignes qui NE contiennent PAS le motif) |
| `-w` | le motif doit correspondre à un mot entier (équivalent à l'entourer de `\b...\b`) |
| `-x` | le motif doit correspondre à la ligne entière |
| `-F` | traite le motif comme une chaîne littérale, pas une regex (plus rapide, utile si le motif contient des caractères spéciaux comme `.` ou `[`) |

```bash
grep -i "error" app.log        # trouve "Error", "ERROR", "error"...
grep -v "^#" config.conf       # affiche tout sauf les lignes de commentaire
grep -w "cat" file.txt         # matche "cat" mais pas "category" ou "concatenate"
grep -x "done" status.txt      # matche seulement une ligne qui contient EXACTEMENT "done"
grep -F "3.14.15" version.txt  # "." est traité littéralement, pas comme "n'importe quel caractère"
```

## 4. Contexte : afficher les lignes autour du match

| Option | Effet |
|---|---|
| `-A N` | affiche aussi les N lignes **après** (After) le match |
| `-B N` | affiche aussi les N lignes **avant** (Before) le match |
| `-C N` | affiche N lignes avant et après (Context) |

```bash
grep -A 2 "Exception" app.log
# affiche la ligne "Exception" + les 2 lignes suivantes (souvent la stack trace)

grep -C 3 "connexion refusée" server.log
# affiche 3 lignes avant et après chaque occurrence
```

Très utile pour explorer un log sans devoir l'ouvrir en entier.

## 5. Plusieurs motifs

| Option | Effet |
|---|---|
| `-e MOTIF` | ajoute un motif (répétable pour chercher plusieurs motifs en une commande) |
| `-f FICHIER` | lit les motifs depuis un fichier (un motif par ligne) |

```bash
grep -e "error" -e "warning" app.log
# équivalent à grep -E "error|warning" app.log

grep -f motifs.txt app.log
# cherche chaque ligne de motifs.txt comme motif dans app.log
```

## 6. Recherche récursive

| Option | Effet |
|---|---|
| `-r` / `-R` | recherche récursivement dans un dossier (`-R` suit aussi les liens symboliques) |
| `--include=MOTIF` | ne cherche que dans les fichiers dont le nom correspond au motif (glob) |
| `--exclude=MOTIF` | exclut les fichiers correspondant au motif |
| `--exclude-dir=MOTIF` | exclut des dossiers entiers (ex. `.git`, `node_modules`) |

```bash
grep -rn "TODO" src/
grep -rn "TODO" --include="*.py" src/
grep -rn "password" --exclude-dir=".git" .
```

## 7. Contrôle du volume et scripting

| Option | Effet |
|---|---|
| `-m N` | s'arrête après N lignes trouvées (par fichier) |
| `-q` | quiet, pas de sortie, seulement le code de sortie |
| `-s` | supprime les messages d'erreur (ex. fichier inexistant) |

```bash
grep -m 1 "ERROR" app.log
# s'arrête dès la première erreur trouvée, utile sur un très gros fichier

if grep -q "FAILED" test_results.txt; then
    echo "Des tests ont échoué"
    exit 1
fi
```

## 8. Fichiers binaires et séparateurs spéciaux

| Option | Effet |
|---|---|
| `-a` | traite un fichier binaire comme du texte (force la recherche) |
| `-I` | ignore les fichiers binaires (comportement souvent implicite) |
| `-z` | utilise le caractère NUL comme séparateur d'enregistrement au lieu de `\n` — permet de traiter tout un fichier comme "une ligne", utile pour du multiline avec `-P` |

```bash
grep -a "secret" binaire.dat
grep -rIn "TODO" .              # ignore les .png, .so, etc. dans la recherche récursive
```

## 9. Regex : BRE, ERE et PCRE

`grep` supporte plusieurs "dialectes" de regex :

- **BRE** (Basic Regular Expression, par défaut) — `\(`, `\)`, `\+`, `\?`, `\|` doivent être échappés pour avoir un sens spécial
- **ERE** (Extended, avec `-E`, alias `egrep`) — `(`, `)`, `+`, `?`, `|` ont directement un sens spécial, pas besoin de les échapper
- **PCRE** (Perl-Compatible, avec `-P`) — le dialecte le plus riche (lookahead, lookbehind, groupes nommés...)

```bash
grep '\(cat\|dog\)' pets.txt          # BRE : alternance échappée
grep -E '(cat|dog)' pets.txt          # ERE : plus lisible
grep -P '(?<=user=)\w+' access.log    # PCRE : lookbehind, capture ce qui suit "user="
```

**Classes de caractères POSIX** (portables entre BRE/ERE) :

```bash
grep -E '[[:digit:]]+' file.txt   # équivalent à [0-9]+
grep -E '[[:alpha:]]+' file.txt   # lettres
grep -E '[[:space:]]' file.txt    # espaces, tabulations
```

**Ancres** :

```bash
grep '^Error' app.log     # lignes qui COMMENCENT par "Error"
grep 'done$' app.log      # lignes qui SE TERMINENT par "done"
grep '^$' app.log         # lignes vides
```

**Limite de mot `\b`** :

```bash
grep '\bcat\b' file.txt   # équivalent à grep -w 'cat' file.txt
```

**PCRE avancé** (`-P`) :

```bash
grep -P '(?<=id=)\d+' data.txt       # lookbehind : capture le nombre après "id="
grep -P '\d+(?=px)' style.css        # lookahead : capture le nombre avant "px"
grep -oP 'user=\K\w+' access.log     # \K : "oublie" ce qui précède dans le match affiché
```

## 10. Combinaisons utiles (one-liners)

```bash
# Chercher "error" ou "warning", insensible à la casse, avec numéro de ligne, récursivement, dans les .log seulement
grep -rniE --include="*.log" '(error|warning)' .

# Compter les occurrences de chaque type d'erreur HTTP dans un log d'accès
grep -oE 'HTTP/[0-9.]+" [0-9]{3}' access.log | sort | uniq -c

# Trouver les fichiers Python contenant "TODO" mais pas encore résolus (exclut "TODO: done")
grep -rl "TODO" --include="*.py" . | xargs grep -v "TODO: done"

# Extraire toutes les adresses email d'un fichier
grep -oE '[[:alnum:].+_-]+@[[:alnum:].-]+\.[[:alpha:]]{2,}' contacts.txt
```
