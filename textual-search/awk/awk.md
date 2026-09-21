# awk — cours complet

`awk` n'est pas juste un outil de recherche comme `grep` : c'est un vrai petit langage de traitement de texte, pensé pour lire un fichier **ligne par ligne** (chaque ligne = un "enregistrement"), découper chaque ligne en **champs** (colonnes), et exécuter une action à chaque fois qu'un motif correspond.

## 1. Introduction — le modèle enregistrement/champ

Syntaxe de base :

```bash
awk 'motif { action }' fichier
```

- Chaque ligne lue est un **enregistrement**, stocké dans `$0`.
- Elle est automatiquement découpée en **champs** séparés par des espaces/tabulations par défaut : `$1`, `$2`, `$3`... et `$NF` pour le dernier champ.
- Si `motif` est vrai pour la ligne, `action` s'exécute. Sans `action`, la ligne est affichée telle quelle. Sans `motif`, l'action s'exécute sur **toutes** les lignes.

```bash
awk '{print $1}' access.log
# affiche seulement la première colonne de chaque ligne

awk '/error/' app.log
# équivalent à grep "error" app.log : pas d'action -> affiche la ligne entière si le motif matche
```

## 2. Sélection et affichage de champs

| Élément | Signifie |
|---|---|
| `$0` | la ligne entière |
| `$1`, `$2`... | le 1er, 2e... champ |
| `$NF` | le dernier champ |
| `$(NF-1)` | l'avant-dernier champ |
| `NF` | le nombre de champs de la ligne courante |
| `-F SEP` | change le séparateur de champs (par défaut : espaces/tabs) |

```bash
awk '{print $1, $4}' access.log
awk '{print $NF}' access.log          # dernier champ (ex: taille de la réponse)
awk -F, '{print $2}' employees.csv    # champs séparés par des virgules
```

## 3. Motifs (conditions)

| Motif | Effet |
|---|---|
| `/regex/` | vrai si `$0` matche la regex |
| `$1 == "valeur"` | comparaison exacte sur un champ |
| `$4 > 400` | comparaison numérique |
| `cond1 && cond2` | ET logique |
| `cond1 \|\| cond2` | OU logique |
| `NR==2,NR==4` | plage de lignes (par numéro) |
| `/debut/,/fin/` | plage de lignes (entre deux motifs, inclus) |

```bash
awk '$4 >= 400 {print $1, $4}' access.log     # codes HTTP d'erreur
awk -F, '$3 == "paris" {print $2}' employees.csv
awk 'NR==2,NR==4' access.log                   # lignes 2 à 4 seulement
awk '/Exception/,/^$/' app.log                 # de la ligne "Exception" jusqu'à la ligne vide suivante
```

## 4. BEGIN et END

Deux blocs spéciaux exécutés respectivement **avant** de lire le fichier et **après** l'avoir fini — parfaits pour l'initialisation et les totaux.

```bash
awk 'BEGIN{print "=== Rapport ==="} {print $1} END{print "Total lignes:", NR}' access.log
```

## 5. Variables intégrées

| Variable | Contient |
|---|---|
| `NR` | numéro de l'enregistrement (ligne) courant, cumulé sur tous les fichiers |
| `FNR` | numéro de ligne, remis à zéro à chaque nouveau fichier |
| `NF` | nombre de champs de la ligne courante |
| `FS` | séparateur de champs en entrée (par défaut : espace) |
| `OFS` | séparateur de champs en sortie pour `print` (par défaut : espace) |
| `RS` | séparateur d'enregistrement en entrée (par défaut : `\n`) |
| `ORS` | séparateur d'enregistrement en sortie (par défaut : `\n`) |
| `FILENAME` | nom du fichier en cours de lecture |

```bash
awk 'BEGIN{OFS="-"} {print $1, $2}' access.log
# recolle $1 et $2 avec un "-" au lieu d'un espace
```

## 6. Opérateurs et expressions

```bash
awk '{print $4 + 1}' access.log          # arithmétique (code HTTP + 1, juste pour l'exemple)
awk '{print $1 " -> " $3}' access.log    # concaténation de chaînes (juste les coller, pas d'opérateur +)
awk 'BEGIN{print (5 > 3 ? "oui" : "non")}'   # opérateur ternaire
```

Les comparaisons (`==`, `!=`, `<`, `>`, `<=`, `>=`) fonctionnent aussi bien sur des nombres que des chaînes selon le contexte ; `&&`, `||`, `!` pour la logique.

## 7. Structures de contrôle

```bash
awk '{ if ($4 >= 500) print $1, "erreur serveur"; else if ($4 >= 400) print $1, "erreur client"; else print $1, "ok" }' access.log

awk '{ i=1; while (i <= NF) { print $i; i++ } }' access.log

awk '{ for (i=1; i<=NF; i++) print $i }' access.log   # équivalent for du while ci-dessus

awk '/error/{next} {print}' app.log     # next : passe à la ligne suivante sans exécuter le reste
awk 'NR==3{exit} {print}' access.log    # exit : arrête tout le traitement
```

## 8. Tableaux associatifs

Le vrai point fort d'awk pour l'agrégation : des tableaux indexés par une **chaîne** (pas juste des nombres).

```bash
awk -F, '{count[$3]++} END{for (ville in count) print ville, count[ville]}' employees.csv
# compte le nombre d'employés par ville

awk -F, '{total[$3] += $5} END{for (v in total) print v, total[v]}' employees.csv
# somme un montant par catégorie

awk 'BEGIN{a["x"]=1; a["y"]=2; delete a["x"]; for (k in a) print k, a[k]}'
```

