# Commandes de recherche — plan d'apprentissage

Uniquement des outils modernes, réellement utilisés aujourd'hui et pertinents pour un futur CTF (forensic, stego, web, pwn léger). Chaque outil est pratiqué en profondeur : cours complet + données d'exemple + exercices, comme `grep` et `ripgrep`.

## 1. Recherche textuelle

- **grep** ✅ — bases : `-r -n -i -v -c -l -E -P` (PCRE), classes de caractères, ancres `^$`, `\b`
- **ripgrep** (`rg`) ✅ — ignore `.gitignore` par défaut, multiline (`-U`), types de fichiers (`--type`), replace (`-r`)
- **awk** — recherche + extraction de champs (`$1`, `$2`), conditions
- **sed** — recherche + substitution, regex étendue

## 2. Recherche de fichiers (métadonnées)

- **find** — par nom, taille, date, permissions, profondeur, exécution de commandes (`-exec`)

## 3. Forensic / binaire

- **file** — identifie le vrai type d'un fichier via ses magic bytes ; souvent la première commande lancée avant les autres
- **strings** — extraction de texte lisible (`-n`, `-e` pour encodage UTF-16 etc.)
- **xxd** / **hexdump** — recherche de signatures hex (magic bytes)
- **binwalk** — détection de fichiers embarqués, extraction récursive
- **foremost**/**scalpel** — carving par signature
- **exiftool** — métadonnées cachées dans images/docs

Stéganographie :

- **steghide** — cache/extrait des données dans images ou audio (avec mot de passe)
- **zsteg** — détection automatique de stéganographie dans des PNG/BMP (LSB...)
- **stegseek** — cassage rapide de mot de passe steghide par dictionnaire

## 4. Données structurées

- **jq** — recherche/filtrage JSON (`.[] | select()`)
- **yq** — équivalent YAML
- **xmllint --xpath** — XML (utile pour les challenges XXE)
- **sqlite3** en CLI pour requêter des bases embarquées

## 5. Archives et compressés

- **zgrep**/**zcat**, **bzgrep**, **xzgrep** — grep dans du compressé sans extraire
- **7z l** / **unzip -l** — lister sans extraire
- **tar tvf** — lister le contenu d'une archive `.tar`/`.tar.gz` sans l'extraire

## 6. Réseau / capture

- **tshark** avec filtres d'affichage (recherche dans pcap)

## 7. Regex avancée (transversal à tout)

- PCRE vs POSIX ERE vs BRE — différences de syntaxe selon l'outil
- Lookahead/lookbehind, groupes nommés, backreferences
- `\K`, mode `-z` (NUL-separated, pour multiline)
