# Exercices grep

Ces exercices utilisent les données du dossier [`data/`](data/). Avant de commencer, place-toi dedans :

```bash
cd textual-search/grep/data
```

Pour chaque exercice : un énoncé, un indice, puis la solution repliée (clique pour l'afficher).

## 1. Bases

**1.1** — Affiche les lignes de `app.log` contenant "error" en minuscules.

<details><summary>Indice</summary>Pas besoin d'option, juste le motif et le fichier.</details>
<details><summary>Solution</summary>

```bash
grep "error" app.log
```
</details>

**1.2** — Sans afficher aucune ligne, fais échouer silencieusement puis affiche "Erreurs présentes" seulement si `app.log` contient "error".

<details><summary>Indice</summary>Quelle option rend grep silencieux et utilisable dans une condition ?</details>
<details><summary>Solution</summary>

```bash
grep -q "error" app.log && echo "Erreurs présentes"
```
</details>

## 2. Options d'affichage

**2.1** — Affiche le(s) TODO de `script.py` avec leur numéro de ligne.

<details><summary>Solution</summary>

```bash
grep -n "TODO" script.py
```
</details>

**2.2** — Compte combien de fois "error" apparaît dans `app.log`, insensible à la casse (donc "error", "Error", "ERROR" comptent).

<details><summary>Indice</summary>Combine deux options.</details>
<details><summary>Solution</summary>

```bash
grep -ci "error" app.log
```
</details>

**2.3** — Parmi tous les `.log` du dossier, lesquels contiennent "error" ?

<details><summary>Solution</summary>

```bash
grep -l "error" *.log
```
</details>

**2.4** — Extrait uniquement les identifiants `user_XX` de `access.log` (pas la ligne entière).

<details><summary>Indice</summary>L'option qui n'affiche que la partie correspondante, avec une regex `user_[0-9]+`.</details>
<details><summary>Solution</summary>

```bash
grep -o "user_[0-9]\+" access.log
```
</details>

## 3. Options de matching

**3.1** — Affiche toutes les lignes de `config.conf` qui ne sont PAS des commentaires (ne commencent pas par `#`).

<details><summary>Solution</summary>

```bash
grep -v "^#" config.conf
```
</details>

**3.2** — Trouve le mot exact "cat" dans `file.txt`, sans matcher "category" ni "cats".

<details><summary>Solution</summary>

```bash
grep -w "cat" file.txt
```
</details>

**3.3** — Trouve dans `status.txt` la ligne qui est EXACTEMENT "done" (pas "not done", pas "done yet").

<details><summary>Solution</summary>

```bash
grep -x "done" status.txt
```
</details>

**3.4** — Cherche littéralement "3.14.15" dans `version.txt`, sans que le `.` ne matche n'importe quel caractère. Compare avec le résultat sans cette option.

<details><summary>Indice</summary>L'option qui traite le motif comme une chaîne littérale, pas une regex.</details>
<details><summary>Solution</summary>

```bash
grep -F "3.14.15" version.txt
# sans -F : grep "3.14.15" version.txt matche aussi "3X14X15" et "3-14-15" (le . matche n'importe quel caractère)
```
</details>

## 4. Contexte

**4.1** — Affiche l'exception dans `app.log` avec les 2 lignes suivantes (la stack trace).

<details><summary>Solution</summary>

```bash
grep -A 2 "Exception" app.log
```
</details>

**4.2** — Affiche les occurrences de "connexion refusée" dans `server.log` avec 3 lignes de contexte avant et après.

<details><summary>Solution</summary>

```bash
grep -C 3 "connexion refusée" server.log
```
</details>

## 5. Plusieurs motifs

**5.1** — Cherche "error" OU "Exception" dans `app.log` en une seule commande, avec `-e`.

<details><summary>Solution</summary>

```bash
grep -e "error" -e "Exception" app.log
```
</details>

**5.2** — Refais la même recherche en utilisant `motifs.txt` comme fichier de motifs.

<details><summary>Solution</summary>

```bash
grep -f motifs.txt app.log
```
</details>

## 6. Recherche récursive

**6.1** — Trouve tous les TODO dans `src/`, récursivement, avec numéro de ligne.

<details><summary>Solution</summary>

```bash
grep -rn "TODO" src/
```
</details>

**6.2** — Refais la recherche précédente en ne cherchant que dans les fichiers `.py` (exclut `README.md`).

<details><summary>Solution</summary>

```bash
grep -rn "TODO" --include="*.py" src/
```
</details>

**6.3** — Cherche "password" dans tout le dossier courant (`.`), récursivement, en excluant le dossier `vendor/`.

<details><summary>Indice</summary>En vrai projet, tu ferais pareil avec `--exclude-dir=".git"`.</details>
<details><summary>Solution</summary>

```bash
grep -rn "password" --exclude-dir="vendor" .
```
</details>

## 7. Contrôle du volume et scripting

**7.1** — Affiche seulement la première ligne "ERROR" trouvée dans `app.log`, même s'il y en a plusieurs.

<details><summary>Solution</summary>

```bash
grep -m 1 "ERROR" app.log
```
</details>

**7.2** — Écris une condition shell qui affiche "Des tests ont échoué" si `test_results.txt` contient "FAILED".

<details><summary>Solution</summary>

```bash
if grep -q "FAILED" test_results.txt; then
    echo "Des tests ont échoué"
fi
```
</details>

## 8. Fichiers binaires

**8.1** — Cherche "secret" dans `binaire.dat` sans option particulière. Que se passe-t-il ?

<details><summary>Indice</summary>grep détecte que le fichier est binaire et ne montre pas son contenu par défaut.</details>
<details><summary>Solution</summary>

```bash
grep "secret" binaire.dat
# binaire.dat: fichiers binaires correspondent (ou "binary file matches")
```
</details>

**8.2** — Force l'affichage du contenu textuel autour de "secret" dans `binaire.dat`.

<details><summary>Solution</summary>

```bash
grep -a "secret" binaire.dat
```
</details>

## 9. Regex avancée

**9.1** — Trouve les lignes contenant "cat" ou "dog" dans `pets.txt`, d'abord en BRE (syntaxe de base), puis en ERE (`-E`).

<details><summary>Solution</summary>

```bash
grep '\(cat\|dog\)' pets.txt
grep -E '(cat|dog)' pets.txt
```
</details>

**9.2** — Extrait uniquement les nombres qui suivent `id=` dans `data.txt`, sans le `id=` lui-même (attention à `id=ABC123`, qui ne doit rien donner).

<details><summary>Indice</summary>Lookbehind PCRE : `(?<=...)`.</details>
<details><summary>Solution</summary>

```bash
grep -oP '(?<=id=)\d+' data.txt
```
</details>

**9.3** — Extrait uniquement les valeurs numériques exprimées en pixels dans `style.css` (donc pas `14pt`).

<details><summary>Indice</summary>Lookahead PCRE : `(?=...)`.</details>
<details><summary>Solution</summary>

```bash
grep -oP '\d+(?=px)' style.css
```
</details>

**9.4** — Dans `file.txt`, trouve les lignes contenant au moins un chiffre, en utilisant une classe de caractères POSIX (pas `[0-9]`).

<details><summary>Solution</summary>

```bash
grep -E '[[:digit:]]+' file.txt
```
</details>

## 10. Combinaisons

**10.1** — Cherche "error" ou "warning", insensible à la casse, avec numéro de ligne, récursivement, uniquement dans les fichiers `.log` du dossier courant.

<details><summary>Solution</summary>

```bash
grep -rniE --include="*.log" '(error|warning)' .
```
</details>

**10.2** — Compte les occurrences de chaque code HTTP dans `access.log`.

<details><summary>Indice</summary>Combine `-o`, une regex, puis `sort | uniq -c`.</details>
<details><summary>Solution</summary>

```bash
grep -oE 'HTTP/[0-9.]+" [0-9]{3}' access.log | sort | uniq -c
```
</details>

**10.3** — Extrait toutes les adresses email de `contacts.txt`.

<details><summary>Solution</summary>

```bash
grep -oE '[[:alnum:].+_-]+@[[:alnum:].-]+\.[[:alpha:]]{2,}' contacts.txt
```
</details>

**10.4** — Liste les fichiers `.py` de `src/` contenant "TODO", puis pour chacun affiche uniquement les lignes correspondantes.

<details><summary>Indice</summary>`-l` pour lister les fichiers, puis `xargs` pour réutiliser la liste comme arguments d'une seconde commande grep.</details>
<details><summary>Solution</summary>

```bash
grep -rl "TODO" --include="*.py" src/ | xargs grep -n "TODO"
```
</details>