**Attention** : l'ordre de `for (clé in tableau)` n'est **pas garanti**. Si tu as besoin d'un ordre précis, trie après coup (avec `sort` en pipeline, ou `asort`/`asorti` en gawk).

## 9. Fonctions intégrées

| Fonction | Effet |
|---|---|
| `length(s)` | longueur d'une chaîne (ou de `$0` si pas d'argument) |
| `substr(s, début, longueur)` | sous-chaîne |
| `split(s, arr, sep)` | découpe `s` selon `sep` dans le tableau `arr`, retourne le nombre d'éléments |
| `sub(regex, remplacement, cible)` | remplace la **première** occurrence |
| `gsub(regex, remplacement, cible)` | remplace **toutes** les occurrences |
| `match(s, regex)` | cherche `regex` dans `s`, remplit `RSTART`/`RLENGTH` |
| `sprintf(format, ...)` | formate une chaîne sans l'afficher (comme `printf` mais retourne le résultat) |
| `toupper(s)` / `tolower(s)` | change la casse |
| `index(s, sous-chaîne)` | position de la sous-chaîne (0 si absente) |

```bash
awk '{gsub(/error/, "ERROR"); print}' app.log
awk 'BEGIN{n=split("a:b:c", arr, ":"); for(i=1;i<=n;i++) print arr[i]}'
awk '{match($0, /[0-9]+/); print substr($0, RSTART, RLENGTH)}' access.log
```

## 10. Fonctions définies par l'utilisateur

```bash
awk -F, '
function bonus(salaire) {
    return salaire * 0.1
}
{ print $2, bonus($5) }
' employees.csv
```

## 11. Formatage de sortie avec printf

`print` sépare juste les valeurs par `OFS` ; `printf` donne un contrôle total du format (comme en C).

```bash
awk -F, '{printf "%-10s %5d ans - %s\n", $2, $4, $3}' employees.csv
# %-10s : chaîne alignée à gauche sur 10 caractères
# %5d   : nombre aligné à droite sur 5 caractères
```

## 12. Travailler avec plusieurs fichiers

`awk` peut lire plusieurs fichiers à la suite, et surtout **combiner leurs données** grâce à l'astuce `NR==FNR`. `departments.csv` (`id,département`) contient une information absente d'`employees.csv` :

```bash
awk -F, 'NR==FNR{dept[$1]=$2; next} {print $2, $3, dept[$1]}' departments.csv employees.csv
```

Explication : `NR==FNR` n'est vrai que pendant la lecture du **premier** fichier (`NR` cumulé = `FNR` du fichier courant seulement au tout début). On en profite pour remplir un tableau `dept` indexé par identifiant, puis `next` passe à la ligne suivante sans exécuter le second bloc. Une fois passé au deuxième fichier, `NR != FNR`, donc c'est le second bloc qui s'exécute — et il peut consulter le tableau rempli avec le premier fichier. C'est la façon idiomatique de faire une **jointure** entre deux fichiers en awk.

## 13. Options avancées supplémentaires

| Option / variable | Effet |
|---|---|
| `-v var=valeur` | injecte une variable dans le programme awk depuis le shell, sans la coder en dur |
| `-f script.awk` | exécute un programme awk depuis un fichier plutôt qu'en ligne de commande (pour les scripts longs) |
| `--csv` (gawk) | parseur CSV natif : gère correctement les champs entre guillemets contenant des virgules, contrairement à `-F,` |
| `ENVIRON["VAR"]` | accède à une variable d'environnement depuis le programme |

```bash
awk -F, -v seuil=30 '$4 > seuil {print $1, $2}' employees.csv
# seuil vient du shell, pas codé en dur dans le programme

MYVAR=hello awk 'BEGIN{print ENVIRON["MYVAR"]}'
```

**Piège classique avec `-F,`** : un CSV réel peut avoir des champs entre guillemets contenant eux-mêmes des virgules (ex. `"hello, world"`). `-F,` les casse en champs supplémentaires ; `--csv` les respecte :

```bash
# fichier: id,name,note / 1,alice,"hello, world"
awk -F, '{print NF, $3}' quoted.csv
# 4 "hello   <- cassé : la virgule dans les guillemets a créé un champ en trop

awk --csv '{print NF, $3}' quoted.csv
# 3 hello, world   <- correct
```

Pour un vrai fichier CSV (pas juste "du texte séparé par des virgules"), préférer `--csv` à `-F,` dès que des guillemets sont possibles.

## 14. Combinaisons utiles (one-liners classiques)

```bash
# Compter les occurrences de chaque code HTTP
awk '{print $4}' access.log | sort | uniq -c

# Somme et moyenne d'une colonne numérique
awk -F, '{sum += $5; n++} END{print "total:", sum, "moyenne:", sum/n}' employees.csv

# Lignes dont un champ dépasse un seuil, triées par ce champ (awk + sort)
awk -F, '$5 > 3000 {print $5, $2}' employees.csv | sort -rn

# Supprimer les doublons sur un champ précis (garde la 1ère occurrence)
awk -F, '!seen[$1]++' employees.csv

# Extraire une colonne et la reformater proprement
awk -F, '{printf "%s (%s)\n", $2, $3}' employees.csv
```
