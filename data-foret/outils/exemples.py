"""Petits jeux de données des modules de prise en main (1b, 2b, 3b, 5b).

Ils sont volontairement minuscules pour que tu puisses vérifier chaque résultat à l'œil.
"""
import pandas as pd


def arbres():
    """12 arbres de 3 placettes."""
    return pd.DataFrame({
        "arbre": [f"A{i:02d}" for i in range(1, 13)],
        "placette": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        "essence": ["Ayous", "Sapelli", "Ayous", "Iroko", "Sapelli", "Ayous", "Tali", "Sapelli", "Iroko", "Ayous", "Tali", "Ayous"],
        "dhp": [42.0, 85.5, 23.4, 61.0, 51.2, 37.8, 48.2, 102.0, 55.1, 18.6, 74.3, 66.9],
        "hauteur": [28.5, 41.0, None, 36.2, 33.0, 26.4, None, 44.8, 35.0, 17.2, 38.9, 37.5],
    })


def especes():
    """Densité du bois de 3 essences (le Tali manque volontairement)."""
    return pd.DataFrame({"essence": ["Ayous", "Sapelli", "Iroko"], "densite_bois": [0.36, 0.58, 0.56]})


def transects():
    """18 lignes de fiche de transects : 5 transects, un doublon, une coordonnée inversée."""
    lignes = [
        (1, "T1", "Parc", "Debut", None, 0, 14.50, 2.300),
        (2, "T1", "Parc", "Nid", "Gorille", 350, 14.50, 2.303),
        (3, "T1", "Parc", "Crotte", "Eléphant", 820, 14.50, 2.307),
        (4, "T1", "Parc", "Nid", "Gorille", 1400, 14.50, 2.313),
        (5, "T1", "Parc", "Fin", None, 2000, 14.50, 2.318),
        (6, "T2", "Parc", "Debut", None, 0, 14.62, 2.410),
        (7, "T2", "Parc", "Crotte", "Eléphant", 600, 2.415, 14.62),
        (8, "T2", "Parc", "Fin", None, 1500, 14.62, 2.424),
        (9, "T3", "Tampon", "Debut", None, 0, 14.80, 2.200),
        (10, "T3", "Tampon", "Piège", "Homme", 300, 14.80, 2.203),
        (11, "T3", "Tampon", "Nid", "Gorille", 900, 14.80, 2.208),
        (12, "T3", "Tampon", "Fin", None, 2000, 14.80, 2.218),
        (13, "T4", "Tampon", "Debut", None, 0, 14.90, 2.250),
        (14, "T4", "Tampon", "Piège", "Homme", 1100, 14.90, 2.260),
        (15, "T4", "Tampon", "Fin", None, 2500, 14.90, 2.272),
        (16, "T5", "Tampon", "Debut", None, 0, 15.00, 2.300),
        (17, "T5", "Tampon", "Fin", None, 1000, 15.00, 2.309),
        (18, "T1", "Parc", "Nid", "Gorille", 1400, 14.50, 2.313),
    ]
    return pd.DataFrame(lignes, columns=["ID", "Transect", "Strate", "Type", "Espece", "Position_m", "Longitude", "Latitude"])


def photos():
    """11 photos de 2 pièges photographiques, dont une photo vide et une date réinitialisée en 2000."""
    return pd.DataFrame({
        "station": ["CT1"] * 6 + ["CT2"] * 5,
        "espece": ["Gorille", "Gorille", "Gorille", "Potamochère", "Potamochère", None,
                   "Céphalophe bleu", "Céphalophe bleu", "Céphalophe bleu", "Céphalophe bleu", "Pangolin géant"],
        "date": ["2026-02-01 08:10:00", "2026-02-01 08:12:30", "2026-02-01 09:05:00", "2026-02-01 23:40:00", "2026-02-02 00:05:00", "2026-02-05 14:00:00",
                 "2026-02-03 10:00:00", "2026-02-03 10:20:00", "2026-02-03 11:30:00", "2000-01-01 03:12:00", "2026-02-04 02:15:00"],
    })


def sessions():
    """Dates de pose et de retrait des 2 pièges."""
    return pd.DataFrame({"station": ["CT1", "CT2"], "pose": ["2026-01-30", "2026-01-31"], "retrait": ["2026-03-01", "2026-03-02"]})
