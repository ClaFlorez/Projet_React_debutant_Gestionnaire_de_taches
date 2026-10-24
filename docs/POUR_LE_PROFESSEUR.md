# Présentation du projet pour le professeur

## Intention pédagogique

Ce dépôt accompagne le TP « Projet React débutant - Gestionnaire de tâches ». L’étudiant progresse dans un seul projet et apprend à relier les données JavaScript, les composants React, l’état, les événements et les échanges HTTP avec une API Python.

Le sujet utilise TypeScript. La réalisation fournie utilise JavaScript avec JSX et JSDoc. Le code a été réalisé avec l’aide de Copilot ; les explications, schémas, PDF et animation ont été préparés avec l’aide de Codex. L’objectif est de pouvoir expliquer les décisions et reproduire les essais, pas seulement montrer du code généré.

## Correspondance avec les exigences

| Étape | Élément attendu | Réalisation consultable |
|---|---|---|
| 0 | Un projet React conservé au fil des exercices | package.json, Vite et src/main.jsx |
| 1 | Objets, tableau, filter et length | javascript-basics.js |
| 2 | TaskHeader et App | src/App.jsx |
| 3 | TaskItem, prop task et état tasks | src/App.jsx et commentaires JSDoc |
| 4 | Formulaire contrôlé et ajout | TaskForm, handleSubmit et addTask |
| 5 | Statut, filtre, map et key | toggleTask, remainingOnly et visibleTasks |
| 6 | Effet sur le titre de l’onglet | useEffect dépendant de remainingCount |
| 7 | GET et CORS dans FastAPI | api/main.py |
| 8 | fetch, loading et error | effet de chargement dans App |
| 9 | POST, PATCH et DELETE | routes Python, request et callbacks React |

## Supports disponibles

- [Corrigé détaillé par étape](PARCOURS_CORRIGE.md)
- [Réponses aux questions du sujet](QUESTIONS_REPONSES.md)
- [PDF illustré avec code en annexe](TP_React_corrige.pdf)
- [Vidéo et scénario](../media/SCENARIO.md)
- [Captures et protocole de test](TESTS_ET_PREUVES.md)
- [Résultats des contrôles de l’archive](VALIDATION.md)

## Questions à poser pendant la présentation

1. À quel endroit la liste est-elle détenue dans React ? Et dans Python ?
2. Comment le clic de l’enfant atteint-il le parent ?
3. Pourquoi le filtre ne supprime-t-il pas les tâches terminées ?
4. Quelle requête part lorsqu’on crée une tâche ? Quel est son corps ?
5. Pourquoi setTasks est-il placé après une réponse réussie ?
6. Que reste-t-il après un rechargement de React ? Après un redémarrage de l’API ?
7. Pourquoi voit-on 404 sur `/`, mais 200 sur `/tasks` ?

## Démonstration courte proposée

Lancer les deux serveurs. Lire les deux tâches. Ajouter une tâche depuis React. Recharger React pour vérifier que l’API la restitue. Changer son statut, filtrer, retirer le filtre, puis supprimer seulement cette tâche de démonstration. Montrer les méthodes dans les outils réseau ou dans /docs. Terminer en expliquant la limite de la RAM.

## Portée des preuves

Les captures correspondent à des moments successifs de la séance. Les essais API dans /docs sont visibles. La première capture React précède les boutons finaux. Les déclarations de réussite de l’utilisateur sont distinguées des captures et des tests automatiques. La validation automatisée de l’API ne prouve pas à elle seule les interactions dans le navigateur.

## Limites assumées

Cette version reste un exercice local : stockage en mémoire, absence d’authentification, validation métier minimale et absence de gestion avancée des requêtes concurrentes. Le dépôt ne prétend pas être une application de production.
