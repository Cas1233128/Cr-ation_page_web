# Socle OS : architecture et feuille de route

> Statut : **aperçu d'interface** (`../preview/index.html`). Aucun noyau, aucun pilote, aucune image installable n'existe encore.

## 1. Ce qui est réaliste

Écrire un système d'exploitation « from scratch » (noyau, pilotes, pile réseau, système de fichiers) au niveau de Windows, macOS ou Linux représente des milliers d'années-personne. Ce n'est pas un projet pour une personne ou une petite équipe.

Socle est donc conçu comme **une distribution Linux opinionnée** :

- on réutilise le noyau Linux et les briques éprouvées ;
- on se différencie par la **configuration de sécurité par défaut**, **l'image système atomique**, **l'isolation obligatoire des applications** et **une interface pensée pour apprendre**.

C'est la même démarche que ChromeOS, SteamOS ou Fedora Silverblue : ils sont uniques par leur assemblage et leur expérience, pas par leur noyau.

## 2. Ce qu'on prend, ce qu'on évite

| Système | Force reprise | Faiblesse évitée |
|---|---|---|
| Windows | Compatibilité matérielle, interface accessible aux débutants | Compte admin par défaut, fenêtres UAC « Oui/Non » sans contexte, surface d'attaque héritée |
| macOS / iOS | Volume système scellé et signé, apps signées et isolées, permissions caméra/micro explicites | Écosystème fermé, iOS très verrouillé pour les développeurs |
| Linux / Ubuntu | Ouvert, outils de dev natifs, gestion de paquets | Culture du `sudo` pour tout, isolation des apps inégale, système modifiable en place (une mise à jour ratée casse le poste) |

## 3. Architecture cible

```
┌─────────────────────────────────────────────────────────┐
│ Interface Socle (shell Wayland) · mode Guidé / Expert    │
├─────────────────────────────────────────────────────────┤
│ Apps Flatpak isolées + portails │ Conteneurs de dev     │
│ (permissions visibles, révocables) │ (toolbox/distrobox) │
├─────────────────────────────────────────────────────────┤
│ Centre de sécurité · journal d'audit · labo cyber (VM)  │
├─────────────────────────────────────────────────────────┤
│ Image système atomique en lecture seule (bootc/OSTree)  │
│ SELinux appliqué · pare-feu entrant fermé · Landlock    │
├─────────────────────────────────────────────────────────┤
│ Noyau Linux (lockdown) · Secure Boot + UKI · TPM2/LUKS2 │
└─────────────────────────────────────────────────────────┘
```

| Brique | Choix | Pourquoi |
|---|---|---|
| Base | Fedora en mode image (bootc) | Mises à jour atomiques et retour arrière intégrés, images construites comme des conteneurs OCI |
| Démarrage | UEFI Secure Boot, image noyau unifiée (UKI) | Chaîne de démarrage vérifiée |
| Disque | LUKS2, clé scellée dans le TPM2 (`systemd-cryptenroll`) | Chiffrement sans saisie pénible, protégé contre la modification du démarrage |
| Contrôle d'accès | SELinux en mode appliqué | Confinement des services système |
| Apps graphiques | Flatpak + portails XDG | Isolation et permissions par application |
| Outils de dev | Toolbox ou Distrobox | Installer compilateurs et bibliothèques sans toucher au système |
| Affichage | Wayland | Isolation entre fenêtres (X11 laisse une app lire le clavier des autres) |
| Labo cyber | VM KVM/libvirt sur réseau isolé | Les outils offensifs ne sortent jamais du périmètre |

## 4. Ce que l'aperçu simule

| Fonction | Dans l'aperçu | Dans la vraie version |
|---|---|---|
| Démarrage vérifié | Texte animé | Secure Boot + mesures TPM |
| Lecture seule du système | `/etc`, `/usr`, `/lab` refusent l'écriture | Image bootc montée en lecture seule |
| `sudo` contextualisé | Fenêtre qui explique la demande, journal d'audit | Agent polkit personnalisé |
| Paquets signés | `installer crack-…` est rejeté | Vérification des signatures par le dépôt |
| Scan limité au labo | Regex sur 10.13.37.0/24 | Espace de noms réseau + règles nftables : l'outil n'a physiquement pas de route vers l'extérieur |
| Mode guidé | Explications, suggestions de commandes, alias Windows (`dir` → `ls`) | Module du shell + aide intégrée |

## 5. Feuille de route

| Phase | Livrable | Effort estimé (1 personne compétente) |
|---|---|---|
| 0 | Aperçu interactif (fait) | - |
| 1 | Image bootc installable en VM : base Fedora, GNOME ou KDE, durcissement, Flatpak par défaut | 1 à 2 mois |
| 2 | Centre de sécurité réel (app GTK/Qt ou web locale) branché sur firewalld, Flatpak, polkit | 2 à 4 mois |
| 3 | Mode guidé du terminal (extension de shell : explications, corrections) | 1 à 2 mois |
| 4 | Labo cyber : VM préconfigurées, réseau isolé, exercices | 2 à 3 mois |
| 5 | Shell graphique propre à Socle | 6 mois et plus |

Ces estimations sont des ordres de grandeur, pas des engagements.

## 6. Risques à regarder en face

1. **Différenciation.** Fedora Silverblue, Bluefin (Universal Blue), Kali et Parrot couvrent déjà une grande partie de ce terrain. Il faut une réponse claire à « pourquoi pas Bluefin + un labo ? ».
2. **Maintenance.** Une distribution doit publier des correctifs de sécurité pendant des années. Sans équipe, c'est le premier point de rupture.
3. **Pilotes.** Le matériel exotique (Wi-Fi, GPU Nvidia, imprimantes) sera la première source de plaintes.
4. **Public double.** Débutants et analystes en cybersécurité veulent des réglages opposés (garde-fous contre accès brut). Le mode Guidé/Expert est une hypothèse à tester avec de vrais utilisateurs.

## 7. Sources

- Fedora bootc : https://docs.fedoraproject.org/en-US/bootc/
- Flatpak (isolation, portails) : https://docs.flatpak.org/
- Toolbx : https://containertoolbx.org/
- Landlock (noyau Linux) : https://docs.kernel.org/userspace-api/landlock.html
- systemd-cryptenroll (TPM2) : https://www.freedesktop.org/software/systemd/man/latest/systemd-cryptenroll.html
- Volume système signé d'Apple : https://support.apple.com/guide/security/signed-system-volume-security-secd698747c9/web
- Universal Blue / Bluefin (concurrent direct) : https://projectbluefin.io/
