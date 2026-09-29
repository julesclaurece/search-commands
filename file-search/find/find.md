# find — cours complet

`find` parcourt une arborescence de dossiers et teste **chaque fichier rencontré** contre des critères (nom, type, taille, date, permissions...). Quand un fichier correspond, une action s'exécute dessus — par défaut, l'afficher.

## 1. Introduction

Syntaxe de base :

```bash
find [chemin] [critères] [action]
```

- `chemin` : où commencer (par défaut `.`, le dossier courant)
- `critères` : les tests à satisfaire (nom, type, taille...)
- `action` : que faire des fichiers trouvés (par défaut : `-print`, les afficher)

```bash
find project/                     # liste tout, récursivement, sans filtre
find project/ -name "*.py"        # seulement les fichiers dont le nom matche
```

`find` est **récursif par défaut** (comme `rg`, contrairement à `grep`) et descend dans tous les sous-dossiers, sauf indication contraire.

## 2. Recherche par nom

| Critère | Effet |
|---|---|
| `-name MOTIF` | nom de fichier exact ou avec jokers (`*`, `?`), **sensible à la casse** |
| `-iname MOTIF` | comme `-name`, insensible à la casse |
| `-path MOTIF` | matche sur le **chemin complet**, pas juste le nom |
| `-regex MOTIF` | le chemin complet doit matcher une regex (pas juste `-name`, un motif glob) |

```bash
find project/ -name "*.py"
find project/ -iname "readme*"          # README.md, readme.md, Readme.MD...
find project/ -path "*/src/*"           # chemin contenant /src/
find project/ -regex ".*/[a-z]+\.py"    # regex sur le chemin entier
```

**Piège classique** : `-name "*.py"` ne matche que le **nom du fichier**, pas le chemin — `*` ne traverse pas les `/`. Pour filtrer sur un dossier, utiliser `-path`.

## 3. Recherche par type

| Critère | Effet |
|---|---|
| `-type f` | fichiers normaux |
| `-type d` | dossiers |
| `-type l` | liens symboliques |

```bash
find project/ -type d              # seulement les dossiers
find project/ -type f -name "*.log"
```

## 4. Recherche par taille

```bash
find project/ -size +100k     # fichiers de plus de 100 Ko
find project/ -size -1024c    # fichiers de moins de 1024 octets EXACTEMENT
find project/ -size 0         # fichiers exactement vides (0 octet)
```

Unités : `c` (octets), `k` (Ko), `M` (Mo), `G` (Go). `+`/`-` = "plus grand que" / "plus petit que" ; sans signe = taille exacte.

**Piège à connaître** : avec une unité comme `k`/`M`/`G`, `find` arrondit chaque fichier **au bloc supérieur** de cette unité avant de comparer. Un fichier de 69 octets compte donc comme "1k" plein, pas "moins de 1k" — `-size -1k` ne matchera que les fichiers **réellement vides** (0 octet), pas "tout ce qui fait moins de 1024 octets" comme on l'imaginerait naturellement. Pour une comparaison en octets exacts, utiliser `c` (`-size -1024c`).

## 5. Recherche par date

| Critère | Effet |
|---|---|
| `-mtime N` | modifié il y a exactement N×24h |
| `-mtime +N` | modifié il y a plus de N jours |
| `-mtime -N` | modifié il y a moins de N jours |
| `-mmin N` / `+N` / `-N` | pareil, mais en **minutes** |
| `-newer FICHIER` | modifié plus récemment que `FICHIER` |

```bash
find project/ -mtime +7            # non modifiés depuis plus d'une semaine
find project/ -mmin -30            # modifiés dans les 30 dernières minutes
find project/ -newer project/logs/old.log   # plus récents que ce fichier de référence
```

`-atime` (dernier accès) et `-ctime` (dernier changement de métadonnées) existent aussi, avec la même syntaxe.

## 6. Recherche par permissions et propriétaire

```bash
find project/ -perm 777          # permissions EXACTEMENT 777
find project/ -perm -u+x         # au moins le bit exécutable pour le propriétaire (peu importe le reste)
find project/ -user root         # appartenant à l'utilisateur root
find project/ -perm -4000        # bit SUID présent (classique en audit sécurité / CTF)
```

**Différence importante** : `-perm 777` (sans signe) exige une correspondance **exacte** ; `-perm -777` (avec `-`) exige que **tous** ces bits soient présents, même s'il y en a d'autres.

## 7. Profondeur de recherche

```bash
find project/ -maxdepth 1      # seulement le contenu direct, pas les sous-dossiers
find project/ -mindepth 2      # ignore les 1er niveau, ne descend qu'à partir du 2e
```

## 8. Opérateurs logiques

