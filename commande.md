# Commandes de recherche — plan d'apprentissage

## 1. Recherche textuelle (le cœur)

- **grep** (POSIX) — bases : `-r -n -i -v -c -l -E -P` (PCRE), classes de caractères, ancres `^$`, `\b`
- **ripgrep** (`rg`) — le remplaçant moderne : ignore `.gitignore` par défaut, multiline (`-U`), types de fichiers (`--type`), replace (`-r`)
- **ag** (silver searcher), **ack** — alternatives historiques, bon à connaître pour comprendre l'évolution
- **awk** — recherche + extraction de champs (`$1`, `$2`), conditions
- **sed** — recherche + substitution, regex étendue

## 2. Recherche de fichiers (métadonnées)

- **find** — par nom, taille, date, permissions, profondeur, exécution de commandes (`-exec`)
- **fd** — find moderne, syntaxe simplifiée
- **locate**/**mlocate** — index précalculé, rapide mais périmé si pas de `updatedb`

## 3. Forensic / binaire

- **strings** — extraction de texte lisible (`-n`, `-e` pour encodage UTF-16 etc.)
- **xxd** / **hexdump** — recherche de signatures hex (magic bytes)
- **binwalk** — détection de fichiers embarqués, extraction récursive
- **foremost**/**scalpel** — carving par signature
- **exiftool** — métadonnées cachées dans images/docs

## 4. Données structurées

- **jq** — recherche/filtrage JSON (`.[] | select()`)
- **yq** — équivalent YAML
- **xmllint --xpath** — XML
- **sqlite3** en CLI pour requêter des bases embarquées

## 5. Archives et compressés

- **zgrep**/**zcat**, **bzgrep**, **xzgrep** — grep dans du compressé sans extraire
- **7z l** / **unzip -l** — lister sans extraire

## 6. Réseau / capture

- **tshark** avec filtres d'affichage (recherche dans pcap)
- **ngrep** — grep sur trafic réseau live ou capture

## 7. Regex avancée (transversal à tout)

- PCRE vs POSIX ERE vs BRE — différences de syntaxe selon l'outil
- Lookahead/lookbehind, groupes nommés, backreferences
- `\K`, mode `-z` (NUL-separated, pour multiline)
