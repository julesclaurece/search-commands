# sed — cours complet

`sed` (Stream EDitor) lit un flux de texte **ligne par ligne** et applique dessus des commandes d'édition — substitution, suppression, insertion — puis affiche le résultat. Contrairement à `awk`, il ne pense pas en "champs", mais en **lignes entières** manipulées par des commandes très courtes.

## 1. Introduction

Syntaxe de base :

```bash
sed 'commande' fichier
```

La commande la plus utilisée est la substitution :

```bash
sed 's/motif/remplacement/' app.log
```

`s/.../.../ ` = **s**ubstitute : cherche `motif` (une regex) sur chaque ligne, et remplace la **première** occurrence trouvée par `remplacement`. Le résultat est affiché ; **le fichier n'est pas modifié** (sauf avec `-i`, vu en section 8).

```bash
sed 's/error/ERROR/' app.log
```

## 2. Substitution et ses flags

| Flag (après le 3e `/`) | Effet |
|---|---|
| (aucun) | remplace seulement la 1re occurrence par ligne |
| `g` | remplace **toutes** les occurrences de la ligne |
| `N` (un nombre) | remplace seulement la N-ième occurrence |
| `Ng` | remplace à partir de la N-ième occurrence, jusqu'à la fin de la ligne |
| `i` ou `I` | insensible à la casse |
| `p` | affiche la ligne si une substitution a eu lieu (utile avec `-n`) |

```bash
sed 's/o/0/g' app.log            # toutes les occurrences de "o"
sed 's/o/0/2' app.log            # seulement la 2e occurrence
sed 's/error/ERROR/gI' app.log   # insensible à la casse : error, Error, ERROR
```

## 3. Adresses — cibler certaines lignes

Une commande peut être limitée à certaines lignes en préfixant une **adresse** :

| Adresse | Cible |
|---|---|
| `N` | la ligne numéro N |
| `N,M` | les lignes N à M |
| `$` | la dernière ligne |
| `/regex/` | toute ligne qui matche la regex |
| `/regex1/,/regex2/` | de la première ligne qui matche `regex1` jusqu'à la première qui matche `regex2` (inclus) |
| `adresse!` | négation — toutes les lignes SAUF celle(s) ciblée(s) |

```bash
sed '3s/o/0/' app.log                    # seulement sur la ligne 3
sed '2,4s/o/0/' app.log                  # sur les lignes 2 à 4
sed '$s/.*/DERNIERE: &/' app.log         # sur la dernière ligne seulement (& = ce qui a matché)
sed '/Exception/,/^$/p' -n app.log       # du "Exception" jusqu'à la ligne vide suivante
sed '2!d' app.log                        # supprime tout SAUF la ligne 2
```

## 4. Affichage sélectif avec -n et p

Par défaut, `sed` affiche **toutes** les lignes (modifiées ou non). L'option `-n` désactive cet affichage automatique ; combinée à la commande `p` (print), elle permet de n'afficher QUE certaines lignes — un peu comme `grep`, mais avec toute la puissance des adresses de `sed`.

```bash
sed -n '/error/p' app.log        # équivalent à grep "error" app.log
sed -n '2,4p' app.log            # affiche seulement les lignes 2 à 4
sed -n '$p' app.log              # affiche seulement la dernière ligne
```

## 5. Suppression de lignes

La commande `d` supprime les lignes ciblées par une adresse (sans adresse, elle supprimerait tout).

```bash
sed '/^#/d' config.conf          # supprime les lignes de commentaire
sed '/^$/d' config.conf          # supprime les lignes vides
sed '2,3d' app.log               # supprime les lignes 2 et 3
```

## 6. Insertion, ajout, remplacement de lignes

| Commande | Effet |
|---|---|
| `a\texte` (ou `a texte` en GNU sed) | ajoute `texte` **après** la ligne ciblée |
| `i\texte` | insère `texte` **avant** la ligne ciblée |
| `c\texte` | **remplace** la ligne ciblée entière par `texte` |

```bash
sed '2a\--- fin de section ---' app.log
sed '1i\=== DEBUT DU RAPPORT ===' app.log
sed '/FAILED/c\LIGNE SUPPRIMÉE POUR CONFIDENTIALITÉ' test_results.txt
```

## 7. Groupes de capture et backreferences

Comme en regex partout ailleurs : on capture une partie du motif entre parenthèses, et on la réutilise dans le remplacement avec `\1`, `\2`...

```bash
# BRE (par défaut) : parenthèses échappées
sed 's/\([a-z]*\),\([a-z]*\)/\2,\1/' employees.csv

# ERE (-E ou -r) : parenthèses nature, plus lisible
sed -E 's/([a-z]+),([a-z]+)/\2,\1/' employees.csv
```

Sur une ligne `alice,martin`, les deux inversent en `martin,alice`.

**Piège identique à grep** : sans `-E`, `(`, `)`, `+`, `?`, `|` doivent être échappés (`\(`, `\)`...) pour avoir un sens spécial — c'est le mode BRE par défaut.

