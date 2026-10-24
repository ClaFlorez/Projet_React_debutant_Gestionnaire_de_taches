# Validation de l’archive

Contrôles exécutés le 24 octobre 2026 sur la copie destinée au dépôt. Les captures historiques sont présentées séparément dans TESTS_ET_PREUVES.md.

| Contrôle | Résultat |
|---|---|
| npm ci | 145 paquets installés, audit sans vulnérabilité signalée |
| npm run lint | Réussi |
| npm run build | Réussi, 18 modules transformés |
| node javascript-basics.js | Affiche Lire le rapport puis 1 |
| GET isolé | 200 et caractères accentués vérifiés |
| POST isolé | 201 et tâche créée |
| PATCH isolé | 200, done modifié et titre conservé |
| DELETE isolé | 200, puis absence confirmée par GET |
| Identifiant absent | 404 |
| Création sans titre | 422 |
| Précontrôle CORS | Origine localhost:5173 autorisée |
| Décodage du MP4 | Réussi, sans erreur de décodage |
| PDF | 22 pages rendues et vérifiées visuellement, avec les essais React finaux |
| React POST puis rechargement | Tâche de validation retrouvée après GET |
| React PATCH | Tâche barrée et compteur réduit |
| React filtre | Tâche terminée masquée puis réaffichée en retirant le filtre |
| React DELETE puis rechargement | Tâche de validation absente ; tâche existante conservée |
| GitHub Actions | Installation, lint, build et tests HTTP réussis sur le premier commit |

La vérification locale JavaScript a utilisé Node 22.12.0 et npm 11.1.0. ESLint 10 signale une exigence Node 22.13+ malgré la réussite du lint ; le README recommande donc 22.13+ ou 24+. Le workflow utilise Node 22 à jour. Vite résolu par le package-lock est 8.3.5.

Les tests API utilisent les versions Python installées dans l’environnement de classe : FastAPI 0.162.0, Uvicorn 0.54.0 et Pydantic 2.14.1. Ils démarrent un serveur temporaire distinct de l’instance de classe.

Le cycle React a ensuite été réalisé dans le navigateur sur localhost:5173 et documenté par quatre nouvelles captures. Seule la tâche temporaire Test de validation du TP a été modifiée et supprimée. Vérifier les alertes est restée présente et non terminée. Ces essais complètent les tests HTTP isolés.

Premier workflow GitHub réussi : https://github.com/ClaFlorez/Projet_React_debutant_Gestionnaire_de_taches/actions/runs/40110927312
