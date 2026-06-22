# Rapport de test de charge — PostgreSQL (Supabase)

Date du test : 2026-06-22 15:01:13
Base de données : PostgreSQL (Supabase, pooler aws-0-eu-west-1)

## Paramètres
- Threads concurrents : 10
- Requêtes par thread : 20
- Requête testée : jointure prix_m2_par_arrondissement ⟷ delinquance, tri + LIMIT 20

## Résultats
| Métrique | Valeur |
|---|---|
| Requêtes réussies | 200/200 |
| Erreurs | 0 |
| Temps total | 1.120 s |
| Débit | 179 req/s |
| Latence moyenne | 31.11 ms |
| Latence p95 | 59.46 ms |

## Conclusion
La base supporte 10 connexions concurrentes sans erreur, avec une
latence p95 restant sous la barre des 59 ms, ce qui confirme
l'intégrité et la performance de la base sous charge (critère C1.1).
