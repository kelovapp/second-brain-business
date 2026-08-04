# Second Brain Business - La bibliothèque de livres business pilotée par l'IA

Le point de départ complet pour construire **ton** second cerveau business : un vault Obsidian que n'importe quelle IA peut piloter (lecture, écriture, journalisation, commit) et qui accumule du savoir fiable sur les livres business - offres, acquisition, modèles économiques, bootstrapping - au lieu de fiches de lecture mortes.

> Basé sur un système éprouvé en production : projets en ligne, décisions documentées, chiffres vérifiés.

## Démarrage en 5 minutes

1. **Fork ou clone** ce repo : `git clone https://github.com/kelovapp/second-brain-business.git`
2. **Ouvre `PROMPT.md`** et colle-le à ton IA préférée (opencode, Claude, etc.)
3. **Ouvre le dossier dans Obsidian** (gratuit, local) - c'est ta fenêtre sur le vault ; l'IA travaille sur les fichiers, toi tu lis et navigues
4. **L'IA construit le vault** : structure, règles, premier commit
5. **Tu valides, tu enrichis** - c'est ton vault, elle exécute
6. Au bout d'une semaine : le système tourne, la mémoire grossit, les décisions sont documentées

## Ce que contient le template

| Fichier / dossier | Rôle |
|---|---|
| `PROMPT.md` | LE prompt à coller à l'IA (règles, structure, rythme, premier jour) |
| `AGENTS.md` | Les règles machine condensées (lues automatiquement par plusieurs outils) |
| `_Templates/` | 9 modèles : Accueil, Todo list, Captures, Projets (index), Projet, Concepts (index), Revue hebdo, Livre, Apprentissages de lecture |
| `scripts/audit-vault.py` | Audit de santé (liens morts, orphelins, stale, tirets) |
| `scripts/extract_book.py` + `scripts/split_chunks.py` | La chaîne bible : extraire un PDF/EPUB et le découper en chunks pour générer une bible de livre (sous-tâches IA) |
| `.obsidian/` | Thème Cupertino inclus (dark par défaut) - la même interface sobre |
| `Projets/` `Concepts/` `Livres/` `Revues/` `Captures/` `Archives/` | La charpente prête (Livres = 6 bibles exhaustives déjà incluses) |

## La bibliothèque business incluse (~58 000 mots)

| Livre | Auteur | Ce que tu en tires |
|---|---|---|
| `$100M Offers` | Alex Hormozi | La Value Equation, le Grand Slam Offer, construire une offre irrésistible |
| `$100M Leads` | Alex Hormozi | La Rule of 100, le cold outreach, trouver des clients en masse |
| `$100M Money Models` | Alex Hormozi | Les modèles économiques, la monétisation, le pricing |
| `The $150M Secret` | Guillaume Moubeche | Le bootstrapping, la profitabilité, le "Marco Polo principle" |
| `The Almanack of Naval Ravikant` | Eric Jorgenson | La richesse, le leverage, la philosophie du désir |
| `Can't Hurt Me` | David Goggins | Le mental d'exécution : la discipline comme compétence |

Chaque note est une **bible exhaustive** (chapitre par chapitre, citations verbatim, frameworks utilisables sans le livre) - régénérée ou enrichie via le skill `livre-bible`. Les prochains livres : fork ce repo, ajoute les notes, fais une PR, ou ouvre une issue.

## Les principes qui rendent le système fort

1. **La confiance avant la quantité** : des marqueurs [F] fait, [C] calcul, [D] déduction, [H] hypothèse, [I] inconnu - mieux vaut "je ne sais pas" qu'une note qui invente
2. **Le rythme avant l'effort** : 10 minutes par jour de rituel battent 5 heures une fois par mois
3. **L'IA exécute, tu décides** : elle écrit, journalise, committe - toi tu valides, tu orientes, tu tranches
4. **La traçabilité** : chaque décision a sa ligne datée - dans 6 mois, tu sauras pourquoi tu as fait ce que tu as fait
5. **Le commit est une sauvegarde** : rien n'existe tant que ce n'est pas poussé

## Licence

Libre d'utilisation, de modification et de redistribution - c'est fait pour être copié.

Si ce template t'a fait gagner du temps, un café est le bienvenu : [buymeacoffee.com](https://buymeacoffee.com/jonasfarny) ☕

---

*Template pour accumuler du savoir business fiable : chaque livre devient une bible exploitable, chaque décision une ligne datée.*
