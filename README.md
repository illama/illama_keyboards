# Illama Keyboards Manager

**Illama Keyboards Manager** est une application Windows tout-en-un permettant de gérer les langues système, les configurations de clavier, les périphériques audio, et même de désinstaller les applications installées, y compris celles souvent protégées comme Edge.

## 🚀 Fonctionnalités

- 🌐 **Gestion des langues et claviers**
  - Sélection d’une langue et d’un type de clavier parmi une vaste base internationale.
  - Détection automatique du clavier utilisé à partir de quelques touches.
  - Application directe via PowerShell avec élévation automatique des privilèges.

- 🔊 **Gestion des périphériques audio**
  - Liste des périphériques d'entrée (microphones) et de sortie (haut-parleurs, casques).
  - Désactivation ou restauration des périphériques.
  - Sauvegarde des périphériques désactivés localement.

- 🗑️ **Désinstallation des applications**
  - Liste des applications installées (Win32 et UWP).
  - Recherche dynamique par nom.
  - Désinstallation via commande système ou suppression manuelle.
  - Support spécial pour Microsoft Edge.

## 📦 Installation

1. Assurez-vous d’avoir **Python 3.9+** installé sur Windows.
2. Cloner ce dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/illama-keyboards-manager.git
   cd illama-keyboards-manager
   ```

3. Installez les dépendances (facultatif, `tkinter` et `ctypes` sont intégrés) :

   ```bash
   pip install -r requirements.txt
   ```

4. Exécutez l'application :

   ```bash
   python clavier_manager.py
   ```

> ⚠️ L'application s’auto-élèvera avec les privilèges administrateur pour fonctionner correctement.

## 🖼️ Interface

L’application propose trois onglets :
- **Claviers** : choix de la langue et clavier, détection automatique.
- **Gestion audio** : désactivation/restauration des périphériques audio.
- **Apps** : désinstallation propre ou forcée de programmes.

## 📁 Structure du projet

```
clavier_manager.py               # Script principal
disabled_audio_devices.json      # Fichier généré localement pour mémoriser les périphériques désactivés
```

## 🔐 Privilèges requis

Certaines opérations (modification de la langue système, désactivation de périphériques, désinstallation) nécessitent les droits administrateur. L'application s'auto-relance avec élévation UAC.

## 📝 Licence

Ce projet est open-source sous licence MIT. Voir [LICENSE](LICENSE).

---
