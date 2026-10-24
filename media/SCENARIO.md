# Scénario de la vidéo

Vidéo MP4 H.264, 1280 × 720 pixels, 20 images par seconde, 64 secondes. Textes en français, sans piste sonore. La métaphore compare deux programmes à deux villes reliées par une route HTTP.

| Temps | Scène | Notion |
|---|---|---|
| 00:00 à 00:08 | Deux villes qui communiquent | React et FastAPI sont distincts, mais ici sur le même PC |
| 00:08 à 00:16 | Préparer la demande | fetch et GET /tasks |
| 00:16 à 00:24 | Traverser la route | Adresse, route et HTTP |
| 00:24 à 00:32 | Recevoir la requête | Uvicorn transmet à FastAPI |
| 00:32 à 00:40 | Faire revenir la réponse | HTTP 200 et données JSON |
| 00:40 à 00:48 | Afficher les données | response.json puis setTasks |
| 00:48 à 00:56 | Les autres voyages | POST, GET, PATCH et DELETE |
| 00:56 à 01:04 | Comprendre la mémoire | RAM temporaire et absence de sauvegarde durable |

Pour une explication orale : « Le camion de l’aller représente ma requête. Le serveur reçoit la demande à l’entrée Uvicorn et l’application FastAPI la traite. Le camion revient avec une réponse contenant les tâches en JSON. React lit ces données et les affiche. »

Le MP4 est conservé dans le dépôt. Le README utilise aussi une pièce jointe GitHub pour la lecture intégrée lorsqu’elle est disponible. La documentation officielle explique [les pièces jointes vidéo](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files).
