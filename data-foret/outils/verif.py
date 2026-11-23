"""Vérifications automatiques et indices du parcours Data Forêt.

Utilisation dans un notebook :
    from outils.verif import verifier, indice
    verifier("m1_e1", dhp, hauteur, essence)
    indice("m1_e1")        # premier indice
    indice("m1_e1", 2)     # indice suivant, plus précis

Ce fichier ne contient pas les solutions. Tu peux le lire, mais tu apprendras
davantage en cherchant d'abord par toi-même.
"""
import json
import math
from pathlib import Path

_ICI = Path(__file__).resolve().parent
_RACINE = _ICI.parent
with open(_ICI / "attendus.json", encoding="utf-8") as f:
    _A = json.load(f)


class _Echec(Exception):
    pass


def _exige(condition, message):
    if not condition:
        raise _Echec(message)


def _proche(a, b, tol=1e-6, rel=False):
    try:
        a = float(a)
    except (TypeError, ValueError):
        return False
    return abs(a - b) <= (abs(b) * tol if rel else tol)


def _serie_vers_dict(s, nom):
    _exige(hasattr(s, "to_dict"), f"`{nom}` doit être une Series pandas (le résultat d'un groupby), pas un {type(s).__name__}.")
    return {int(k): float(v) for k, v in s.to_dict().items()}


def _g(d):
    return math.pi * (d / 200) ** 2


# ---------------------------------------------------------------- Module 1
_DHPS = [12.4, 35.0, 81.2, 18.9, 104.5, 47.3, 9.8, 66.0]


def _m1_e1(dhp, hauteur, essence):
    _exige(isinstance(dhp, (int, float)) and not isinstance(dhp, bool), f"`dhp` doit être un nombre. Tu as donné un {type(dhp).__name__} : as-tu mis des guillemets autour du nombre ?")
    _exige(dhp == 62.5, f"`dhp` vaut {dhp}, on attend 62.5. En Python, le séparateur décimal est le point, pas la virgule.")
    _exige(isinstance(hauteur, (int, float)) and hauteur == 34, "`hauteur` doit valoir le nombre 34.")
    _exige(isinstance(essence, str), "`essence` doit être un texte, donc entre guillemets.")
    _exige(essence == "Sapelli", f"`essence` vaut {essence!r}. Attention à la casse : on attend 'Sapelli'.")


def _m1_e2(g):
    if _proche(g, math.pi * (62.5 / 100) ** 2, 1e-4):
        raise _Echec("Tu as divisé par 100 : tu as utilisé le diamètre en mètres comme si c'était le rayon. Le rayon en mètres vaut dhp / 200.")
    if _proche(g, math.pi * (62.5 / 200), 1e-4):
        raise _Echec("Tu as oublié de mettre au carré. En Python, le carré s'écrit ** 2.")
    _exige(_proche(g, _g(62.5), 1e-4), f"g vaut {g}. Attendu : environ 0.3068 m². Revois la formule g = π × (dhp / 200)².")


def _m1_e3(n, dmax, moyenne):
    _exige(n == 8, f"Nombre d'arbres : {n}, attendu 8. Quelle fonction donne la longueur d'une liste ?")
    _exige(dmax == 104.5, f"Diamètre maximum : {dmax}, attendu 104.5.")
    _exige(_proche(moyenne, sum(_DHPS) / 8, 1e-6), f"Moyenne : {moyenne}. Attendu : {sum(_DHPS) / 8:.4f}. Moyenne = somme / nombre.")


def _m1_e4(liste_g):
    _exige(isinstance(liste_g, list), f"On attend une liste, tu as donné un {type(liste_g).__name__}.")
    _exige(len(liste_g) == 8, f"Ta liste a {len(liste_g)} éléments au lieu de 8 : un g par arbre. As-tu utilisé append() dans la boucle ?")
    for d, g in zip(_DHPS, liste_g):
        _exige(_proche(g, _g(d), 1e-6), f"Pour le dhp {d}, tu as g = {g}, attendu {_g(d):.6f}.")


def _m1_e5(nb, retenus):
    attendus = [d for d in _DHPS if d >= 10]
    _exige(nb == 7, f"Tu comptes {nb} arbres. Attendu : 7. Un arbre de exactement 10 cm est-il inventorié ? (>= ou >)")
    _exige(list(retenus) == attendus, f"Liste des arbres retenus incorrecte. Attendu : {attendus}.")


def _m1_e6(surface_terriere):
    _exige(callable(surface_terriere), "Il faut passer la fonction elle-même : verifier('m1_e6', surface_terriere), sans parenthèses.")
    for d in (10, 62.5, 100, 0):
        r = surface_terriere(d)
        _exige(r is not None, "Ta fonction ne renvoie rien. As-tu oublié le mot-clé return ?")
        _exige(_proche(r, _g(d), 1e-9), f"surface_terriere({d}) renvoie {r}, attendu {_g(d):.6f}.")


def _m1_e7(densite):
    _exige(callable(densite), "Passe la fonction elle-même, sans parenthèses.")
    _exige(densite("Azobé") == 0.95, f"densite('Azobé') renvoie {densite('Azobé')}, attendu 0.95.")
    _exige(densite("Ayous") == 0.36, "densite('Ayous') devrait renvoyer 0.36.")
    try:
        r = densite("Teck")
    except KeyError:
        raise _Echec("densite('Teck') provoque une erreur KeyError. Une essence inconnue doit renvoyer None. Cherche la méthode .get() des dictionnaires.")
    _exige(r is None, f"densite('Teck') renvoie {r!r}, attendu None.")


def _m1_e8(classe_diametre):
    _exige(callable(classe_diametre), "Passe la fonction elle-même, sans parenthèses.")
    for d, c in ((47.3, 40), (10, 10), (19.99, 10), (20, 20), (119.9, 110), (120, 120), (175, 120)):
        r = classe_diametre(d)
        _exige(r == c, f"classe_diametre({d}) renvoie {r}, attendu {c}.")


_DME = {"Ayous": 80, "Sapelli": 100, "Iroko": 100, "Azobé": 60}


def _m1_e9(est_exploitable):
    _exige(callable(est_exploitable), "Passe la fonction elle-même, sans parenthèses.")
    cas = [("Ayous", 85, True), ("Ayous", 80, True), ("Ayous", 79.9, False), ("Sapelli", 95, False), ("Azobé", 61, True), ("Fromager", 150, False)]
    for e, d, att in cas:
        try:
            r = est_exploitable(e, d, _DME)
        except KeyError:
            raise _Echec(f"est_exploitable({e!r}, {d}, dme) plante avec KeyError : l'essence n'est pas dans le dictionnaire. Elle doit renvoyer False.")
        _exige(r is att, f"est_exploitable({e!r}, {d}, dme) renvoie {r!r}, attendu {att}.")


_ARBRES = [("Ayous", 85.0), ("Sapelli", 112.4), ("Iroko", 64.0), ("Azobé", 71.5), ("Ayous", 42.0), ("Fromager", 140.0), ("Sapelli", 98.0)]


def _m1_e10(total):
    att = sum(_g(d) for e, d in _ARBRES if e in _DME and d >= _DME[e])
    tout = sum(_g(d) for _, d in _ARBRES)
    _exige(not _proche(total, tout, 1e-6), "Tu as additionné tous les arbres. Seuls les arbres exploitables comptent.")
    _exige(_proche(total, att, 1e-6), f"Total : {total}. Attendu : {att:.4f} m².")


