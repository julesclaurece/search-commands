# Exercices awk

Ces exercices utilisent les données du dossier [`data/`](data/). Avant de commencer, place-toi dedans :

```bash
cd textual-search/awk/data
```

Pour chaque exercice : un énoncé, un indice, puis la solution repliée (clique pour l'afficher).

## 1. Introduction

**1.1** — Affiche uniquement la méthode HTTP (2e champ) de chaque ligne d'`access.log`.

<details><summary>Solution</summary>

```bash
awk '{print $2}' access.log
```
</details>

**1.2** — Affiche les lignes de `app.log` contenant "error", sans écrire d'action explicite (comme `grep "error"`).

<details><summary>Indice</summary>Sans bloc `{ }`, awk affiche `$0` par défaut quand le motif matche.</details>
<details><summary>Solution</summary>

```bash
awk '/error/' app.log
```
</details>

## 2. Sélection et affichage de champs

**2.1** — Affiche le nom et la ville de chaque employé (`employees.csv`).

<details><summary>Solution</summary>

```bash
awk -F, '{print $2, $3}' employees.csv
```
</details>

**2.2** — Affiche uniquement le dernier champ (taille de réponse) de chaque ligne d'`access.log`.

<details><summary>Solution</summary>

```bash
awk '{print $NF}' access.log
```
</details>

## 3. Motifs

**3.1** — Affiche les lignes d'`access.log` dont le code HTTP est une erreur (≥ 400).

<details><summary>Solution</summary>

```bash
awk '$4 >= 400' access.log
```
</details>

**3.2** — Affiche le nom des employés qui habitent à Paris.

<details><summary>Solution</summary>

```bash
awk -F, '$3 == "paris" {print $2}' employees.csv
```
</details>

**3.3** — Affiche uniquement le bloc de `app.log` entre "Exception" et la ligne vide qui suit.

<details><summary>Solution</summary>

```bash
awk '/Exception/,/^$/' app.log
```
</details>

## 4. BEGIN et END

**4.1** — Affiche un en-tête "Employés :", puis chaque nom, puis le nombre total d'employés à la fin.

<details><summary>Solution</summary>

```bash
awk -F, 'BEGIN{print "Employés :"} {print $2} END{print "Total:", NR}' employees.csv
```
</details>

## 5. Variables intégrées

**5.1** — Affiche le numéro de ligne suivi du nom, pour chaque employé.

<details><summary>Solution</summary>

```bash
awk -F, '{print NR, $2}' employees.csv
```
</details>

**5.2** — Affiche nom et ville recollés par un `/` au lieu d'un espace.

<details><summary>Indice</summary>Change `OFS` dans un `BEGIN`.</details>
<details><summary>Solution</summary>

```bash
awk -F, 'BEGIN{OFS="/"} {print $2, $3}' employees.csv
```
</details>

## 6. Opérateurs et expressions

**6.1** — Affiche le code HTTP de chaque ligne d'`access.log` augmenté de 100.

<details><summary>Solution</summary>

```bash
awk '{print $4 + 100}' access.log
```
</details>

**6.2** — Pour chaque employé, affiche son nom suivi de "haut" si son salaire dépasse 3000, sinon "bas".

<details><summary>Indice</summary>Opérateur ternaire `cond ? a : b`.</details>
<details><summary>Solution</summary>

```bash
awk -F, '{print $2, ($5 > 3000 ? "haut" : "bas")}' employees.csv
```
</details>

## 7. Structures de contrôle

**7.1** — Pour chaque ligne d'`access.log`, affiche l'IP suivie de "erreur" si le code HTTP est ≥ 400, sinon "ok".

<details><summary>Solution</summary>

```bash
awk '{if ($4 >= 400) print $1, "erreur"; else print $1, "ok"}' access.log
```
</details>

**7.2** — Affiche `app.log` en sautant toutes les lignes contenant "INFO".

<details><summary>Solution</summary>

```bash
awk '/INFO/{next} {print}' app.log
```
</details>

## 8. Tableaux associatifs

**8.1** — Compte le nombre d'employés par ville.

<details><summary>Solution</summary>

```bash
awk -F, '{c[$3]++} END{for (v in c) print v, c[v]}' employees.csv
```
</details>

**8.2** — Somme les salaires par ville.

<details><summary>Solution</summary>

```bash
awk -F, '{s[$3] += $5} END{for (v in s) print v, s[v]}' employees.csv
```
</details>

## 9. Fonctions intégrées

**9.1** — Dans `access.log`, remplace "GET" par "get" sur chaque ligne (affichage seulement).

<details><summary>Solution</summary>

```bash
awk '{gsub(/GET/, "get"); print}' access.log
```
</details>

**9.2** — Découpe la chaîne `"203.0.113.10"` par `.` et affiche chaque partie sur sa propre ligne.

<details><summary>Solution</summary>

```bash
awk 'BEGIN{n=split("203.0.113.10", ip, "."); for(i=1;i<=n;i++) print ip[i]}'
```
</details>

## 10. Fonctions définies par l'utilisateur

**10.1** — Écris une fonction `tva(x)` qui calcule 20% d'un montant, et affiche le nom de chaque employé avec la TVA de son salaire.

<details><summary>Solution</summary>

```bash
awk -F, 'function tva(x){return x*0.2} {print $2, tva($5)}' employees.csv
```
</details>

## 11. Formatage de sortie avec printf

**11.1** — Affiche le nom (aligné à gauche sur 10 caractères) et le salaire (aligné à droite sur 6 caractères) de chaque employé.

<details><summary>Solution</summary>

```bash
awk -F, '{printf "%-10s %6d\n", $2, $5}' employees.csv
```
</details>

## 12. Travailler avec plusieurs fichiers

**12.1** — Affiche le nom et le département de chaque employé, en joignant `employees.csv` et `departments.csv` sur l'identifiant.

<details><summary>Indice</summary>Le motif `NR==FNR` n'est vrai que pendant la lecture du premier fichier.</details>
<details><summary>Solution</summary>

```bash
awk -F, 'NR==FNR{d[$1]=$2; next} {print $2, d[$1]}' departments.csv employees.csv
```
</details>

## 13. Options avancées

**13.1** — Affiche le nom et la ville des employés dont l'âge dépasse un seuil donné par une variable shell (essaie avec 30).

<details><summary>Indice</summary>`-v seuil=30`.</details>
<details><summary>Solution</summary>

```bash
awk -F, -v seuil=30 '$4 > seuil {print $2, $3}' employees.csv
```
</details>

**13.2** — `quoted.csv` contient un champ entre guillemets avec une virgule dedans (`"hello, world"`). Compare le nombre de champs comptés avec `-F,` puis avec `--csv`. Pourquoi le résultat diffère ?

<details><summary>Solution</summary>

```bash
awk -F, '{print NF}' quoted.csv   # 4 sur la ligne guillemetée : -F, coupe à tort à l'intérieur des guillemets
awk --csv '{print NF}' quoted.csv # 3 sur toutes les lignes : --csv respecte les guillemets
```
</details>

## 14. Combinaisons

**14.1** — Compte, pour `access.log`, combien de requêtes GET et combien de POST.

<details><summary>Solution</summary>

```bash
awk '{print $2}' access.log | sort | uniq -c
```
</details>

**14.2** — Affiche les employés dont le salaire dépasse 2700, triés par salaire décroissant.

<details><summary>Solution</summary>

```bash
awk -F, '$5 > 2700 {print $5, $2}' employees.csv | sort -rn
```
</details>

**14.3** — Supprime les doublons d'`employees.csv` sur l'identifiant (1re colonne).

<details><summary>Solution</summary>

```bash
awk -F, '!seen[$1]++' employees.csv
```
</details>
