# Expliquer le flux d’information

## 1. Mon code actuel

App possède la liste des tâches dans son état tasks. Il transmet chaque tâche à TaskItem par une prop. TaskForm possède son propre état title pour mémoriser le texte saisi.

Quand je saisis du texte, onChange appelle setTitle. Quand je soumets le formulaire, handleSubmit empêche le rechargement de la page et vérifie que le titre n’est pas vide. Il appelle ensuite onAdd, qui correspond à addTask dans App. Cette fonction appelle setTasks pour créer une nouvelle liste. React recalcule l’interface et met à jour la page. Le formulaire vide aussi son champ avec setTitle('').

Quand je clique sur une tâche, TaskItem transmet son identifiant à toggleTask par la fonction onToggle. map construit une nouvelle liste en inversant done pour la tâche choisie. setTasks déclenche la mise à jour de l’affichage.

Quand je coche le filtre, remainingOnly change. filter sélectionne les tâches non terminées pour calculer visibleTasks. La liste originale reste dans tasks. map transforme ensuite les tâches visibles en éléments affichés.

remainingCount est calculé à partir de tasks. Après l’affichage, useEffect synchronise le titre de l’onglet avec ce nombre lorsqu’il change.

## 2. La prochaine étape avec FastAPI

L’API possède déjà GET /tasks, mais mon composant React ne l’appelle pas encore. React et FastAPI sont deux programmes distincts.

Pour charger les tâches, React enverra une requête HTTP avec fetch. FastAPI renverra une réponse contenant du JSON. response.json() convertira le corps JSON en données JavaScript. setTasks enregistrera ces données dans l’état React, puis React actualisera l’affichage.

Pour le CRUD, POST créera une tâche, GET lira les tâches, PATCH modifiera une tâche et DELETE la supprimera. L’état React devra être mis à jour après une réponse réussie de l’API.

## À retenir

- Une prop est une information transmise du parent à l’enfant.
- Un état est la mémoire d’un composant. Son setter demande un nouveau rendu.
- Une fonction transmise par prop permet à l’enfant de signaler une action au parent.
- Le filtre change les tâches visibles, sans supprimer les tâches.
- Dans le code actuel, aucune base de données n’est utilisée. Les listes en mémoire se réinitialisent au rechargement de React ou au redémarrage du serveur, respectivement.

Lecture du code : src/App.jsx, src/main.jsx et api/main.py. Le PDF utilise App.tsx (TypeScript), tandis que le projet actuel utilise App.jsx (JavaScript).