# ---------------------------------------------------------------- Module 2
A2 = _A["m2"]


def _m2_e1(df):
    _exige(hasattr(df, "shape"), "On attend un DataFrame pandas (le résultat de pd.read_csv).")
    _exige(df.shape == (A2["nb_lignes_brut"], A2["nb_colonnes"]), f"Ton tableau a la forme {df.shape}, attendu {(A2['nb_lignes_brut'], A2['nb_colonnes'])}. As-tu lu donnees/inventaire_brut.csv ?")


def _m2_e2(reponse):
    _exige(isinstance(reponse, str), "Réponds par le texte 'texte' ou 'nombre'.")
    _exige(reponse.strip().lower() == "texte", "Non. Regarde df['dhp'].dtype : object ou str signifie que pandas a lu la colonne comme du texte. Cherche pourquoi dans les valeurs.")


def _m2_e3(df):
    import pandas as pd
    _exige(pd.api.types.is_numeric_dtype(df["dhp"]), f"La colonne dhp est encore de type {df['dhp'].dtype}. Elle doit être numérique.")
    nan = int(df["dhp"].isna().sum())
    _exige(nan == 0, f"{nan} valeurs sont devenues NaN pendant la conversion. Ce sont les nombres écrits avec une virgule : remplace-la par un point AVANT de convertir.")
    _exige(_proche(df["dhp"].sum(), A2["somme_dhp_converti"], 0.5), "La conversion n'a pas donné les bonnes valeurs. As-tu modifié autre chose que le séparateur décimal ?")


def _m2_e4(df):
    vus = set(df["essence"].unique())
    attendus = set(A2["essences"])
    en_trop = sorted(vus - attendus)
    _exige(not en_trop, f"Il reste des noms non harmonisés : {en_trop}. Pense aux espaces, aux majuscules, aux accents et aux fautes de frappe.")
    _exige(vus == attendus, f"Il manque des essences : {sorted(attendus - vus)}.")


def _m2_e5(nb_doublons, df):
    _exige(nb_doublons == A2["nb_doublons"], f"Tu comptes {nb_doublons} doublons. Ce n'est pas le bon nombre. Un doublon est une ligne identique à une autre dans TOUTES ses colonnes : df.duplicated() fait exactement ce test.")
    _exige(len(df) == A2["nb_apres_doublons"], f"Ton tableau a {len(df)} lignes après suppression, attendu {A2['nb_apres_doublons']}.")


def _m2_e6(df):
    _exige(float(df["dhp"].min()) > 0, f"Il reste des diamètres nuls ou négatifs (minimum : {df['dhp'].min()}).")
    _exige(len(df) == A2["nb_apres_dhp"], f"Ton tableau a {len(df)} lignes, attendu {A2['nb_apres_dhp']}.")


def _m2_e7(placette_mm):
    _exige(int(placette_mm) == A2["placette_mm"], f"Ce n'est pas la placette {placette_mm}. Compare la médiane du dhp de chaque placette : laquelle est environ 10 fois plus grande que les autres ?")


def _m2_e8(df):
    _exige(float(df["dhp"].max()) < 200, f"Il reste un dhp de {df['dhp'].max()} cm : impossible pour un arbre de cette forêt. La placette en millimètres n'a pas été corrigée, ou l'a été deux fois.")
    _exige(_proche(df["dhp"].median(), A2["dhp_median_global"], 0.05), f"Médiane globale du dhp : {df['dhp'].median()}. Attendu : {A2['dhp_median_global']}. As-tu corrigé seulement les lignes de la bonne placette ?")


def _m2_e9(nb):
    _exige(int(nb) == A2["nb_hauteurs_manquantes"], f"{nb} hauteurs manquantes, attendu {A2['nb_hauteurs_manquantes']} (compté sur le tableau nettoyé).")


def _m2_e10():
    import pandas as pd
    p = _RACINE / "donnees" / "inventaire_propre.csv"
    _exige(p.exists(), "Fichier donnees/inventaire_propre.csv introuvable. Vérifie le chemin passé à to_csv().")
    df = pd.read_csv(p)
    _exige("Unnamed: 0" not in df.columns, "Ton fichier contient une colonne 'Unnamed: 0' : c'est l'index. Ajoute index=False dans to_csv().")
    _exige(len(df) == A2["nb_apres_dhp"], f"Le fichier contient {len(df)} lignes, attendu {A2['nb_apres_dhp']}.")
    _m2_e4(df)
    _m2_e8(df)


# ---------------------------------------------------------------- Module 3
A3 = _A["m3"]


def _comparer_placettes(s, ref, nom, tol_rel):
    d = _serie_vers_dict(s, nom)
    _exige(set(d) == {int(k) for k in ref}, f"`{nom}` doit avoir une valeur par placette (20). Tu en as {len(d)}.")
    for k, v in ref.items():
        if not _proche(d[int(k)], v, tol_rel, rel=True):
            ratio = d[int(k)] / v if v else 0
            astuce = " Ton résultat est environ 2 fois trop petit : n'oublie pas de diviser par la surface (0,5 ha)." if 0.45 < ratio < 0.55 else ""
            astuce = astuce or (" Environ 1000 fois trop grand : convertis les kg en tonnes." if 900 < ratio < 1100 else "")
            raise _Echec(f"Placette {k} : {nom} = {d[int(k)]:.3f}, attendu ≈ {v}.{astuce}")


def _m3_e1(df):
    _exige("g" in df.columns, "Ajoute une colonne nommée 'g' au tableau.")
    _exige(_proche(df["g"].sum(), A3["somme_g"], 1e-3, rel=True), f"Somme des g : {df['g'].sum():.3f} m², attendu ≈ {A3['somme_g']}. Le dhp est en cm : rayon en m = dhp / 200.")


def _m3_e2(G_ha):
    _comparer_placettes(G_ha, A3["G_ha"], "G_ha", 1e-3)


def _m3_e3(N_ha):
    _comparer_placettes(N_ha, A3["N_ha"], "N_ha", 1e-6)


def _m3_e4(top3):
    _exige(list(top3) == A3["top3_G"], "Ce ne sont pas les bonnes essences, ou pas dans le bon ordre (de la plus grande surface terrière à la plus petite).")


def _m3_e5(df):
    nan = int(df["hauteur"].isna().sum())
    _exige(nan == 0, f"Il reste {nan} hauteurs manquantes.")
    _exige("classe" in df.columns, "Crée d'abord la colonne 'classe' (classes de 10 cm, plafonnées à 120).")
    _exige(_proche(df["hauteur"].mean(), A3["hauteur_moyenne_imputee"], 2e-3, rel=True), f"Hauteur moyenne après imputation : {df['hauteur'].mean():.3f} m, attendu ≈ {A3['hauteur_moyenne_imputee']}. Utilise la MÉDIANE de la classe de diamètre, pas la moyenne générale.")


def _m3_e6(df):
    _exige("densite_bois" in df.columns, "La colonne densite_bois est absente : as-tu fusionné avec especes.csv (merge) ?")
    _exige(len(df) == A3["n_final"], f"Le tableau a {len(df)} lignes après fusion, attendu {A3['n_final']}. Une fusion ne doit ni perdre ni dupliquer d'arbres.")
    _exige(int(df["densite_bois"].isna().sum()) == 0, "Certains arbres n'ont pas de densité : leurs noms d'essence ne correspondent pas à especes.csv.")


