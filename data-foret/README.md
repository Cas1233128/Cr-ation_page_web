# Data Forêt

Un parcours pour apprendre l'analyse de données et la data science **en pratiquant sur des cas forestiers**, pensé pour un ingénieur forestier qui débute en programmation.

Chaque module est un notebook Jupyter. Tu écris le code toi-même, une fonction `verifier()` te dit si c'est juste et **pourquoi** ce ne l'est pas, et `indice()` te débloque par étapes sans donner la solution.

## Les modules

| # | Module | Ce que tu apprends | Ouvrir |
|---|---|---|---|
| 0 | Prise en main de Python | Une notion à la fois : types, opérateurs, texte, erreurs, conditions, listes, boucles, dictionnaires, fonctions | [Ouvrir dans Colab](https://colab.research.google.com/github/Cas1233128/Cr-ation_page_web/blob/claude/quirky-keller-jhyoi0/data-foret/00_prise_en_main_python.ipynb) |
| 1 | Bases de Python appliquées | Combiner ces notions sur des calculs forestiers complets | [Ouvrir dans Colab](https://colab.research.google.com/github/Cas1233128/Cr-ation_page_web/blob/claude/quirky-keller-jhyoi0/data-foret/01_bases_python.ipynb) |
| 1b | Prise en main de pandas | Tableaux, colonnes, filtres, .loc, groupby, une notion à la fois, avec un aide-mémoire | [Ouvrir dans Colab](https://colab.research.google.com/github/Cas1233128/Cr-ation_page_web/blob/claude/quirky-keller-jhyoi0/data-foret/01b_prise_en_main_pandas.ipynb) |
| 2 | Nettoyer un inventaire | pandas : charger, diagnostiquer et nettoyer un inventaire en désordre | [Ouvrir dans Colab](https://colab.research.google.com/github/Cas1233128/Cr-ation_page_web/blob/claude/quirky-keller-jhyoi0/data-foret/02_nettoyage_inventaire.ipynb) |
| 3 | Dendrométrie et carbone | G, N, essences dominantes, imputation, allométrie de Chave (2014), carbone | [Ouvrir dans Colab](https://colab.research.google.com/github/Cas1233128/Cr-ation_page_web/blob/claude/quirky-keller-jhyoi0/data-foret/03_dendrometrie_carbone.ipynb) |
| 4 | Transects : taux de rencontre | Fiche au format du programme, effort, doublons cachés, coordonnées, taux par transect et par strate | [Ouvrir dans Colab](https://colab.research.google.com/github/Cas1233128/Cr-ation_page_web/blob/claude/quirky-keller-jhyoi0/data-foret/04_transects_taux_rencontre.ipynb) |
| 5 | Transects : densité et effectif | Distance sampling des nids de gorille : fonction de détection, ESW, densité, effectif par strate, IC par bootstrap, équivalent R | [Ouvrir dans Colab](https://colab.research.google.com/github/Cas1233128/Cr-ation_page_web/blob/claude/quirky-keller-jhyoi0/data-foret/05_transects_densite.ipynb) |
| 6 | Pièges photo : taux de capture | Export Camelot (71 colonnes), dates aberrantes, effort réel, événements indépendants, RAI, sensibilité au seuil | [Ouvrir dans Colab](https://colab.research.google.com/github/Cas1233128/Cr-ation_page_web/blob/claude/quirky-keller-jhyoi0/data-foret/06_pieges_photo_taux_capture.ipynb) |
| 7 | Pièges photo : activité et occupation | Activité sur 24 h, chevauchement, occupation naïve puis modélisée | À construire |
| 8 | Expliquer les variations | Corrélations, tests, GLM de Poisson et binomial négatif | À construire |
| 9 | Perte de couvert forestier | Données satellitaires, analyse spatiale | À construire |

Compte 3 à 4 heures par module. À 4 ou 5 heures par semaine, les trois premiers modules prennent environ 3 semaines.

## Installer

**Option A : Google Colab (rien à installer, il faut un compte Google)**

1. Clique sur « Ouvrir dans Colab » dans le tableau ci-dessus.
2. Exécute la première cellule (bouton ▶). Elle télécharge seule les données et les vérifications.
3. Pour garder ton travail : *Fichier › Enregistrer une copie dans Drive*. Sinon, Colab efface tout à la fermeture.

**Option B : sur ton ordinateur (recommandé à terme)**

1. Installe [Anaconda](https://www.anaconda.com/download) (Python + Jupyter + pandas en une fois).
2. Télécharge ce dossier.
3. Ouvre *Anaconda Prompt*, va dans le dossier `data-foret` puis lance `jupyter lab`.

## Comment travailler

1. Lis l'énoncé, écris ton code sous `# À toi`, exécute avec **Maj + Entrée**.
2. Lis le verdict. Un ❌ explique ce qui ne va pas : corrige et recommence.
3. Bloqué plus de 15 minutes ? `indice("m2_e4")`, puis `indice("m2_e4", 2)`…
4. **Il n'y a pas de fichier de solutions, et c'est volontaire.** Une solution lue trop tôt donne l'illusion d'avoir compris.

## Utiliser une IA sans saboter ton apprentissage

Tu l'as dit toi-même : faire écrire à l'IA ce que tu ne maîtrises pas ne t'apprend rien. Colle ce texte au début de chaque conversation avec Claude ou un autre assistant :

```
Je suis débutant en Python et j'apprends en faisant des exercices.
Règles :
- Ne me donne jamais le code de la solution, même si je le demande.
- Quand je montre une erreur, explique ce qu'elle signifie et pose-moi une question qui m'aide à trouver la correction.
- Si je te montre mon code, dis-moi ce qui ne va pas sans le réécrire.
- Tu peux m'expliquer un concept avec un exemple qui n'a PAS de rapport avec mon exercice.
```

**Données du travail :** ne colle jamais dans une IA des données de ton programme (coordonnées de faune, données de patrouille, informations non publiées) sans l'accord de ta hiérarchie. Les exercices utilisent des données fictives précisément pour cette raison.

## Ce qu'il faut savoir sur les données

- **L'inventaire est fictif** : 20 placettes de 0,5 ha générées pour imiter une forêt dense humide du Sud-Cameroun (environ 400 tiges/ha, 19 à 33 m²/ha, 200 à 400 t/ha de biomasse aérienne). Les erreurs de saisie sont volontaires.
- **Les densités du bois** de `especes.csv` sont des valeurs indicatives. Pour un vrai calcul, utilise la Global Wood Density Database (Zanne et al., 2009).
- **Les DME** du module 1 sont inventés pour l'exercice. Les DME réels sont fixés par la réglementation camerounaise et les plans d'aménagement.
- **L'équation de biomasse** est celle de Chave et al. (2014), *Global Change Biology* 20 : 3177-3190, avec la fraction de carbone de 0,47 du GIEC.
