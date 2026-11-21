# Data Forêt

Un parcours pour apprendre l'analyse de données et la data science **en pratiquant sur des cas forestiers**, pensé pour un ingénieur forestier qui débute en programmation.

Chaque module est un notebook Jupyter. Tu écris le code toi-même, une fonction `verifier()` te dit si c'est juste et **pourquoi** ce ne l'est pas, et `indice()` te débloque par étapes sans donner la solution.

## Les modules

| # | Module | Ce que tu apprends | Statut |
|---|---|---|---|
| 1 | `01_bases_python.ipynb` | Variables, listes, boucles, conditions, fonctions, dictionnaires | Prêt |
| 2 | `02_nettoyage_inventaire.ipynb` | pandas : charger, diagnostiquer et nettoyer un inventaire réel en désordre | Prêt |
| 3 | `03_dendrometrie_carbone.ipynb` | G, N, essences dominantes, imputation, allométrie de Chave (2014), carbone | Prêt |
| 4 | Statistiques appliquées | Comparer des zones, intervalles de confiance, erreur d'échantillonnage d'un inventaire (le lien avec ton bootcamp) | À construire |
| 5 | Modélisation | Régression hauteur-diamètre, validation, premier modèle prédictif | À construire |
| 6 | Pièges photographiques | Taux de détection, activité de la faune, cartes de présence | À construire |
| 7 | Perte de couvert forestier | Données satellitaires (Global Forest Change), raster, analyse spatiale | À construire |

Compte 3 à 4 heures par module. À 4 ou 5 heures par semaine, les trois premiers modules prennent environ 3 semaines.

## Installer

**Option A : Google Colab (rien à installer, il faut un compte Google)**

Dans un nouveau notebook Colab, exécute :

```
!git clone -b claude/quirky-keller-jhyoi0 https://github.com/Cas1233128/Cr-ation_page_web
%cd Cr-ation_page_web/data-foret
```

Puis ouvre le module dans Colab via *Fichier › Ouvrir un notebook*. Attention : Colab efface les fichiers à la fin de chaque session. Télécharge tes notebooks complétés (*Fichier › Télécharger*).

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
