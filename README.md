# search-commands

Apprendre à fond les commandes de recherche en ligne de commande — grep, ripgrep, find, awk, sed, outils forensic, données structurées, regex — par la théorie et par la pratique.

Chaque outil a son propre module : un cours de référence, des exercices avec indices et solutions, et des fichiers d'exemple réalistes pour s'entraîner. Toutes les commandes présentées ont été testées avant d'être écrites — pas de pseudo-code.

## Pourquoi ce projet

Ces outils sont utilisés tous les jours par n'importe quel développeur ou administrateur système, mais rarement maîtrisés au-delà de `grep -r` ou `find -name`. L'objectif ici est d'aller jusqu'au bout de chaque outil : ses options avancées, ses pièges classiques (BRE vs ERE, comportement sur les fichiers binaires, smart-case...), et les combinaisons qui servent vraiment en pratique.

## Structure d'un module

```
<catégorie>/<outil>/
├── <outil>.md    # cours : une section par catégorie d'options, avec exemples
├── exercices.md   # exercices pratiques, indices puis solutions repliées
└── data/           # fichiers utilisés par le cours et les exercices
```

## Pour apprendre un outil

```bash
cd textual-search/grep
```

1. Lire `grep.md` — le cours.
2. Se placer dans `data/` et suivre `exercices.md` pour pratiquer sur de vraies commandes.

**Utilise le mode aperçu (preview) pour lire les `.md`** — les cours contiennent des tableaux, du code coloré et une mise en forme pensée pour être lus rendus, pas en texte brut. Dans VS Code : `Ctrl+Shift+V` pour prévisualiser le fichier ouvert.

Pour que **tous** les `.md` s'ouvrent automatiquement en aperçu, sans avoir à le faire à chaque fois :

1. Ouvre les paramètres VS Code (`Ctrl+,`)
2. Cherche **"editor associations"**
3. Clique sur **"Edit in settings.json"**
4. Ajoute :
   ```json
   "workbench.editorAssociations": {
       "*.md": "vscode.markdown.preview.editor"
   }
   ```

Après ça, chaque `.md` ouvert ou double-cliqué s'affiche directement en rendu.

## Outils couverts

- **Recherche textuelle** — grep, ripgrep, ag/ack, awk, sed
- **Recherche de fichiers** — find, fd, locate
- **Forensic / binaire** — strings, xxd/hexdump, binwalk, foremost/scalpel, exiftool
- **Données structurées** — jq, yq, xmllint, sqlite3
- **Archives** — zgrep/bzgrep/xzgrep, 7z/unzip
- **Réseau** — tshark, ngrep
- **Regex avancée** — POSIX vs PCRE, lookaround, backreferences

Le projet est en cours de construction, module par module.
