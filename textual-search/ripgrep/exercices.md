# Exercices ripgrep

Ces exercices utilisent les données du dossier [`data/`](data/). Avant de commencer, place-toi dedans :

```bash
cd textual-search/ripgrep/data
```

Pour chaque exercice : un énoncé, un indice, puis la solution repliée (clique pour l'afficher).

## 1. Introduction

**1.1** — Depuis `data/`, cherche "TODO" dans tout le dossier, sans utiliser `-r` ni préciser de sous-dossier. Observe que les fichiers de `project/node_modules/` et `project/build/` (gitignorés) n'apparaissent pas.

<details><summary>Solution</summary>

```bash
rg "TODO"
```
</details>

## 2. Options d'affichage

**2.1** — Compte le nombre de lignes contenant "error" dans `app.log`.

<details><summary>Solution</summary>

```bash
rg -c "error" app.log
```
</details>

**2.2** — Parmi tous les fichiers de `data/` (hors `project/`), lesquels contiennent "error" ?

<details><summary>Solution</summary>

```bash
rg -l "error" .
```
</details>

**2.3** — Extrait uniquement le texte après "TODO: " dans `script.py` et `project/src/app.py`, en une seule commande.

<details><summary>Indice</summary>`-o` avec une regex `TODO: .*`, plusieurs fichiers en arguments.</details>
<details><summary>Solution</summary>

```bash
rg -o "TODO: .*" script.py project/src/app.py
```
</details>

## 3. Options de matching

**3.1** — Compare le nombre de matches de "error" dans `app.log` par défaut, puis avec `-S` (smart-case). Pourquoi le résultat change ?

<details><summary>Indice</summary>`app.log` contient "error", "Error" et "ERROR".</details>
<details><summary>Solution</summary>

```bash
rg -c "error" app.log     # 1 (sensible à la casse par défaut)
rg -Sc "error" app.log    # 5 (motif tout en minuscules → smart-case l'insensibilise)
```
</details>

**3.2** — Dans le texte `system log / auto login / catalog item`, trouve la ligne contenant le mot exact "log" (pas "login" ni "catalog").

<details><summary>Solution</summary>

```bash
printf "system log\nauto login\ncatalog item\n" | rg -w "log"
```
</details>

**3.3** — Dans `version 3.14.15 vs 3X14X15`, cherche littéralement "3.14.15" sans que le `.` ne matche n'importe quel caractère.

<details><summary>Solution</summary>

```bash
echo "version 3.14.15 vs 3X14X15" | rg -F "3.14.15"
```
</details>

## 4. Contexte

**4.1** — Affiche l'exception de `app.log` avec les 2 lignes suivantes.

<details><summary>Solution</summary>

```bash
rg -A 2 "Exception" app.log
```
</details>

**4.2** — Affiche "connexion refusée" dans `server.log` avec 3 lignes de contexte avant/après.

<details><summary>Solution</summary>

```bash
rg -C 3 "connexion refusée" server.log
```
</details>

## 5. Plusieurs motifs

**5.1** — Cherche "error" ou "Exception" dans `app.log` avec `-e`.

<details><summary>Solution</summary>

```bash
rg -e "error" -e "Exception" app.log
```
</details>

**5.2** — Refais la même recherche avec `motifs.txt` comme fichier de motifs.

<details><summary>Solution</summary>

```bash
rg -f motifs.txt app.log
```
</details>

## 6. Filtrage de fichiers

**6.1** — Dans `project/`, cherche "TODO" uniquement dans les fichiers Python.

<details><summary>Solution</summary>

```bash
rg -t py "TODO" project/
```
</details>

**6.2** — Refais la recherche précédente en excluant cette fois les fichiers Markdown (résultat identique ici, mais pas pour la même raison — laquelle ?).

<details><summary>Indice</summary>`-t py` inclut seulement les .py ; `-T md` exclut seulement les .md. Les deux excluent `README.md`, mais `-T md` laisserait passer un `.js` par exemple, pas `-t py`.</details>
<details><summary>Solution</summary>

```bash
rg -T md "TODO" project/
```
</details>

**6.3** — Depuis `data/`, cherche "error" uniquement dans les fichiers `.log`.

<details><summary>Solution</summary>

```bash
rg -g "*.log" "error" .
```
</details>

**6.4** — Dans `project/`, cherche "password" en excluant le dossier `vendor/`.

<details><summary>Solution</summary>

```bash
rg -g "!vendor/*" "password" project/
```
</details>

**6.5** — `project/.env` contient une clé API mais n'apparaît dans aucune recherche normale. Affiche-le quand même.

<details><summary>Solution</summary>

```bash
rg --hidden "API_KEY" project/
```
</details>

**6.6** — Cherche "TODO" dans `project/` en ignorant complètement les règles `.gitignore` (tu dois maintenant voir aussi `node_modules/lib.js` et `debug.log`).

<details><summary>Solution</summary>

```bash
rg -uu "TODO" project/
```
</details>

**6.7** — Liste, sans chercher de motif, tous les fichiers `.py` que `rg` regarderait dans `project/`.

<details><summary>Solution</summary>

```bash
rg --files project/ -g "*.py"
```
</details>

## 7. Remplacement

**7.1** — Affiche `app.log` avec "error" remplacé par "ERROR" (uniquement à l'affichage, le fichier n'est pas modifié).

<details><summary>Solution</summary>

```bash
rg "error" -r "ERROR" app.log
```
</details>

**7.2** — Dans `script.py`, affiche la ligne de TODO en remplaçant "TODO: " par "FIXME: ", en réutilisant le texte capturé après "TODO: ".

<details><summary>Indice</summary>Capture avec `(...)`, réutilise avec `$1`.</details>
<details><summary>Solution</summary>

```bash
rg "TODO: (.*)" -r 'FIXME: $1' script.py
```
</details>

## 8. Contrôle du volume et scripting

**8.1** — Affiche seulement la première ligne "ERROR" de `app.log`.

<details><summary>Solution</summary>

```bash
rg -m 1 "ERROR" app.log
```
</details>

**8.2** — Affiche "trouvé" seulement si `test_results.txt` contient "FAILED", sans afficher la ligne elle-même.

<details><summary>Solution</summary>

```bash
rg -q "FAILED" test_results.txt && echo "trouvé"
```
</details>

## 9. Recherche multiligne

**9.1** — Dans `app.log`, capture tout le bloc depuis "Exception" jusqu'à la ligne contenant "App.main" (sur plusieurs lignes).

<details><summary>Indice</summary>`-U`, et `[\s\S]*?` pour traverser les sauts de ligne de façon non gloutonne.</details>
<details><summary>Solution</summary>

```bash
rg -U "Exception[\s\S]*?App.main" app.log
```
</details>

## 10. Regex : moteur Rust vs PCRE2

**10.1** — Essaie d'extraire le premier mot après "TODO: " dans `script.py` avec un lookbehind, sans `-P`. Que se passe-t-il ?

<details><summary>Solution</summary>

```bash
rg '(?<=TODO: )\w+' script.py
# erreur : look-around non supporté par le moteur par défaut
```
</details>

**10.2** — Refais la même extraction en activant PCRE2.

<details><summary>Solution</summary>

```bash
rg -oP '(?<=TODO: )\w+' script.py
```
</details>

## 11. Options avancées supplémentaires

**11.1** — Affiche la ligne ET la colonne où "TODO" apparaît dans `script.py`.

<details><summary>Solution</summary>

```bash
rg --column "TODO" script.py
```
</details>

**11.2** — Cherche "secret" dans `binaire.dat` en forçant l'affichage du contenu binaire comme texte.

<details><summary>Solution</summary>

```bash
rg -a "secret" binaire.dat
```
</details>

**11.3** — Liste (séparés par NUL) les fichiers de `project/` contenant "TODO", puis affiche "trouvé: " devant chacun via `xargs -0`.

<details><summary>Solution</summary>

```bash
rg -l "TODO" -0 project | xargs -0 -I{} echo "trouvé: {}"
```
</details>

## 12. Combinaisons

**12.1** — Depuis `data/`, cherche "error" ou "warning", insensible à la casse, uniquement dans les `.log`.

<details><summary>Solution</summary>

```bash
rg -i "(error|warning)" -g "*.log" .
```
</details>

**12.2** — Fais un audit sécurité dans `project/` : cherche "password", "secret" ou "api_key", en incluant les fichiers habituellement ignorés par `.gitignore`.

<details><summary>Indice</summary>Combine l'alternance `|` avec l'option qui désactive le filtrage `.gitignore`.</details>
<details><summary>Solution</summary>

```bash
rg -uu "password|secret|api_key" project/
```
</details>