def _m3_e7(biomasse_chave):
    _exige(callable(biomasse_chave), "Passe la fonction elle-même, sans parenthèses.")
    for rho, d, h in ((0.6, 50, 30), (0.95, 100, 42), (0.36, 15, 12)):
        att = 0.0673 * (rho * d ** 2 * h) ** 0.976
        r = biomasse_chave(rho, d, h)
        _exige(_proche(r, att, 1e-6, rel=True), f"biomasse_chave({rho}, {d}, {h}) renvoie {r}, attendu ≈ {att:.1f} kg. Attention : l'exposant 0.976 s'applique à tout le produit ρ × D² × H.")


def _m3_e8(AGB_ha):
    _comparer_placettes(AGB_ha, A3["AGB_ha"], "AGB_ha", 5e-3)


def _m3_e9(C_ha, placette_max):
    _comparer_placettes(C_ha, A3["C_ha"], "C_ha", 5e-3)
    _exige(int(placette_max) == A3["placette_max_carbone"], f"La placette {placette_max} n'est pas celle qui stocke le plus de carbone.")


# ---------------------------------------------------------------- Module 4
A4 = _A["m4"]


def _comparer_transects(s, ref, nom, tol):
    _exige(hasattr(s, "to_dict"), f"`{nom}` doit être une Series pandas indexée par transect.")
    d = {str(k): float(v) for k, v in s.to_dict().items()}
    manquants = sorted(set(ref) - set(d))
    if manquants:
        raise _Echec(f"`{nom}` n'a pas de valeur pour {len(manquants)} transect(s), par exemple {manquants[:3]}. "
                     "Un transect où l'espèce n'a pas été vue compte avec un taux de 0 : il faut le garder (reindex avec fill_value=0).")
    en_trop = sorted(set(d) - set(ref))
    _exige(not en_trop, f"`{nom}` contient des transects à exclure : {en_trop}. Sans longueur connue, on ne peut pas calculer de taux.")
    for k, v in ref.items():
        _exige(abs(d[k] - v) <= tol, f"Transect {k} : {nom} = {d[k]:.4f}, attendu ≈ {v}. Vérifie que tu divises par la longueur en km, pas en m.")


def _m4_e1(df):
    _exige(hasattr(df, "shape"), "On attend un DataFrame (résultat de pd.read_excel).")
    _exige(df.shape == (A4["n_brut"], A4["n_col"]), f"Forme {df.shape}, attendu {(A4['n_brut'], A4['n_col'])}.")


def _m4_e2(n_transects):
    _exige(int(n_transects) == len(A4["L_km"]) + len(A4["sans_fin"]), f"{n_transects} transects, ce n'est pas le bon nombre. Compte les valeurs DIFFÉRENTES de la colonne 'Transec N°' (pas le nombre de lignes).")


def _m4_e3(df):
    vus = set(df.loc[df["Types_Donnees"] == "Faune", "Espèce_Fact_Nat2"].unique())
    en_trop = sorted(vus - set(A4["especes_nat2_faune"]))
    _exige(not en_trop, f"Noms d'espèces encore non harmonisés : {en_trop}.")
    vus_h = set(df.loc[df["Espèce_Fact_Nat1"] == "Homme", "Type indice "].unique())
    en_trop = sorted(vus_h - set(A4["indices_homme"]))
    _exige(not en_trop, f"Indices humains encore en double : {en_trop}. 'Coupe machette' et 'Coupe à la machette' désignent la même chose.")


def _m4_e4(nb_doublons, df):
    if int(nb_doublons) == 0:
        raise _Echec("Tu trouves 0 doublon parce que la colonne ID est différente sur chaque ligne, même pour une saisie en double. "
                     "Cherche les doublons sur toutes les colonnes SAUF ID (paramètre subset).")
    _exige(int(nb_doublons) == A4["nb_doublons"], f"{nb_doublons} doublons, attendu {A4['nb_doublons']}.")
    _exige(len(df) == A4["n_apres_doublons"], f"{len(df)} lignes après suppression, attendu {A4['n_apres_doublons']}.")


def _m4_e5(nb_inverses, df):
    _exige(int(nb_inverses) == A4["nb_inverses"], f"{nb_inverses} lignes inversées, attendu {A4['nb_inverses']}. Au Cameroun, la longitude (vers 14-16° E) est toujours plus grande que la latitude (vers 2-3° N) dans cette zone.")
    _exige(float(df["Longitude"].min()) > 10, "Il reste des longitudes inférieures à 10° : l'inversion n'est pas corrigée.")
    _exige(float(df["Latitude"].max()) < 5, "Il reste des latitudes supérieures à 5° : l'inversion n'est pas corrigée.")


def _m4_e6(L_km, sans_fin):
    _exige(sorted(sans_fin) == A4["sans_fin"], f"Transect(s) sans point de fin : attendu {A4['sans_fin']}, tu as {sorted(sans_fin)}.")
    _comparer_transects(L_km, A4["L_km"], "L_km", 1e-6)


def _m4_e7(tr_gor):
    _comparer_transects(tr_gor, A4["tr_gor"], "tr_gor", 1e-3)


def _m4_e8(tr_gor_strate):
    _exige(hasattr(tr_gor_strate, "to_dict"), "`tr_gor_strate` doit être une Series indexée par strate.")
    d = {str(k): float(v) for k, v in tr_gor_strate.to_dict().items()}
    _exige(set(d) == set(A4["tr_gor_strate"]), f"On attend une valeur par strate : {sorted(A4['tr_gor_strate'])}.")
    for k, v in A4["tr_gor_strate"].items():
        _exige(abs(d[k] - v) <= 1e-3, f"{k} : {d[k]:.4f} nids/km, attendu ≈ {v}. Le taux d'une strate = (total des nids de la strate) / (total des km de la strate), pas la moyenne des taux des transects.")


def _m4_e9(pression):
    _comparer_transects(pression, A4["pression"], "pression", 1e-3)


def _m4_e10(nb):
    _exige(int(nb) == A4["nids_perp_manquante"], f"{nb} nids sans distance perpendiculaire, attendu {A4['nids_perp_manquante']} (compté sur toutes les lignes de nids, toutes espèces).")


# ---------------------------------------------------------------- Module 0
def _m0_e2(message):
    _exige(isinstance(message, str), f"`message` doit être un texte (entre guillemets). Tu as donné un {type(message).__name__}.")
    _exige(message == "Bonjour la forêt", f"`message` vaut {message!r}. Attendu exactement : 'Bonjour la forêt' (majuscule, accent, pas d'espace en trop).")


def _m0_e3(nb_arbres, dhp, essence, vivant):
    _exige(type(nb_arbres) is int and nb_arbres == 12, f"`nb_arbres` doit être le nombre entier 12 (type int). Tu as {nb_arbres!r} de type {type(nb_arbres).__name__}.")
    _exige(type(dhp) is float and dhp == 45.5, f"`dhp` doit être le nombre décimal 45.5 (type float). Tu as {dhp!r} de type {type(dhp).__name__}.")
    _exige(type(essence) is str and essence == "Iroko", f"`essence` doit être le texte 'Iroko' (type str). Tu as {essence!r}.")
    _exige(vivant is True, f"`vivant` doit valoir True (type bool, sans guillemets, avec une majuscule). Tu as {vivant!r} de type {type(vivant).__name__}.")


