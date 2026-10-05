# Exercices file

Ces exercices utilisent les fichiers du dossier [`data/`](data/). Avant de commencer :

```bash
cd forensic/file/data
```

Pour chaque exercice : un énoncé, un indice, puis la solution repliée.

## 1. Premier scan

**1.1** — Lance `file` sur tous les fichiers du dossier en une seule commande.

<details><summary>Solution</summary>

```bash
file *
```

Résultat attendu : tu verras tout de suite que plusieurs fichiers ne sont pas ce que leur extension prétend.
</details>

## 2. Fichiers à extension trompeuse

**2.1** — Quel est le vrai type de `image_secrete.txt` ?

<details><summary>Solution</summary>

```bash
file image_secrete.txt
# image_secrete.txt: PNG image data, 1 x 1, 8-bit/color RGB, non-interlaced
```

C'est un PNG, pas un fichier texte.
</details>

**2.2** — Quel est le vrai type de `rapport_finance.pdf` ?

<details><summary>Solution</summary>

```bash
file rapport_finance.pdf
# rapport_finance.pdf: JPEG image data, JFIF standard 1.01, ...
```

C'est un JPEG, pas un PDF.
</details>

**2.3** — `fake_image.jpg` est censé être une image. Qu'est-ce que `file` dit vraiment ?

<details><summary>Solution</summary>

```bash
file fake_image.jpg
# fake_image.jpg: ELF 64-bit LSB pie executable, x86-64, ...
```

C'est un exécutable Linux (ELF), pas une image.
</details>

## 3. Mode MIME

**3.1** — Affiche le type MIME de `image_secrete.txt`, `rapport_finance.pdf` et `fake_image.jpg`.

<details><summary>Solution</summary>

```bash
file -i image_secrete.txt rapport_finance.pdf fake_image.jpg
# image_secrete.txt:   image/png; charset=binary
# rapport_finance.pdf: image/jpeg; charset=binary
# fake_image.jpg:      application/x-pie-executable; charset=binary
```
</details>

## 4. Sans nom de fichier

**4.1** — Affiche uniquement le type de `document.docx`, sans que le nom du fichier apparaisse dans la sortie.

<details><summary>Indice</summary>L'option `-b` signifie *brief*.</details>
<details><summary>Solution</summary>

```bash
file -b document.docx
# Zip archive data, made by v2.0 UNIX, extract using at least v2.0, ...
```

`.docx` est en réalité une archive ZIP. C'est normal — tous les formats Microsoft Office modernes sont des ZIP.
</details>

## 5. Archives compressées

**5.1** — Qu'y a-t-il à l'intérieur de `archive.gz` ? Lance `file` deux fois : une sans option, une avec l'option qui inspecte le contenu.

<details><summary>Indice</summary>L'option `-z` demande à `file` de regarder à l'intérieur.</details>
<details><summary>Solution</summary>

```bash
file archive.gz
# archive.gz: gzip compressed data, from Unix, original size modulo 2^32 38

file -z archive.gz
# archive.gz: Unicode text, UTF-8 text (gzip compressed data, from Unix)
```

Sans `-z` : on sait que c'est du gzip.  
Avec `-z` : on sait que ça contient du texte UTF-8.
</details>

## 6. Extensions suggérées

**6.1** — Demande à `file` quelle extension conviendrait mieux pour `image_secrete.txt` et `rapport_finance.pdf`.

<details><summary>Solution</summary>

```bash
file --extension image_secrete.txt rapport_finance.pdf
# image_secrete.txt:   png
# rapport_finance.pdf: jpeg/jpg/jpe/jfif
```
</details>

## 7. Lire depuis une liste

**7.1** — Crée un fichier `liste.txt` contenant les noms de `notes.txt`, `fake_image.jpg` et `archive.gz`, puis passe cette liste à `file`.

<details><summary>Indice</summary>L'option `-f` lit les chemins depuis un fichier.</details>
<details><summary>Solution</summary>

```bash
echo -e "notes.txt\nfake_image.jpg\narchive.gz" > liste.txt
file -f liste.txt
```

Ou avec `ls` :

```bash
ls notes.txt fake_image.jpg archive.gz > liste.txt
file -f liste.txt
```
</details>

## 8. Combiner avec find

**8.1** — Lance `file` sur tous les fichiers du dossier en passant par `find` (pas juste `file *`).

<details><summary>Indice</summary>`find . -type f -exec file {} +`</details>
<details><summary>Solution</summary>

```bash
find . -type f -exec file {} +
```

Le `{} +` regroupe tous les fichiers en un seul appel — plus efficace que `{} \;` qui lancerait un `file` par fichier.
</details>

**8.2** — Parmi tous les fichiers du dossier, affiche uniquement ceux qui sont des exécutables ELF.

<details><summary>Solution</summary>

```bash
file * | grep "ELF"
# fake_image.jpg: ELF 64-bit LSB pie executable, ...
```

Ou avec find pour une arborescence :

```bash
find . -type f | xargs file | grep "ELF"
```
</details>

## 9. Workflow CTF complet

**9.1** — Tu reçois un dossier avec des fichiers aux extensions variées. Écris la commande qui affiche le type MIME de chaque fichier, pour avoir une vue synthétique à scripter.

<details><summary>Solution</summary>

```bash
file -i *
```

La sortie MIME est facile à parser avec `grep` ou `awk` :

```bash
file -i * | grep "image/"      # seulement les images
file -i * | grep "application/x-executable\|application/x-pie-executable"  # exécutables
```
</details>

**9.2** — Tu veux compter combien de fichiers de chaque type se trouvent dans le dossier.

<details><summary>Solution</summary>

```bash
file -b * | sort | uniq -c | sort -rn
```

`-b` supprime les noms → la sortie ne contient que les types → `sort | uniq -c` compte les occurrences.
</details>