| Opérateur | Effet |
|---|---|
| (rien, implicite) | ET logique entre critères consécutifs |
| `-o` / `-or` | OU logique |
| `-not` / `!` | négation |
| `\( ... \)` | groupement (les parenthèses doivent être échappées ou protégées) |

```bash
find project/ -name "*.py" -o -name "*.md"              # .py OU .md
find project/ -type f -not -name "*.py"                  # fichiers, sauf les .py
find project/ \( -name "*.py" -o -name "*.md" \) -size +0
```

**Piège** : sans parenthèses, `-o` a une portée qui peut surprendre — `find . -name "*.py" -o -name "*.md" -size +0` n'applique `-size +0` qu'au `.md`, pas au `.py`. Toujours grouper avec `\( \)` dès qu'on mélange `-o` et d'autres critères.

## 9. Exécuter une commande sur les résultats (`-exec`)

| Forme | Effet |
|---|---|
| `-exec cmd {} \;` | exécute `cmd` **une fois par fichier trouvé** (`{}` = le chemin du fichier) |
| `-exec cmd {} +` | regroupe tous les fichiers trouvés en **un minimum d'appels** (plus rapide, comme `xargs`) |
| `-ok cmd {} \;` | comme `-exec`, mais demande confirmation avant chaque exécution |

```bash
find project/ -name "*.py" -exec echo "trouvé: {}" \;   # une commande par fichier
find project/ -name "*.py" -exec ls -la {} +              # une seule commande ls avec tous les fichiers en argument
find project/ -name "*.tmp" -exec rm {} \;                 # supprimer chaque fichier trouvé
```

`{} +` est presque toujours préférable à `{} \;` quand la commande le permet (bien moins de processus lancés sur un grand nombre de fichiers).

## 10. Actions d'affichage

| Action | Effet |
|---|---|
| `-print` | affiche le chemin (comportement par défaut) |
| `-print0` | comme `-print`, mais sépare par un octet NUL — pour un pipeline sûr avec `xargs -0` |
| `-ls` | affiche un format détaillé façon `ls -l` |
| `-printf FORMAT` | affichage entièrement personnalisé (façon `printf` du C) |
| `-delete` | supprime directement chaque fichier trouvé — **irréversible**, toujours tester sans `-delete` (juste `-print`) avant |

```bash
find project/ -name "*.py" -print0 | xargs -0 -I{} echo "fichier: {}"
find project/ -maxdepth 1 -type f -printf "%f - %s octets\n"   # %f = nom, %s = taille
```

## 11. Élaguer une partie de l'arborescence (`-prune`)

Exclure un dossier entier de la recherche (plus efficace que `-not -path`, qui filtre après coup, alors que `-prune` empêche même d'y descendre) :

```bash
find project/ -name ".git" -prune -o -print
```

Explication : `-name ".git" -prune` coupe la descente dès qu'on rencontre `.git` ; `-o -print` affiche tout le reste. La forme `A -prune -o B` est un idiome à retenir tel quel.

## 12. Combiner avec d'autres commandes

```bash
find project/ -name "*.log" -print0 | xargs -0 grep -l "error"    # grep uniquement dans les fichiers trouvés
find project/ -type f -exec du -h {} + | sort -rh                  # taille de chaque fichier, triée
```

## 13. Autres critères utiles

| Critère | Effet |
|---|---|
| `-empty` | fichier ou dossier vide |
| `-samefile FICHIER` | même inode qu'un autre fichier (détecte les liens durs) |
| `-links N` | exactement N liens durs |
| `-inum N` | numéro d'inode exact |

```bash
find project/ -empty                        # fichiers ou dossiers vides
find project/ -samefile project/README.md   # autres noms pointant vers le même contenu (lien dur)
find project/ -type f -links 2               # fichiers ayant exactement 2 liens durs (restreint aux fichiers : les dossiers ont presque toujours -links 2 aussi, à cause de l'auto-référence ".")
```

## 14. Combinaisons utiles (one-liners classiques)

```bash
# Trouver les fichiers SUID (classique en audit sécurité / CTF privesc)
find / -perm -4000 -type f 2>/dev/null

# Fichiers de plus de 50 Mo, triés par taille
find / -size +50M -exec du -h {} + 2>/dev/null | sort -rh

# Nettoyer les fichiers temporaires de plus de 7 jours
find /tmp -name "*.tmp" -mtime +7 -delete

# Fichiers modifiés dans la dernière heure (investigation d'incident)
find / -mmin -60 -type f 2>/dev/null

# Chercher du texte uniquement dans les fichiers correspondant à un critère de fichier
find project/ -name "*.py" -exec grep -l "TODO" {} +
```
