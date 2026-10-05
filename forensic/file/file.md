# file — cours complet

`file` identifie le **vrai type** d'un fichier en lisant son contenu, pas son extension. C'est systématiquement la première commande à lancer sur un fichier inconnu en CTF ou en forensic.

## 1. Introduction — pourquoi l'extension ne suffit pas

Les extensions (`.jpg`, `.pdf`, `.txt`...) ne sont que des étiquettes. N'importe qui peut renommer un fichier PNG en `.txt` — son contenu ne change pas.

`file` fait le contraire : il **lit le début du fichier** (les *magic bytes*, aussi appelés *signatures*) et compare avec une base de données de formats connus pour identifier ce que le fichier est vraiment.

```bash
file image_secrete.txt
# image_secrete.txt: PNG image data, 1 x 1, 8-bit/color RGB, non-interlaced
```

Le fichier s'appelle `.txt`, mais `file` voit les bytes `\x89PNG` au début et dit : c'est un PNG.

## 2. Usage basique

```bash
file notes.txt                    # un fichier
file notes.txt rapport_finance.pdf fake_image.jpg   # plusieurs fichiers d'un coup
file data/*                       # tous les fichiers d'un dossier
```

Sortie typique :

```
image_secrete.txt:   PNG image data, 1 x 1, 8-bit/color RGB, non-interlaced
rapport_finance.pdf: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16
fake_image.jpg:      ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, ...
document.docx:       Zip archive data, made by v2.0 UNIX, extract using at least v2.0, ...
analyse_logs:        Bourne-Again shell script, ASCII text executable
notes.txt:           ASCII text
archive.gz:          gzip compressed data, from Unix, original size modulo 2^32 38
```

Remarques directes :
- `rapport_finance.pdf` est en réalité un JPEG
- `fake_image.jpg` est un binaire ELF (exécutable Linux)
- `document.docx` est un ZIP (les fichiers `.docx`/`.xlsx`/`.pptx` sont des archives ZIP déguisées)

## 3. Options principales

| Option | Effet |
|---|---|
| `-b` | *brief* — affiche le type sans répéter le nom du fichier |
| `-i` | affiche le type MIME (`image/png`, `application/zip`...) |
| `-z` | inspecte le contenu à l'intérieur des archives compressées |
| `-k` | *keep going* — ne s'arrête pas au premier type détecté, continue les tests |
| `-f FICHIER` | lit la liste de fichiers à analyser depuis `FICHIER` (un chemin par ligne) |
| `--extension` | suggère les extensions correspondant au type détecté |
| `-L` | suit les liens symboliques (par défaut, `file` analyse le lien lui-même) |
| `-s` | analyse les fichiers spéciaux (devices `/dev/*`) |

### `-b` — sortie sans nom

Utile pour du scripting ou pour piper la sortie :

```bash
file -b image_secrete.txt
# PNG image data, 1 x 1, 8-bit/color RGB, non-interlaced
```

### `-i` — type MIME

```bash
file -i image_secrete.txt rapport_finance.pdf fake_image.jpg
# image_secrete.txt:   image/png; charset=binary
# rapport_finance.pdf: image/jpeg; charset=binary
# fake_image.jpg:      application/x-pie-executable; charset=binary
```

Pratique pour du filtrage automatique en script (`if file -bi "$f" | grep -q "image/"`).

### `-z` — voir dans les archives

```bash
file archive.gz
# archive.gz: gzip compressed data, from Unix, original size modulo 2^32 38

file -z archive.gz
# archive.gz: Unicode text, UTF-8 text (gzip compressed data, from Unix)
```

Sans `-z`, `file` s'arrête à "c'est du gzip". Avec `-z`, il décompresse en mémoire et identifie aussi le contenu.

### `--extension` — extensions suggérées

```bash
file --extension image_secrete.txt rapport_finance.pdf
# image_secrete.txt:   png
# rapport_finance.pdf: jpeg/jpg/jpe/jfif
```

Renvoie `???` si `file` ne connaît pas d'extension standard pour ce type.

### `-f` — lire depuis une liste

```bash
find . -type f > /tmp/liste.txt
file -f /tmp/liste.txt
```

Évite de construire une ligne de commande trop longue avec des centaines de fichiers.

### `-k` — continuer après le premier match

Par défaut, `file` s'arrête dès qu'il trouve un type. `-k` force la continuation de tous les tests :

```bash
file -k image_secrete.txt
# image_secrete.txt: PNG image data, 1 x 1, 8-bit/color RGB, non-interlaced
#                  - data
```

Le deuxième résultat (`data`) est le type générique qui "matche" presque tout. Utile quand un fichier pourrait être plusieurs choses à la fois (ex. un PDF qui contient aussi un exécutable embarqué).

## 4. Magic bytes — comment ça marche

`file` compare les premiers octets d'un fichier (parfois à des offsets précis) avec une base de signatures appelée `magic`. Chaque format a une signature reconnaissable :

| Format | Offset | Magic bytes (hex) | Ascii |
|---|---|---|---|
| PNG | 0 | `89 50 4E 47 0D 0A 1A 0A` | `\x89PNG\r\n\x1a\n` |
| JPEG | 0 | `FF D8 FF` | `ÿØÿ` |
| PDF | 0 | `25 50 44 46` | `%PDF` |
| ZIP | 0 | `50 4B 03 04` | `PK\x03\x04` |
| ELF | 0 | `7F 45 4C 46` | `\x7fELF` |
| GIF | 0 | `47 49 46 38` | `GIF8` |
| gzip | 0 | `1F 8B` | — |

En CTF, **vérifier les magic bytes manuellement** avec `xxd` (vu plus tard) est souvent nécessaire quand un fichier a été corrompu intentionnellement pour tromper `file`.

## 5. Workflow CTF — les trois réflexes

**Réflexe 1 : scanner tous les fichiers d'un dossier d'un coup**

```bash
file data/*
```

**Réflexe 2 : trouver les fichiers avec une extension trompeuse**

```bash
# Les fichiers qui ne sont pas ce que leur extension prétend
for f in data/*; do
    ext="${f##*.}"
    type=$(file -bi "$f")
    echo "$f → ext:.$ext | type:$type"
done
```

**Réflexe 3 : combiner avec `find` pour scanner une arborescence entière**

```bash
find . -type f -exec file {} +
```

Le `{} +` regroupe tous les fichiers en un seul appel à `file` — bien plus rapide que `{} \;` sur un grand nombre de fichiers.

## 6. Exemples CTF concrets

```bash
# Scan complet d'un dossier de challenge
file challenge/*
# → on repère les fichiers suspects (ELF caché en .jpg, ZIP caché en .docx...)

# Trouver tous les exécutables déguisés
file data/* | grep -i "ELF"

# Trouver toutes les images, peu importe leur extension
file data/* | grep -iE "PNG|JPEG|GIF|BMP|TIFF"

# Type MIME pour du scripting propre
file -bi rapport_finance.pdf
# image/jpeg; charset=binary
```

## 7. Combinaisons utiles

```bash
# Lister type + taille pour chaque fichier
find . -type f -exec file -b {} \; | sort | uniq -c | sort -rn
# → vue d'ensemble : combien de fichiers par type

# Extraire seulement les exécutables ELF d'un dossier
find . -type f | xargs file | grep "ELF" | cut -d: -f1

# Vérifier qu'un fichier téléchargé est bien ce qu'il prétend être
file -b document.docx
# Zip archive data → c'est normal, .docx est un ZIP
```
