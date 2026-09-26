# Exercices sed

Ces exercices utilisent les données du dossier [`data/`](data/). Avant de commencer, place-toi dedans :

```bash
cd textual-search/sed/data
```

Pour chaque exercice : un énoncé, un indice, puis la solution repliée (clique pour l'afficher).

## 1. Introduction

**1.1** — Affiche `app.log` avec "error" remplacé par "ERROR" (première occurrence par ligne), sans modifier le fichier.

<details><summary>Solution</summary>

```bash
sed 's/error/ERROR/' app.log
```
</details>

## 2. Substitution et flags

**2.1** — Remplace tous les "o" par "0" sur chaque ligne de `app.log`.

<details><summary>Solution</summary>

```bash
sed 's/o/0/g' app.log
```
</details>

**2.2** — Remplace uniquement la 2e occurrence de "o" sur chaque ligne.

<details><summary>Solution</summary>

```bash
sed 's/o/0/2' app.log
```
</details>

**2.3** — Remplace "error" par "ERROR" partout dans `app.log`, en ignorant la casse (donc "Error" et "ERROR" aussi).

<details><summary>Indice</summary>Combine deux flags après le 3e `/`.</details>
<details><summary>Solution</summary>

```bash
sed 's/error/ERROR/gI' app.log
```
</details>

## 3. Adresses

**3.1** — Remplace "o" par "0" uniquement sur les lignes 2 à 4 de `app.log`.

<details><summary>Solution</summary>

```bash
sed '2,4s/o/0/' app.log
```
</details>

**3.2** — Ajoute le préfixe "DERNIERE: " devant le contenu de la toute dernière ligne de `app.log`.

<details><summary>Indice</summary>Adresse `$`, et `&` dans le remplacement représente tout ce qui a matché.</details>
<details><summary>Solution</summary>

```bash
sed '$s/.*/DERNIERE: &/' app.log
```
</details>

**3.3** — Supprime toutes les lignes de `app.log` SAUF la ligne 2.

<details><summary>Solution</summary>

```bash
sed '2!d' app.log
```
</details>

## 4. Affichage sélectif (-n / p)

**4.1** — Affiche uniquement les lignes contenant "error", insensible à la casse, dans `app.log` (comme `grep -i "error"`).

<details><summary>Indice</summary>Le flag `I` peut aussi s'appliquer directement sur une adresse `/regex/I`, pas seulement sur `s///`.</details>
<details><summary>Solution</summary>

```bash
sed -n '/error/Ip' app.log
```
</details>

## 5. Suppression de lignes

**5.1** — Supprime les lignes de commentaire (commençant par `#`) de `config.conf`.

<details><summary>Solution</summary>

```bash
sed '/^#/d' config.conf
```
</details>

**5.2** — Supprime les lignes vides de `config.conf`.

<details><summary>Solution</summary>

```bash
sed '/^$/d' config.conf
```
</details>

## 6. Insertion, ajout, remplacement

**6.1** — Ajoute une ligne "--- FIN ---" après la toute dernière ligne de `test_results.txt`.

<details><summary>Solution</summary>

```bash
sed '$a\--- FIN ---' test_results.txt
```
</details>

**6.2** — Remplace la ligne contenant "FAILED" dans `test_results.txt` par "LIGNE SUPPRIMÉE POUR CONFIDENTIALITÉ".

<details><summary>Solution</summary>

```bash
sed '/FAILED/c\LIGNE SUPPRIMÉE POUR CONFIDENTIALITÉ' test_results.txt
```
</details>

## 7. Groupes de capture et backreferences

**7.1** — `employees.csv` contient des lignes `prenom,nom`. Inverse l'ordre en `nom,prenom` avec des groupes de capture, en syntaxe ERE.

<details><summary>Solution</summary>

```bash
sed -E 's/([a-z]+),([a-z]+)/\2,\1/' employees.csv
```
</details>

## 8. Modification sur place (-i)

**8.1** — Sur une copie de `app.log`, remplace "error" par "ERROR" directement dans le fichier, tout en gardant une sauvegarde `.bak`.

<details><summary>Solution</summary>

```bash
cp app.log app_copy.log
sed -i.bak 's/error/ERROR/g' app_copy.log
```
</details>

## 9. BRE vs ERE

**9.1** — Remplace "cat" ou "dog" par "animal" dans `pets.txt`, en syntaxe BRE (mode par défaut).

<details><summary>Indice</summary>En BRE, `|` doit être échappé pour être une alternance.</details>
<details><summary>Solution</summary>

```bash
sed 's/cat\|dog/animal/' pets.txt
```
</details>

## 10. Plusieurs commandes

**10.1** — En une seule commande `sed` (avec `;`), remplace "error" par "ERROR" partout, ET "info" par "INFO" en ignorant la casse, dans `app.log`.

<details><summary>Solution</summary>

```bash
sed 's/error/ERROR/g; s/info/INFO/gI' app.log
```
</details>

## 11. Hold space

**11.1** — Affiche les lignes de `app.log` dans l'ordre inverse (comme `tac`).

<details><summary>Solution</summary>

```bash
sed -n '1!G;h;$p' app.log
```
</details>

## 12. Autres commandes

**12.1** — Affiche seulement les 5 premières lignes de `app.log` avec `sed` (comme `head -n 5`).

<details><summary>Solution</summary>

```bash
sed '5q' app.log
```
</details>

**12.2** — Dans `file.txt`, translittère chaque `a`, `b`, `c` minuscule en majuscule.

<details><summary>Solution</summary>

```bash
sed 'y/abc/ABC/' file.txt
```
</details>

## 13. Séparateur alternatif

**13.1** — Remplace `/var/log/` par `/tmp/` dans `chemins.txt`, sans échapper les `/`.

<details><summary>Solution</summary>

```bash
sed 's|/var/log/|/tmp/|' chemins.txt
```
</details>

## 14. Combinaisons

**14.1** — Supprime à la fois les commentaires ET les lignes vides de `config.conf`, en une seule commande.

<details><summary>Solution</summary>

```bash
sed '/^#/d; /^$/d' config.conf
```
</details>

**14.2** — Extrait uniquement le contenu entre "START" et "END" (sans ces deux lignes) dans `rapport.txt`.

<details><summary>Solution</summary>

```bash
sed -n '/START/,/END/{/START/d; /END/d; p}' rapport.txt
```
</details>

**14.3** — Supprime les doublons consécutifs de `doublons.txt` (comme `uniq`, en pur sed).

<details><summary>Solution</summary>

```bash
sed '$!N; /^\(.*\)\n\1$/!P; D' doublons.txt
```
</details>