def _m0_e4(surface_m2, surface_ha):
    _exige(surface_m2 == 5000, f"Surface en m² : {surface_m2}, attendu 5000 (50 × 100). La multiplication s'écrit *.")
    _exige(_proche(surface_ha, 0.5), f"Surface en ha : {surface_ha}, attendu 0.5. Un hectare vaut 10 000 m².")


def _m0_e5(lignes_completes, reste):
    _exige(lignes_completes == 4, f"lignes_completes = {lignes_completes}, attendu 4. La division entière s'écrit // (deux barres).")
    _exige(reste == 7, f"reste = {reste}, attendu 7. Le reste d'une division s'obtient avec %.")


def _m0_e6(type_erreur, hauteur_affichee):
    _exige(isinstance(type_erreur, str) and type_erreur.strip() == "NameError", f"Le nom de l'erreur est écrit en rouge dans la dernière ligne du message. Ce n'est pas {type_erreur!r}.")
    _exige(hauteur_affichee == 30, "Une fois corrigé, le code doit afficher 30. Python distingue majuscules et minuscules : hauteur et Hauteur sont deux noms différents.")


def _m0_e7(phrase):
    att = "L'arbre Iroko mesure 45.5 cm"
    _exige(isinstance(phrase, str), "`phrase` doit être un texte.")
    _exige(phrase == att, f"Ta phrase : {phrase!r}\n   Attendue : {att!r}\n   Utilise une f-string : f\"... {{essence}} ... {{dhp}} ...\"")


def _m0_e8(propre):
    _exige(propre == "Ayous", f"Résultat : {propre!r}, attendu 'Ayous'. Il faut retirer les espaces (.strip()) ET mettre la majuscule (.capitalize()).")


def _m0_e9(valeur):
    _exige(isinstance(valeur, float), f"`valeur` doit être un nombre décimal (float). Tu as un {type(valeur).__name__} : as-tu utilisé float(...) ?")
    _exige(valeur == 34.5, f"`valeur` vaut {valeur}, attendu 34.5.")


def _m0_e10(est_gros, est_exploitable):
    _exige(est_gros is False, f"`est_gros` vaut {est_gros!r}. 45.5 >= 60 est faux : on attend False.")
    _exige(est_exploitable is False, f"`est_exploitable` vaut {est_exploitable!r}. Les deux conditions doivent être vraies (and) : on attend False.")


def _m0_e11(categorie):
    _exige(categorie == "gros", f"Pour un dhp de 72, `categorie` vaut {categorie!r}, attendu 'gros'. Vérifie l'ordre de tes conditions if / elif / else.")


def _m0_e12(total_nids):
    _exige(total_nids == 11, f"total_nids = {total_nids}, attendu 11. As-tu corrigé l'indentation pour que l'addition soit DANS la boucle ?")


def _m0_e13(premier, dernier, n, placettes):
    _exige(premier == "P01", f"premier = {premier!r}. En Python, le premier élément est à l'index 0 : liste[0].")
    _exige(dernier == "P04", f"dernier = {dernier!r}. Le dernier élément s'obtient avec l'index -1.")
    _exige(n == 4, f"n = {n}, attendu 4 (longueur AVANT l'ajout).")
    _exige(list(placettes) == ["P01", "P02", "P03", "P04", "P05"], f"placettes = {placettes}. On attend la liste avec 'P05' ajouté à la fin.")


def _m0_e14(total):
    _exige(_proche(total, 186.5), f"total = {total}, attendu 186.5. Commence à 0 et ajoute chaque hauteur dans la boucle : total = total + h.")


def _m0_e15(numeros):
    _exige(list(numeros) == list(range(1, 21)), f"On attend la liste 1, 2, …, 20. range(1, 21) s'arrête AVANT 21. Tu as {list(numeros)[:3]}…{list(numeros)[-2:] if len(list(numeros)) else ''} ({len(list(numeros))} éléments).")


def _m0_e16(d_sapelli, densites):
    _exige(d_sapelli == 0.58, f"d_sapelli = {d_sapelli}, attendu 0.58.")
    _exige(isinstance(densites, dict) and densites.get("Iroko") == 0.56, "Ajoute la clé 'Iroko' avec la valeur 0.56 au dictionnaire : densites['Iroko'] = 0.56.")
    _exige(len(densites) == 3, f"Le dictionnaire doit contenir 3 essences, il en contient {len(densites)}.")


def _m0_e17(en_metres):
    _exige(callable(en_metres), "Passe la fonction elle-même, sans parenthèses.")
    for cm in (250, 1000, 0, 35.5):
        r = en_metres(cm)
        _exige(r is not None, "Ta fonction ne renvoie rien : il manque return. (print affiche, mais ne renvoie pas.)")
        _exige(_proche(r, cm / 100), f"en_metres({cm}) renvoie {r}, attendu {cm / 100}.")


def _m0_e18(diametre):
    _exige(_proche(diametre, 2 * math.sqrt(0.5 / math.pi) * 100, 1e-6), f"diametre = {diametre}. Attendu ≈ {2 * math.sqrt(0.5 / math.pi) * 100:.2f} cm. Rayon (m) = racine(g / π), diamètre (cm) = 2 × rayon × 100.")


# ---------------------------------------------------------------- Module 5
A5 = _A["m5"]


def _m5_e1(nids):
    _exige(hasattr(nids, "shape"), "`nids` doit être un DataFrame filtré.")
    _exige(len(nids) == A5["n_groupes"], f"{len(nids)} groupes de nids, attendu {A5['n_groupes']}. Garde les nids de gorille des transects dont la longueur est connue (index de L_km).")


def _m5_e2(x):
    _exige(len(x) == A5["n_distances"], f"{len(x)} distances, attendu {A5['n_distances']}. Retire les distances manquantes avec .dropna().")
    _exige(_proche(float(x.mean()), A5["x_moy"], 1e-3), f"Distance moyenne {float(x.mean()):.3f}, attendu ≈ {A5['x_moy']} m. Les fiches sont en cm : divise par 100.")


def _m5_e3(sigma):
    _exige(_proche(sigma, A5["sigma"], 1e-3), f"sigma = {sigma}, attendu ≈ {A5['sigma']} m. Estimateur : racine carrée de la MOYENNE des distances au carré.")


def _m5_e4(esw):
    _exige(_proche(esw, A5["esw"], 1e-3), f"ESW = {esw}, attendu ≈ {A5['esw']} m. ESW = sigma × racine(π / 2).")


def _m5_e5(D_groupes):
    if _proche(D_groupes, A5["D_groupes"] / 1000, 1e-2, rel=True) or _proche(D_groupes, A5["D_groupes"] * 1000, 1e-2, rel=True):
        raise _Echec("Erreur d'unités d'un facteur 1000 : L est en km, l'ESW en m. Convertis l'ESW en km avant de diviser.")
    if _proche(D_groupes, A5["D_groupes"] * 2, 1e-2, rel=True):
        raise _Echec("Résultat 2 fois trop grand : la bande observée s'étend des DEUX côtés du transect (2 × L × ESW).")
    _exige(_proche(D_groupes, A5["D_groupes"], 1e-3, rel=True), f"D_groupes = {D_groupes}, attendu ≈ {A5['D_groupes']} groupes/km².")