## 8. Modification sur place (`-i`)

Par défaut, `sed` n'affiche que le résultat sans toucher au fichier. `-i` réécrit le fichier directement — **attention, irréversible sans backup**.

```bash
sed -i 's/error/ERROR/g' app.log          # modifie app.log directement, aucune sauvegarde
sed -i.bak 's/error/ERROR/g' app.log      # modifie app.log, mais garde une copie dans app.log.bak
```

**Toujours tester sans `-i` d'abord** pour vérifier le résultat, puis ajouter `-i` (ou `-i.bak` pour garder un filet de sécurité) une fois sûr.

## 9. Regex étendue vs basique (BRE vs ERE)

Comme `grep`, `sed` utilise par défaut le mode **BRE**. `-E` (ou `-r` sur certains systèmes) passe en **ERE** :

```bash
sed 's/cat\|dog/animal/' pets.txt      # BRE : alternance échappée
sed -E 's/cat|dog/animal/' pets.txt    # ERE : plus lisible
```

## 10. Plusieurs commandes en une fois

| Méthode | Syntaxe |
|---|---|
| `;` | sépare plusieurs commandes dans le même script |
| `-e` (répétable) | une commande supplémentaire par `-e` |
| `-f script.sed` | lit les commandes depuis un fichier |

```bash
sed 's/error/ERROR/g; s/warning/WARNING/g' app.log
sed -e 's/error/ERROR/g' -e 's/warning/WARNING/g' app.log
sed -f script.sed app.log
```

## 11. L'espace de travail (pattern space) et l'espace de retenue (hold space)

C'est la partie la plus avancée de `sed`, et ce qui le rend capable de traitements multi-lignes. Chaque ligne lue va dans le **pattern space** (l'espace de travail courant) ; le **hold space** est une mémoire tampon séparée, vide au départ, où l'on peut mettre de côté du contenu pour le réutiliser plus tard.

| Commande | Effet |
|---|---|
| `h` | copie le pattern space **vers** le hold space (écrase) |
| `H` | ajoute le pattern space **à la suite** du hold space |
| `g` | copie le hold space **vers** le pattern space (écrase) |
| `G` | ajoute le hold space **à la suite** du pattern space |
| `x` | échange pattern space et hold space |

```bash
# Inverser l'ordre des lignes d'un fichier (comme `tac`)
sed -n '1!G;h;$p' app.log

# Doubler chaque ligne (ajoute une ligne vide après chaque ligne)
sed 'G' app.log
```

Ces deux one-liners sont des classiques : ils illustrent bien pourquoi `sed` est parfois utilisé pour des transformations qu'on penserait réservées à un vrai langage.

## 12. Autres commandes utiles

| Commande | Effet |
|---|---|
| `q` | arrête le traitement immédiatement (comme `head`) |
| `q N` | arrête et sort avec le code de sortie `N` |
| `n` | passe à la ligne suivante en gardant le flux de commandes |
| `N` | ajoute la ligne suivante au pattern space (fusionne 2 lignes) |
| `y/abc/xyz/` | translittère caractère par caractère (comme `tr`) |
| `=` | affiche le numéro de la ligne courante |

```bash
sed '3q' app.log              # affiche les 3 premières lignes puis s'arrête, comme head -n3
sed 'y/abc/ABC/' file.txt     # remplace chaque a->A, b->B, c->C
sed -n '=' app.log            # numérote chaque ligne (sans l'afficher elle-même)
sed 'N;s/\n/ /' app.log       # fusionne les lignes 2 par 2, séparées par un espace
```

## 13. Séparateur alternatif

Quand le motif ou le remplacement contient déjà des `/`, changer le séparateur de `s///` évite de tout échapper :

```bash
sed 's/\/var\/log\//\/tmp\//' chemins.txt   # illisible
sed 's|/var/log/|/tmp/|' chemins.txt         # même résultat, bien plus lisible
```

N'importe quel caractère peut servir de séparateur (`s|...|...|`, `s#...#...#`...), tant qu'il est utilisé de façon cohérente sur les 3 positions.

## 14. Combinaisons utiles (one-liners classiques)

```bash
# Supprimer les lignes vides ET les commentaires d'un fichier de config
sed '/^#/d; /^$/d' config.conf

# Extraire le contenu entre deux motifs (sans les motifs eux-mêmes)
sed -n '/START/,/END/{/START/d; /END/d; p}' rapport.txt

# Supprimer les doublons consécutifs (comme `uniq`, en pur sed)
sed '$!N; /^\(.*\)\n\1$/!P; D' doublons.txt

# Remplacer plusieurs motifs différents en une seule commande
sed -e 's/error/ERROR/g' -e 's/warning/WARNING/g' -e 's/info/INFO/gI' app.log

# Modifier un fichier sur place en gardant une sauvegarde, seulement si le motif est présent
grep -q "error" app.log && sed -i.bak 's/error/ERROR/g' app.log
```
