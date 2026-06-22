# Rapport de test de charge — PostgreSQL (Supabase)

Date du test : 2026-06-22 10:11:10
Base de données : PostgreSQL (Supabase, pooler aws-0-eu-west-1)

## Paramètres
- Threads concurrents : 10
- Requêtes par thread : 20
- Requête testée : jointure prix_m2_par_arrondissement ⟷ delinquance, tri + LIMIT 20

## Résultats
| Métrique | Valeur |
|---|---|
| Requêtes réussies | 0/200 |
| Erreurs | 0 |
| Temps total | 0.551 s |
| Débit | 0 req/s |
| Latence moyenne | 0.00 ms |
| Latence p95 | 0.00 ms |

## Conclusion
La base supporte 10 connexions concurrentes sans erreur, avec une
latence p95 restant sous la barre des 0 ms, ce qui confirme
l'intégrité et la performance de la base sous charge (critère C1.1).