def _m5_e6(D_nids):
    _exige(_proche(D_nids, A5["D_nids"], 1e-3, rel=True), f"D_nids = {D_nids}, attendu ≈ {A5['D_nids']} nids/km². Multiplie par la taille MOYENNE des groupes (colonne Nombre).")


def _m5_e7(D_ind):
    _exige(_proche(D_ind, A5["D_ind"], 1e-3, rel=True), f"D_ind = {D_ind}, attendu ≈ {A5['D_ind']} individus/km². D_ind = D_nids / (r × t).")


def _m5_e8(N_strate):
    _exige(hasattr(N_strate, "to_dict"), "`N_strate` doit être une Series indexée par strate.")
    d = {str(k): float(v) for k, v in N_strate.to_dict().items()}
    _exige(set(d) == set(A5["N_strate"]), f"On attend une valeur par strate : {sorted(A5['N_strate'])}.")
    for k, v in A5["N_strate"].items():
        _exige(abs(d[k] - v) <= max(1.0, v * 2e-3), f"{k} : {d[k]:.1f} individus, attendu ≈ {v}. N = densité de la strate × superficie de la strate (Sup_strate_km²).")


def _m5_e9(bas, haut, N_total):
    _exige(_proche(N_total, A5["N_total"], 2e-3, rel=True), f"N_total = {N_total}, attendu ≈ {A5['N_total']}.")
    _exige(bas < N_total < haut, f"Ton intervalle [{bas:.0f} ; {haut:.0f}] ne contient pas l'estimation {N_total:.0f}. Vérifie les percentiles 2.5 et 97.5.")
    _exige(0.15 * N_total < haut - bas < 3 * N_total, f"Largeur de l'intervalle : {haut - bas:.0f}. Ça ne semble pas plausible : vérifie que tu tires les TRANSECTS avec remise (replace=True) et que tu refais tout le calcul à chaque tirage.")


# ---------------------------------------------------------------- Module 6
A6 = _A["m6"]


def _m6_e1(df):
    _exige(hasattr(df, "shape") and df.shape == (A6["n_brut"], A6["n_col"]), f"Forme attendue {(A6['n_brut'], A6['n_col'])}. As-tu chargé donnees/camelot_export.csv ?")


def _m6_e2(pp):
    import pandas as pd
    for col in ["Date/Time", "Session Start Date", "Session End Date"]:
        _exige(pd.api.types.is_datetime64_any_dtype(pp[col]), f"La colonne {col!r} n'est pas au format date (type actuel : {pp[col].dtype}). Utilise pd.to_datetime().")


def _m6_e3(nb_hors, pp):
    _exige(int(nb_hors) == A6["nb_hors_session"], f"{nb_hors} photos hors session, attendu {A6['nb_hors_session']}. Une photo est hors session si elle est AVANT la date de pose ou APRÈS la date de retrait (compte le jour du retrait comme valide).")
    _exige(len(pp) == A6["n_brut"] - A6["nb_hors_session"], f"Le tableau a {len(pp)} lignes après filtrage, attendu {A6['n_brut'] - A6['nb_hors_session']}.")


def _m6_e4(effort):
    _exige(hasattr(effort, "to_dict"), "`effort` doit être une Series indexée par station.")
    d = {str(k): float(v) for k, v in effort.to_dict().items()}
    total = sum(d.values())
    if abs(total - A6["effort_naif_total"]) < 2:
        raise _Echec(f"Tu obtiens {total:.0f} jours-pièges : c'est l'effort théorique (pose → retrait). Trois caméras sont tombées en panne avant le retrait. L'effort réel s'arrête à la dernière photo prise.")
    for k, v in A6["effort"].items():
        _exige(k in d and abs(d[k] - v) < 0.6, f"Station {k} : {d.get(k)} jours, attendu {v}. Jours-pièges = (jour de la dernière photo − jour de pose) + 1.")


def _m6_e5(nb_indet, obs):
    _exige(int(nb_indet) == A6["nb_indet"], f"{nb_indet} photos 'Indéterminé', attendu {A6['nb_indet']}.")
    vus = set(obs["Species Common Name"].unique())
    _exige(vus == set(A6["especes"]), f"Espèces restantes incorrectes. En trop : {sorted(vus - set(A6['especes']))}, manquantes : {sorted(set(A6['especes']) - vus)}. "
           "Retire les photos vides (NaN) et 'Indéterminé', et harmonise les noms mal orthographiés.")
    _exige(len(obs) == A6["n_photos_id"], f"{len(obs)} photos identifiées, attendu {A6['n_photos_id']}.")


def _m6_e6(ev30):
    n = len(ev30)
    _exige(n != A6["n_photos_id"], "Tu as autant d'événements que de photos : chaque rafale compte encore plusieurs fois.")
    _exige(n == A6["n_ev30"], f"{n} événements indépendants, attendu {A6['n_ev30']}. Trie par station, espèce et date, puis garde une photo si l'écart avec la précédente (même station, même espèce) dépasse 30 minutes ou si c'est la première.")


def _m6_e7(rai):
    _exige(hasattr(rai, "to_dict"), "`rai` doit être une Series indexée par espèce.")
    d = {str(k): float(v) for k, v in rai.to_dict().items()}
    for k, v in A6["rai"].items():
        _exige(k in d and abs(d[k] - v) < 1e-3, f"{k} : RAI = {d.get(k)}, attendu ≈ {v}. RAI = événements / jours-pièges totaux × 100.")


def _m6_e8(rai_gor):
    _exige(hasattr(rai_gor, "to_dict"), "`rai_gor` doit être une Series indexée par station.")
    d = {str(k): float(v) for k, v in rai_gor.to_dict().items()}
    _exige(len(d) == len(A6["rai_gor"]), f"{len(d)} stations, attendu {len(A6['rai_gor'])}. Les stations sans gorille comptent, avec 0.")
    for k, v in A6["rai_gor"].items():
        _exige(abs(d.get(k, -1) - v) < 1e-3, f"Station {k} : {d.get(k)}, attendu ≈ {v}. Divise par l'effort DE LA STATION.")


def _m6_e9(n_ev60):
    _exige(int(n_ev60) == A6["n_ev60"], f"{n_ev60} événements avec un seuil de 60 min, attendu {A6['n_ev60']}.")


# ---------------------------------------------------------------- Module 1b (pandas)
def _arbres_ref():
    import pandas as pd
    return pd.DataFrame({
        "arbre": [f"A{i:02d}" for i in range(1, 13)],
        "placette": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        "essence": ["Ayous", "Sapelli", "Ayous", "Iroko", "Sapelli", "Ayous", "Tali", "Sapelli", "Iroko", "Ayous", "Tali", "Ayous"],
        "dhp": [42.0, 85.5, 23.4, 61.0, 51.2, 37.8, 48.2, 102.0, 55.1, 18.6, 74.3, 66.9],
        "hauteur": [28.5, 41.0, None, 36.2, 33.0, 26.4, None, 44.8, 35.0, 17.2, 38.9, 37.5],
    })


def _mp_e1(n_lignes, n_colonnes):
    _exige(n_lignes == 12 and n_colonnes == 5, f"Tu donnes {n_lignes} lignes et {n_colonnes} colonnes. arbres.shape renvoie (lignes, colonnes) : on attend 12 et 5.")


def _mp_e2(colonnes):
    _exige(list(colonnes) == ["arbre", "placette", "essence", "dhp", "hauteur"], f"On attend la liste des 5 noms de colonnes, dans l'ordre. Tu as {list(colonnes)}.")


