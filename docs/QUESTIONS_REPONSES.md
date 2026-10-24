# Questions et réponses pour expliquer le TP

## Quelle est la différence entre tableau et objet

Un tableau regroupe des éléments dans un ordre. Un objet regroupe des propriétés nommées. tasks est un tableau ; chaque tâche est un objet avec id, title et done.

## Qu’est ce qu’un composant et pourquoi une majuscule

Un composant React est une fonction qui décrit une partie de l’interface. En JSX, la majuscule distingue le composant d’une balise HTML native.

## Une prop vient elle du parent ou de l’enfant

Du parent. App fournit task et des callbacks à TaskItem. TaskItem peut appeler un callback pour signaler un clic.

## À quoi sert useState

À conserver une valeur entre les rendus et à demander un nouveau rendu avec le setter. Modifier une variable JavaScript ordinaire n’assure pas une actualisation de l’interface.

## À quoi servent onChange onSubmit et preventDefault

onChange reçoit les changements de saisie. onSubmit reçoit la soumission du formulaire. preventDefault empêche le rechargement HTML habituel du formulaire. trim et le test de chaîne vide évitent les titres vides dans l’interface.

## Quelle est la différence entre map et filter

map produit une valeur pour chaque élément. filter conserve seulement les éléments qui respectent une condition. Les deux construisent un nouveau tableau. Le filtre d’affichage ne supprime rien sur le serveur.

## Pourquoi utiliser task.id comme key

Parce que React a besoin d’une identité stable pour associer les éléments d’une liste entre les rendus. Une position peut changer après suppression ou filtrage.

## Pourquoi modifier document.title dans useEffect

Le titre de l’onglet appartient au navigateur, en dehors de l’arbre JSX. L’effet synchronise cet élément extérieur avec remainingCount.

## React et FastAPI sont ils le même programme

Non. React s’exécute dans le navigateur. FastAPI est une application Python servie par Uvicorn. Pendant le développement, Vite sert aussi les fichiers de React. Les ports 5173 et 8000 séparent les services dans ce TP.

## Que signifient HTTP GET et JSON

HTTP est un protocole de requêtes et de réponses. GET demande la lecture d’une ressource. JSON est un format textuel pour échanger des données. `GET /tasks` demande la liste des tâches.

## Pourquoi utiliser await avec fetch

La réponse réseau n’est pas immédiatement disponible. await attend la promesse dans une fonction async sans bloquer le navigateur. `response.json()` attend aussi la lecture et l’analyse du corps de réponse.

## Pourquoi vérifier response.ok

fetch peut fournir une réponse HTTP 404 ou 500 sans rejeter sa promesse. response.ok indique un statut de réussite entre 200 et 299 ; le code déclenche une erreur sinon.

## Quels sont les quatre verbes du CRUD

Créer : POST. Lire : GET. Modifier partiellement : PATCH. Supprimer : DELETE. Le code attend la réussite de l’API avant de changer la liste React.

## À quoi servent CORS et les deux adresses locales

Le navigateur voit localhost:5173 et 127.0.0.1:8000 comme des origines différentes. L’API autorise l’origine React avec CORS. CORS n’est ni une authentification ni un mot de passe. localhost et 127.0.0.1 désignent ici l’ordinateur local ; le port désigne le service.

## Uvicorn est il un véritable serveur

Oui. Il reçoit les requêtes HTTP et sert l’application FastAPI. Son programme est installé sur le disque et son processus fonctionne en mémoire. La RAM n’est pas sa seule fonction : la réception et la transmission HTTP sont son rôle de serveur.

## Où se trouve le serveur et comment y accéder

Il tourne dans le processus lancé dans le terminal. L’exécutable se trouve dans `.venv/Scripts` sous Windows. On utilise `/tasks` pour les données et `/docs` pour les tests. Le serveur n’a pas un bureau de fichiers accessible par une URL `/scripts`.

## Pourquoi la racine affiche Not Found

Aucune fonction n’est associée à `/`. Le serveur répond, mais il ne connaît pas cette route. Une application pourrait ajouter une route d’accueil plus tard.

## Que veut dire Impression élégante

C’est une option du visualiseur JSON du navigateur pour ajouter des retraits et des retours à la ligne. Elle n’imprime rien et ne modifie pas les données.

## Que devient la mémoire après un arrêt

Les changements de tasks existent dans la RAM du processus Python. Recharger le navigateur relit la liste du serveur. Redémarrer le serveur recrée la liste à partir du code initial. Une base de données ou un fichier permettrait une sauvegarde durable.

## Peut on accéder au serveur à distance

Oui, avec une configuration réseau adaptée. Le lancement actuel lié à 127.0.0.1 reste local. Le projet n’ajoute ni exposition Internet, ni authentification, ni accès distant. Ce n’est pas nécessaire pour le TP.

## Quelles sont les limites de cette version

La liste n’est pas persistante. L’API n’a pas d’authentification. Les titres blancs ne sont refusés que côté formulaire. TaskUpdate accepte null, que l’interface normale n’envoie pas. Les clics répétés et les actions simultanées ne sont pas contrôlés. Le champ du formulaire est effacé avant de connaître le résultat du POST. Ces points sont documentés et conservés pour rester fidèle au projet réalisé.
