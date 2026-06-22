# Test de résilience — Urban Data Explorer

Date : 2026-06-22 16:17:16

## Principe testé
Les endpoints `/prix_m2`, `/delinquance`, etc. lisent les fichiers Gold
(`data/Gold/*.csv`) stockés sur le filesystem du service Render, et non
la base PostgreSQL Supabase en temps réel. PostgreSQL n'est utilisé que
comme entrepôt analytique secondaire (migration ponctuelle), pas comme
dépendance critique de l'API au runtime.

## Résultat
7/7 endpoints répondent correctement.

| Endpoint | Statut HTTP | OK |
|---|---|---|
| /prix_m2 | 200 | ✅ |
| /logements_sociaux | 200 | ✅ |
| /delinquance | 200 | ✅ |
| /densite | 200 | ✅ |
| /espaces_verts | 200 | ✅ |
| /qualite_air | 200 | ✅ |
| /typologie | 200 | ✅ |

## Conclusion
L'API reste pleinement fonctionnelle indépendamment de la disponibilité
de PostgreSQL/Supabase, ce qui constitue une isolation de panne réelle :
une indisponibilité de la base de données n'affecte pas le service de
données aux utilisateurs (C1.4 — résilience face aux pannes).