def _mp_e3(dhps, dmax):
    _exige(hasattr(dhps, "tolist") and dhps.tolist() == _arbres_ref()["dhp"].tolist(), "`dhps` doit être la colonne dhp : arbres[\"dhp\"] (un seul crochet, avec le nom entre guillemets).")
    _exige(dmax == 102.0, f"dmax = {dmax}, attendu 102.0. Une colonne a des méthodes : .max(), .min(), .mean(), .sum()…")


def _mp_e4(sous):
    _exige(hasattr(sous, "columns") and list(sous.columns) == ["essence", "dhp"], "Pour garder plusieurs colonnes, on donne une LISTE de noms : arbres[[\"essence\", \"dhp\"]] (deux crochets).")
    _exige(len(sous) == 12, "Toutes les lignes doivent être gardées.")


def _mp_e5(gros):
    _exige(hasattr(gros, "columns"), "`gros` doit être un tableau filtré : arbres[condition].")
    _exige(sorted(gros["arbre"]) == ["A02", "A04", "A05", "A08", "A09", "A11", "A12"], f"Tu gardes {len(gros)} arbres, on en attend 7 (dhp de 50 cm ou plus). As-tu utilisé >= ?")


def _mp_e6(sel):
    _exige(hasattr(sel, "columns"), "`sel` doit être un tableau filtré.")
    _exige(sorted(sel["arbre"]) == ["A02", "A05", "A08"], f"On attend les 3 Sapelli de 50 cm ou plus, tu en as {len(sel)}. Avec pandas : & (pas and), et chaque condition entre parenthèses.")


def _mp_e7(comptes):
    _exige(hasattr(comptes, "to_dict") and comptes.to_dict() == {"Ayous": 5, "Sapelli": 3, "Iroko": 2, "Tali": 2}, "On attend le nombre d'arbres par essence : arbres[\"essence\"].value_counts().")


def _mp_e8(tri):
    _exige(hasattr(tri, "iloc"), "`tri` doit être le tableau trié.")
    _exige(list(tri["arbre"])[:3] == ["A08", "A02", "A11"], "Le tableau doit être trié du plus GROS au plus petit dhp : ascending=False.")


def _mp_e9(arbres):
    _exige("g" in arbres.columns, "Crée la colonne avec arbres[\"g\"] = ...")
    att = [math.pi * (d / 200) ** 2 for d in _arbres_ref()["dhp"]]
    _exige(all(_proche(a, b, 1e-9) for a, b in zip(arbres["g"], att)), "Valeurs de g incorrectes. Même formule qu'au module 1, appliquée à la colonne entière : np.pi * (arbres[\"dhp\"] / 200) ** 2.")


def _mp_e10(nb_nan):
    _exige(int(nb_nan) == 2, f"{nb_nan} hauteurs manquantes, on en attend 2. .isna() donne True/False par ligne, .sum() compte les True.")


def _mp_e11(propre):
    _exige(hasattr(propre, "tolist") and propre.tolist() == ["Ayous", "Sapelli", "Iroko"], f"Résultat : {list(propre) if hasattr(propre, 'tolist') else propre}. Sur une colonne de texte, les méthodes passent par .str : noms.str.strip().str.capitalize().")


def _mp_e12(releve):
    v = releve.loc[releve["placette"] == 2, "dhp"].tolist()
    if _proche(v[0], 5.12, 1e-6):
        raise _Echec("Les dhp de la placette 2 ont été divisés deux fois. Recrée `releve` en relançant la cellule depuis le début.")
    _exige(all(_proche(a, b, 1e-6) for a, b in zip(v, [51.2, 37.8, 48.2, 102.0])), f"Placette 2 : {v}. Attendu [51.2, 37.8, 48.2, 102.0]. Utilise releve.loc[condition, \"dhp\"] = releve.loc[condition, \"dhp\"] / 10.")
    autres = releve.loc[releve["placette"] != 2, "dhp"].tolist()
    _exige(autres == _arbres_ref().loc[_arbres_ref()["placette"] != 2, "dhp"].tolist(), "Les autres placettes ont été modifiées : la condition doit viser seulement la placette 2.")


def _mp_e13(moy):
    att = _arbres_ref().groupby("essence")["dhp"].mean()
    _exige(hasattr(moy, "to_dict"), "`moy` doit être le résultat d'un groupby.")
    d = moy.to_dict()
    _exige(set(d) == set(att.index) and all(_proche(d[k], att[k], 1e-6) for k in att.index), "On attend le dhp MOYEN par essence : arbres.groupby(\"essence\")[\"dhp\"].mean().")


def _mp_e14(nb_doublons, saisie_propre):
    _exige(int(nb_doublons) == 1, f"{nb_doublons} doublon(s), on en attend 1. saisie.duplicated().sum().")
    _exige(len(saisie_propre) == 12, f"Après suppression on attend 12 lignes, tu en as {len(saisie_propre)}.")


_VERIFS = {k[1:]: v for k, v in globals().items() if k.startswith("_m") and callable(v)}


def verifier(exercice, *valeurs):
    """Vérifie ta réponse à un exercice. Affiche ✅ ou ❌ avec une explication."""
    f = _VERIFS.get(exercice)
    if f is None:
        print(f"Exercice inconnu : {exercice!r}.")
        return False
    try:
        f(*valeurs)
    except _Echec as e:
        print(f"❌ {exercice} : {e}")
        print("   Besoin d'aide ? indice(\"" + exercice + "\")")
        return False
    except TypeError as e:
        print(f"❌ {exercice} : mauvais nombre ou type de valeurs passées à verifier(). Relis l'énoncé. ({e})")
        return False
    except Exception as e:  # erreur dans le code de l'étudiant
        print(f"❌ {exercice} : ton code a provoqué une erreur {type(e).__name__} : {e}")
        return False
    print(f"✅ {exercice} : correct.")
    return True


