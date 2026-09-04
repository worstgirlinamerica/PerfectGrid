<p align="center">
  <img src="assets/icon.png" width="80" alt="Perfect Grid">
  <h1 align="center">Perfect Grid</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid" alt="GitHub Release">
  <img src="https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total" alt="Téléchargements">
  <img src="https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid" alt="Licence">
</p>

Perfect Grid est une application de bureau gratuite et open source permettant de créer des planches contact vidéo et des vignettes d'aperçu à partir de fichiers vidéo locaux. Importez une vidéo, choisissez votre mise en page et exportez une planche contact au format PNG de haute qualité.

Conçue pour les monteurs, les collectionneurs, les archivistes et tous ceux qui souhaitent obtenir un résumé visuel rapide d'une vidéo.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Exemple de feuille de prévisualisation créée avec Perfect Grid">
  <br>
  <em>Exemple de feuille de contact générée avec Perfect Grid.</em>
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-macos-universal.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?logo=apple&logoColor=white" alt="Télécharger pour macOS">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Windows-x86_64.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?logo=windows11&logoColor=white" alt="Télécharger pour Windows">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Linux-x86_64.AppImage">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?logo=linux&logoColor=white" alt="Télécharger pour Linux">
  </a>
</p>

## Fonctionnalités

- Génération de planches contact de haute qualité avec affichage avancé des métadonnées vidéo (résolution, codecs, durée, taille de fichier, etc.)
- Mises en page de grille entièrement personnalisables
- Superposition optionnelle du timecode
- Sélection intelligente des images avec **Refine Picks**
- Enregistrement et réutilisation de préréglages personnalisés
- Traitement par lots
- Fonctionne sous Windows, macOS et Linux
> Si vous rencontrez __une quelconque__ erreur, si quelque chose ne fonctionne pas ou si vous avez des questions, veuillez créer un [ticket](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) pour le signaler.

## Localisation

L'interface utilisateur de l'application est disponible en 8 langues. L'affichage des noms de fichiers sur les feuilles est géré par un système distinct : les noms de fichiers sont dessinés sous forme de pixels sur le fichier PNG exporté, ce qui nécessite une gestion des polices spécifique au script.

| Langue | Interface utilisateur | Sur la feuille |
|---|---|---|
| Anglais | Oui | Oui |
| Chinois (中文) | Oui | Oui (macOS, Windows) |
| Portugais (PT) | Oui | Oui |
| Espagnol (ES) | Oui | Oui |
| Japonais (JA) | Oui | Oui (macOS, Windows) |
| Français (FR) | Oui | Oui |
| Allemand (DE) | Oui | Oui |
| Coréen (KO) | Oui | Oui (macOS, Windows) |
| Arabe / RTL | — | Oui |
| Hébreu | — | — |
| Thaï | — | — |
| Devanagari (hindi, etc.) | — | — |

> L'affichage des noms de fichiers non ASCII sous Linux n'est actuellement pas pris en charge — les noms de fichiers en scripts non latins s'afficheront sous forme de carrés. Ce problème sera corrigé dans la prochaine version !

## Utilisation de base

1. Ouvrez Perfect Grid.
2. Faites glisser une vidéo dans la fenêtre.
3. Ajustez la disposition et le style de la grille. Si vous modifiez la disposition, cliquez sur **Actualiser l’aperçu** pour régénérer les vignettes.
4. Les aperçus sont volontairement de qualité inférieure — les exportations utilisent toujours le paramètre de qualité que vous avez sélectionné.
5. (Facultatif) Sous l’onglet **Plage**, utilisez **Affiner la sélection** pour une sélection plus précise des images.
6. Choisissez une qualité d’exportation sous **Plage** : **Rapide (1080p)**, **Détail (1440p)** ou **Maximum (4K)**.
7. Cliquez sur **Exporter au format PNG**.

## Installation

Téléchargez la dernière version pour votre système d’exploitation depuis la page [Versions](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest).

### macOS

1. Téléchargez `PerfectGrid-v0.1.2-macos-universal.zip`.
2. Double-cliquez pour l'extraire, puis faites glisser Perfect Grid dans le dossier Applications.
3. Ouvrez `Perfect Grid.app`.

> macOS bloquera l'application lors du premier lancement car elle n'est pas signée. Cliquez avec le bouton droit → **Ouvrir** → **Ouvrir** pour contourner ce blocage. Si l’application ne s’ouvre toujours pas, exécutez la commande suivante dans Terminal : `xattr -cr "/Applications/Perfect Grid.app"`

### Windows

1. Téléchargez `PerfectGrid-v0.1.2-Windows-x86_64.zip`.
2. Clic droit → **Extraire tout**, puis ouvrez le dossier.
3. Double-cliquez sur `Perfect Grid.exe`.

> Windows SmartScreen peut vous avertir car l’application n’est pas signée. Cliquez sur **Plus d’informations** → **Exécuter quand même**.

### Linux

1. Téléchargez `PerfectGrid-v0.1.2-Linux-x86_64.AppImage`.
2. Rendez-le exécutable et lancez-le :
```bash
chmod +x PerfectGrid-v0.1.2-Linux-x86_64.AppImage
./PerfectGrid-v0.1.2-Linux-x86_64.AppImage
```

Aucune installation n’est nécessaire : FFmpeg et toutes les dépendances sont incluses. Fonctionne sur la plupart des distributions x86_64 (Ubuntu 22.04 et versions ultérieures, Fedora, Arch, etc.).

> Si vous obtenez une erreur FUSE : `sudo apt install fuse` (Debian/Ubuntu) ou `sudo dnf install fuse` (Fedora).

## Confidentialité

Tout s’exécute localement. Pas d’analyse, pas de télémétrie, pas de transfert de données. FFmpeg et FFprobe sont intégrés.

## Remarques

- Prend en charge les formats MP4, MOV, MKV, AVI, WebM et tout ce que FFmpeg peut lire.
- Le décodage AV1 et VP9 peut être lent sur du matériel ancien.
- Les versions pour macOS ne sont pas signées — voir la remarque d’installation ci-dessus.

<details>
<summary>Pour les développeurs</summary>

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

Pour une prise en charge complète des noms de fichiers en arabe/RTL lors de l’exécution à partir du code source :

```bash
pip install arabic-reshaper python-bidi
```

Les scripts de compilation se trouvent dans le répertoire `scripts/`. GitHub Actions compile automatiquement les versions Windows et Linux lors des poussées (push) avec balise. La version macOS est compilée manuellement.

</details>

## Contribuer

Merci de nous signaler tout bug ou erreur en créant un [ticket](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) 
Les informations les plus utiles à fournir sont votre système d’exploitation, le format vidéo concerné, ainsi que le module dans lequel le problème s’est produit (aperçu, affinage, exportation ou traitement par lots).

Consultez le fichier [CONTRIBUTING.md](CONTRIBUTING.md) pour plus d’informations.

## Licence

MIT. Consultez le fichier [LICENSE](LICENSE).
