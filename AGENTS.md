# AGENTS.md - Règles du second cerveau

Ce fichier est lu automatiquement par plusieurs outils IA au démarrage dans ce vault. Les règles s'appliquent à TOUTE IA qui consulte ce vault, quel que soit l'outil.

## Règles absolues

1. Lecture intégrale obligatoire : toute note consultée se lit EN ENTIER, jamais partiellement
2. Jamais de tirets longs : ni em-dash, ni en-dash - seul le tiret simple est autorisé
3. Frontmatter normalisé : tags (liste), statut, derniere-maj AAAA-MM-JJ
4. Marqueurs de confiance : [F] fait, [C] calcul, [D] déduction, [H] hypothèse, [I] inconnu - ne jamais élever une déduction au rang de fait, écrire INCONNU si non mesurable
5. Journalisation : toute session qui a produit décision/constat/chiffre = ligne datée dans la note concernée
6. Todo quotidienne : lire la Todo list en début de session, cocher uniquement ce qui est prouvé, adapter le reste
7. Snapshot vs concept : chiffres datés dans les suivis, règles durables dans les concepts
8. Commit PUIS push : rien n'existe tant que ce n'est pas poussé

## Le rythme

- Chaque session : todo -> travail -> journalisation -> commit + push
- Revue hebdo : tri des captures, journaux, chiffres, décisions
- Audit avant commit : liens morts, orphelins, stale, tirets (scripts/audit-vault.py)

## Ne jamais

- Inventer un chiffre, un fait ou une note "pour faire joli"
- Laisser une case cochée sans preuve
- Faire une démarche externe sans feu vert
- Laisser un commit non poussé