_INDICES = {
    "m1_e1": ["Une variable se crée avec un signe = : nom = valeur.", "Un texte s'écrit entre guillemets : \"Sapelli\". Un nombre décimal s'écrit avec un point : 62.5."],
    "m1_e2": ["π est disponible dans le module math : import math, puis math.pi.", "Le dhp est en cm. Le rayon en mètres vaut dhp / 200.", "Puissance en Python : x ** 2. Donc math.pi * (dhp / 200) ** 2."],
    "m1_e3": ["Trois fonctions intégrées suffisent : len(), max(), sum().", "moyenne = sum(liste) / len(liste)."],
    "m1_e4": ["Commence par une liste vide : liste_g = [].", "Parcours les diamètres avec : for d in dhps:", "Dans la boucle, calcule g pour d puis ajoute-le : liste_g.append(...)."],
    "m1_e5": ["Une condition s'écrit : if d >= 10:", "Crée une liste vide, ajoute dedans seulement les d qui passent la condition, puis compte avec len()."],
    "m1_e6": ["Une fonction : def surface_terriere(dhp): suivi d'un bloc indenté.", "La fonction doit se terminer par return suivi du résultat."],
    "m1_e7": ["Un dictionnaire : {\"Ayous\": 0.36, ...}. Accès : densites[\"Ayous\"].", "densites[\"Teck\"] plante. densites.get(\"Teck\") renvoie None."],
    "m1_e8": ["Arrondir à la dizaine inférieure : diviser par 10, garder la partie entière, remultiplier par 10.", "math.floor(47.3 / 10) * 10 donne 40. Il reste à plafonner à 120 avec min(..., 120)."],
    "m1_e9": ["Vérifie d'abord que l'essence est dans le dictionnaire : if essence not in dme: return False", "Sinon, renvoie le résultat de la comparaison dhp >= dme[essence] (c'est déjà True ou False)."],
    "m1_e10": ["Boucle sur la liste de tuples : for essence, d in arbres:", "Utilise ta fonction est_exploitable() et additionne surface_terriere(d) quand elle renvoie True."],
    "m2_e1": ["import pandas as pd, puis pd.read_csv(\"chemin/vers/le/fichier.csv\").", "Le chemin est relatif au notebook : \"donnees/inventaire_brut.csv\"."],
    "m2_e2": ["Affiche df[\"dhp\"].dtype et df.head(20).", "Cherche des valeurs contenant une virgule : df[df[\"dhp\"].astype(str).str.contains(\",\")]."],
    "m2_e3": ["Étape 1 : transformer en texte et remplacer la virgule : .astype(str).str.replace(\",\", \".\").", "Étape 2 : convertir en nombre : pd.to_numeric(...)."],
    "m2_e4": ["Regarde tous les noms : df[\"essence\"].value_counts().", "Les méthodes .str.strip() et .str.capitalize() règlent espaces et majuscules.", "Il reste des fautes : corrige-les avec .replace({\"Ayouss\": \"Ayous\", ...})."],
    "m2_e5": [".duplicated() renvoie True pour chaque ligne déjà vue. .sum() les compte.", ".drop_duplicates() les supprime."],
    "m2_e6": ["Filtrer des lignes : df = df[condition].", "La condition : df[\"dhp\"] > 0."],
    "m2_e7": ["df.groupby(\"placette\")[\"dhp\"].median() donne la médiane par placette.", "Une médiane près de 200 au lieu de 20 : ce sont des millimètres. .idxmax() renvoie la placette concernée."],
    "m2_e8": ["Sélectionne les lignes de cette placette avec df.loc[condition, \"dhp\"].", "df.loc[df[\"placette\"] == X, \"dhp\"] = df.loc[df[\"placette\"] == X, \"dhp\"] / 10. N'exécute la cellule qu'UNE fois."],
    "m2_e9": ["df[\"hauteur\"].isna() renvoie True pour chaque valeur manquante.", "Additionne ces True avec .sum()."],
    "m2_e10": ["df.to_csv(\"donnees/inventaire_propre.csv\", index=False)."],
    "m3_e1": ["Une opération sur une colonne s'applique à toutes les lignes d'un coup : df[\"dhp\"] / 200.", "Utilise np.pi et ** 2, comme au module 1."],
    "m3_e2": ["Somme par placette : df.groupby(\"placette\")[\"g\"].sum().", "Ramène à l'hectare : divise par la surface d'une placette (0.5 ha)."],
    "m3_e3": ["Nombre d'arbres par placette : df.groupby(\"placette\").size().", "Divise par 0.5 pour obtenir des tiges par hectare."],
    "m3_e4": ["groupby(\"essence\"), somme des g, puis .sort_values(ascending=False).", ".head(3).index.tolist() donne les 3 premiers noms."],
    "m3_e5": ["Classe : np.floor(df[\"dhp\"] / 10) * 10, puis .clip(upper=120).", "Médiane de la classe, ligne par ligne : df.groupby(\"classe\")[\"hauteur\"].transform(\"median\").", "Remplis les trous : df[\"hauteur\"].fillna(...)."],
    "m3_e6": ["Lis donnees/especes.csv, puis df.merge(especes, on=\"essence\", how=\"left\")."],
    "m3_e7": ["Formule de Chave et al. (2014) : AGB = 0.0673 × (ρ × D² × H)^0.976, en kg.", "En Python : 0.0673 * (densite * dhp ** 2 * hauteur) ** 0.976."],
    "m3_e8": ["Applique la fonction aux colonnes : biomasse_chave(df[\"densite_bois\"], df[\"dhp\"], df[\"hauteur\"]).", "Somme par placette, divise par 1000 (kg → t) et par 0.5 (→ par ha)."],
    "m3_e9": ["Le carbone vaut 47 % de la biomasse sèche (fraction par défaut du GIEC) : C_ha = AGB_ha * 0.47.", ".idxmax() donne la placette avec la plus grande valeur."],
    "m4_e1": ["pd.read_excel(\"donnees/transects_bruts.xlsx\") lit un fichier Excel (il faut le paquet openpyxl, présent dans Anaconda et Colab)."],
    "m4_e2": ["Une colonne a une méthode .nunique() qui compte les valeurs distinctes.", "Attention au nom exact de la colonne : df[\"Transec N°\"]."],
    "m4_e3": ["Même méthode qu'au module 2 : .str.strip() puis .replace({...}).", "Regarde df[\"Espèce_Fact_Nat2\"].value_counts() pour repérer les variantes. Attention : la colonne s'appelle \"Type indice \" avec une espace à la fin."],
    "m4_e4": ["Construis la liste des colonnes sans ID : cols = [c for c in df.columns if c != \"ID\"].", "df.duplicated(subset=cols).sum() compte, df.drop_duplicates(subset=cols) supprime."],
    "m4_e5": ["inv = df[\"Longitude\"] < df[\"Latitude\"] donne True pour les lignes inversées.", "Pour échanger : df.loc[inv, [\"Longitude\", \"Latitude\"]] = df.loc[inv, [\"Latitude\", \"Longitude\"]].values"],
    "m4_e6": ["La longueur parcourue est la 'Distance transect (m)' de la ligne dont le type d'indice est 'Fin'.", "fins = df[df[\"Type indice \"] == \"Fin\"].set_index(\"Transec N°\")[\"Distance transect (m)\"], puis divise par 1000.", "sans_fin : les transects de df[\"Transec N°\"].unique() absents de L_km.index."],
    "m4_e7": ["Filtre les nids de gorille, puis .groupby(\"Transec N°\").size().", "Les transects sans nid manquent : .reindex(L_km.index, fill_value=0) les ajoute avec 0 (et retire T27).", "Divise par L_km : pandas aligne automatiquement les transects."],
    "m4_e8": ["Additionne les nids par strate et les km par strate séparément, puis divise.", "Il te faut la strate de chaque transect : df.drop_duplicates(\"Transec N°\").set_index(\"Transec N°\")[\"Strate/site\"]."],
    "m4_e9": ["Même logique qu'à l'exercice 7, avec les lignes où Espèce_Fact_Nat1 vaut \"Homme\"."],
    "m4_e10": ["Filtre les lignes dont le type d'indice est \"Nid\", puis .isna().sum() sur la distance perpendiculaire."],
    "m0_e2": ["Un texte s'écrit entre guillemets : message = \"...\"."],
    "m0_e3": ["Entier : 12. Décimal : 45.5. Texte : \"Iroko\". Booléen : True (sans guillemets)."],
    "m0_e4": ["surface_m2 = 50 * 100", "1 ha = 10 000 m², donc surface_ha = surface_m2 / 10000."],
    "m0_e5": ["47 // 10 donne le quotient entier, 47 % 10 le reste."],
    "m0_e6": ["Exécute la cellule fournie et lis la DERNIÈRE ligne rouge : elle commence par le nom de l'erreur.", "Le message dit que le nom 'Hauteur' n'est pas défini. Compare avec le nom de la variable créée."],
    "m0_e7": ["Une f-string commence par f avant les guillemets : f\"texte {variable}\".", "phrase = f\"L'arbre {essence} mesure {dhp} cm\""],
    "m0_e8": ["On peut enchaîner les méthodes : nom.strip().capitalize()."],
    "m0_e9": ["float(\"34,5\") provoque ValueError : Python attend un point.", "Remplace d'abord la virgule : texte.replace(\",\", \".\"), puis float(...)."],
    "m0_e10": ["est_gros = dhp >= 60", "est_exploitable = (dhp >= 60) and (essence == \"Iroko\")"],
    "m0_e11": ["if dhp < 30: ... elif dhp < 60: ... else: ...", "Chaque branche contient categorie = \"...\", indentée de 4 espaces."],
    "m0_e12": ["Une ligne fait partie de la boucle si elle est décalée de 4 espaces sous le for.", "Il faut décaler la ligne total_nids = total_nids + n."],
    "m0_e13": ["premier = placettes[0], dernier = placettes[-1], n = len(placettes).", "Puis placettes.append(\"P05\"), APRÈS avoir calculé n."],
    "m0_e14": ["total = 0, puis for h in hauteurs: et dans la boucle total = total + h."],
    "m0_e15": ["numeros = list(range(début, fin)) : fin est exclue."],
    "m0_e16": ["d_sapelli = densites[\"Sapelli\"]", "densites[\"Iroko\"] = 0.56 ajoute une nouvelle clé."],
    "m0_e17": ["def en_metres(cm):\n    return ..."],
    "m0_e18": ["import math, puis math.sqrt() et math.pi.", "rayon_m = math.sqrt(g / math.pi), puis diametre = 2 * rayon_m * 100."],
    "m5_e1": ["Combine trois conditions avec & : espèce Gorille, type d'indice Nid, transect dans L_km.index (méthode .isin())."],
    "m5_e2": ["x = nids[\"Distance perpendiculaire_cm\"].dropna() / 100"],
    "m5_e3": ["Pour une fonction de détection semi-normale sans troncature, l'estimateur du maximum de vraisemblance de sigma est racine(moyenne(x²)).", "np.sqrt((x ** 2).mean())"],
    "m5_e4": ["esw = sigma * np.sqrt(np.pi / 2)"],
    "m5_e5": ["D = n / (2 × L × ESW), avec L en km et ESW en km (esw / 1000).", "n = len(nids), L = L_km.sum()."],
    "m5_e6": ["D_nids = D_groupes * nids[\"Nombre\"].mean()"],
    "m5_e7": ["D_ind = D_nids / (r * t) avec r = 1.0 et t = 90."],
    "m5_e8": ["Nombre de groupes par strate : compte par transect (reindex avec 0), puis groupby(strate).sum(). Fais pareil pour L.", "D_strate = n_strate / (2 * L_strate * esw / 1000) * taille_moy / (r * t), puis N = D_strate * superficie."],
    "m5_e9": ["Dans une boucle de 1000 tours : tire des transects avec remise, rng.choice(L_km.index, size=len(L_km), replace=True).", "Pour chaque tirage, recalcule N_total en utilisant les nids et les longueurs des transects tirés (un transect tiré deux fois compte deux fois).", "Termine avec np.percentile(resultats, [2.5, 97.5])."],
    "m6_e1": ["pd.read_csv(\"donnees/camelot_export.csv\", low_memory=False)"],
    "m6_e2": ["Pour chaque colonne de date : pp[col] = pd.to_datetime(pp[col])."],
    "m6_e3": ["hors = (pp[\"Date/Time\"] < pp[\"Session Start Date\"]) | (pp[\"Date/Time\"] > pp[\"Session End Date\"] + pd.Timedelta(days=1))"],
    "m6_e4": ["Par station : date de pose (première valeur de Session Start Date) et date de la dernière photo (max de Date/Time).", "(derniere.dt.normalize() - debut).dt.days + 1 donne des jours entiers, jour de pose compris."],
    "m6_e5": ["Une photo vide a un nom d'espèce NaN : .notna() les repère.", "Regarde pp[\"Species Common Name\"].value_counts() pour trouver les fautes d'orthographe."],
    "m6_e6": ["Trie avec .sort_values([\"Trap Station Name\", \"Species Common Name\", \"Date/Time\"]).", "Écart avec la photo précédente du même groupe : obs.groupby([station, espèce])[\"Date/Time\"].diff().", "Garde les lignes où l'écart est NaN (première photo) ou > pd.Timedelta(minutes=30)."],
    "m6_e7": ["ev30.groupby(\"Species Common Name\").size() / effort.sum() * 100"],
    "m6_e8": ["Compte les événements de gorille par station, .reindex(effort.index, fill_value=0), puis divise par effort et multiplie par 100."],
    "m6_e9": ["Refais le calcul de l'exercice 6 avec pd.Timedelta(minutes=60)."],
    "mp_e1": ["arbres.shape donne un couple (lignes, colonnes).", "n_lignes, n_colonnes = arbres.shape"],
    "mp_e2": ["arbres.columns contient les noms ; list(...) en fait une liste."],
    "mp_e3": ["Une colonne : arbres[\"dhp\"].", "Son maximum : arbres[\"dhp\"].max()."],
    "mp_e4": ["Une liste de colonnes s'écrit entre crochets, et on la met dans les crochets du tableau : arbres[[\"essence\", \"dhp\"]]."],
    "mp_e5": ["arbres[\"dhp\"] >= 50 donne une colonne de True/False.", "On met cette condition entre crochets pour garder les lignes True : arbres[arbres[\"dhp\"] >= 50]."],
    "mp_e6": ["Deux conditions avec pandas : (condition1) & (condition2), chacune entre parenthèses.", "arbres[(arbres[\"essence\"] == \"Sapelli\") & (arbres[\"dhp\"] >= 50)]"],
    "mp_e7": [".value_counts() s'applique à une colonne."],
    "mp_e8": ["arbres.sort_values(\"dhp\", ascending=False)"],
    "mp_e9": ["arbres[\"g\"] = np.pi * (arbres[\"dhp\"] / 200) ** 2 : le calcul s'applique à toutes les lignes d'un coup."],
    "mp_e10": ["arbres[\"hauteur\"].isna().sum()"],
    "mp_e11": ["noms.str.strip() retire les espaces ; enchaîne avec .str.capitalize()."],
    "mp_e12": ["Condition : releve[\"placette\"] == 2.", ".loc[lignes, colonne] sélectionne une case ou un groupe de cases ; on peut leur affecter une valeur avec =."],
    "mp_e13": ["groupby(\"essence\") regroupe, [\"dhp\"] choisit la colonne, .mean() calcule la moyenne de chaque groupe."],
    "mp_e14": ["saisie.duplicated().sum() compte, saisie.drop_duplicates() supprime."],
}

def indice(exercice, niveau=1):
    """Affiche un indice. Augmente le niveau si tu bloques encore."""
    liste = _INDICES.get(exercice)
    if not liste:
        print(f"Pas d'indice pour {exercice!r}.")
        return
    niveau = max(1, min(int(niveau), len(liste)))
    print(f"💡 Indice {niveau}/{len(liste)} : {liste[niveau - 1]}")
    if niveau < len(liste):
        print(f"   Toujours bloqué ? indice(\"{exercice}\", {niveau + 1})")
