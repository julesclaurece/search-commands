# Exercices find

Ces exercices utilisent l'arborescence du dossier [`data/`](data/). Avant de commencer, place-toi dedans :

```bash
cd file-search/find/data
```

Pour chaque exercice : un énoncé, un indice, puis la solution repliée (clique pour l'afficher).

## 1. Introduction

**1.1** — Liste tous les fichiers `.py` de `project/`, récursivement.

<details><summary>Solution</summary>

```bash
find project/ -name "*.py"
```
</details>

## 2. Recherche par nom

**2.1** — Trouve `README.md`, peu importe la casse du nom.

<details><summary>Solution</summary>

```bash
find project/ -iname "readme*"
```
</details>

**2.2** — Trouve tous les fichiers dont le **chemin** contient `/src/` (pas juste le nom).

<details><summary>Solution</summary>

```bash
find project/ -path "*/src/*"
```
</details>

## 3. Recherche par type

**3.1** — Liste uniquement les dossiers de `project/`.

<details><summary>Solution</summary>

```bash
find project/ -type d
```
</details>

**3.2** — Liste uniquement les fichiers `.log`.

<details><summary>Solution</summary>

```bash
find project/ -type f -name "*.log"
```
</details>

## 4. Recherche par taille

**4.1** — Trouve les fichiers de plus de 100 Ko.

<details><summary>Solution</summary>

```bash
find project/ -size +100k
```
</details>

**4.2** — Trouve les fichiers réellement vides (0 octet).

<details><summary>Indice</summary>Deux façons d'y arriver : `-size 0` ou `-empty`.</details>
<details><summary>Solution</summary>

```bash
find project/ -size 0
```
</details>

## 5. Recherche par date

**5.1** — Trouve les fichiers modifiés il y a plus de 7 jours.

<details><summary>Solution</summary>

```bash
find project/ -mtime +7
```
</details>

**5.2** — Trouve les fichiers plus récents que `project/logs/old.log`.

<details><summary>Solution</summary>

```bash
find project/ -newer project/logs/old.log -type f
```
</details>

## 6. Permissions et propriétaire

**6.1** — Trouve les fichiers ayant exactement les permissions 777.

<details><summary>Solution</summary>

```bash
find project/ -perm 777
```
</details>

**6.2** — Trouve les fichiers avec le bit SUID actif (classique en audit sécurité).

<details><summary>Solution</summary>

```bash
find project/ -perm -4000
```
</details>

## 7. Profondeur

**7.1** — Liste uniquement le contenu direct de `project/`, sans descendre dans les sous-dossiers.

<details><summary>Solution</summary>

```bash
find project/ -maxdepth 1
```
</details>

## 8. Opérateurs logiques

**8.1** — Trouve les fichiers `.py` OU `.md`.

<details><summary>Solution</summary>

```bash
find project/ -name "*.py" -o -name "*.md"
```
</details>

**8.2** — Trouve les fichiers qui ne sont PAS des `.py`.

<details><summary>Solution</summary>

```bash
find project/ -type f -not -name "*.py"
```
</details>

## 9. Exécuter une commande (-exec)

**9.1** — Affiche le détail (`ls -la`) de chaque fichier `.log` trouvé, en un minimum d'appels à `ls`.

<details><summary>Indice</summary>`{} +` plutôt que `{} \;`.</details>
<details><summary>Solution</summary>

```bash
find project/ -name "*.log" -exec ls -la {} +
```
</details>

## 10. Actions d'affichage

**10.1** — Affiche chaque fichier `.py` sous la forme "nom - taille en octets".

<details><summary>Solution</summary>

```bash
find project/ -name "*.py" -printf "%f - %s octets\n"
```
</details>

## 11. Élaguer l'arborescence

**11.1** — Liste tout `project/` en excluant complètement le contenu de `.git/`.

<details><summary>Solution</summary>

```bash
find project/ -name ".git" -prune -o -print
```
</details>

## 12. Combiner avec d'autres commandes

**12.1** — Cherche le mot "old" uniquement dans les fichiers `.log` trouvés par `find`.

<details><summary>Solution</summary>

```bash
find project/ -name "*.log" -print0 | xargs -0 grep -l "old"
```
</details>

## 13. Autres critères

**13.1** — Trouve les fichiers ou dossiers vides.

<details><summary>Solution</summary>

```bash
find project/ -empty
```
</details>

**13.2** — Trouve tous les noms de fichiers qui pointent vers le même contenu que `project/README.md` (lien dur).

<details><summary>Solution</summary>

```bash
find project/ -samefile project/README.md
```
</details>

## 14. Combinaisons

**14.1** — Trouve les fichiers `.py` qui contiennent "TODO".

<details><summary>Solution</summary>

```bash
find project/ -name "*.py" -exec grep -l "TODO" {} +
```
</details>

**14.2** — Liste tous les fichiers de `project/` avec leur taille, triés du plus gros au plus petit.

<details><summary>Solution</summary>

```bash
find project/ -type f -exec du -h {} + | sort -rh
```
</details>
