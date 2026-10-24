# Provenance et conservation des supports

## Code

Copie du dossier de classe react-tasks. Le code métier App.jsx et api/main.py est conservé sans modification. Le fichier package-lock.json est inclus. Le README Vite d’origine est archivé dans docs/archives.

Les exigences Python reprennent les versions installées et vérifiées pendant la séance. Les fichiers .venv et node_modules se réinstallent et ne sont pas publiés. Les paramètres locaux de l’éditeur ne sont pas nécessaires au projet.

## Énoncé

Le PDF de l’enseignant est conservé comme référence pédagogique dans docs/enonce. Aucune licence de redistribution n’est déduite de sa présence. Le dépôt est privé par défaut.

## Captures

Les captures 00 à 12 proviennent des images envoyées par l’utilisateur dans cette séance. Leurs noms descriptifs indiquent leur contenu et les originaux gardent leur nom technique. Les captures 13 à 16 ont ensuite été prises pendant les essais réels du navigateur par Codex. Aucune capture d’un test inexistant n’a été inventée.

## Corrigé et explications

Le PDF explique les étapes, répond aux questions et reproduit le code final. Les fichiers Markdown rendent le parcours consultable directement sur GitHub. L’aide de Copilot et de Codex est mentionnée dans la présentation pour le professeur.

## Schémas et vidéo

Les deux schémas manuscrits ont été générés avec l’outil d’images intégré. Les prompts sont archivés dans docs/flux. Ils décrivent les étapes du projet au moment de leur création. La vidéo a été produite localement comme une animation de schéma, sans voix clonée, sans service payant et sans logo ajouté.

## Reproduction des supports

Le script scripts/generer_supports.py reprend le générateur du PDF et du MP4 avec des chemins relatifs au dépôt. Il nécessite requirements-media.txt et, sous Windows, les polices Arial et Consolas. Les sorties se trouvent dans output/tp-react-corrige. Les sorties déjà validées restent dans docs et media.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-media.txt
.\.venv\Scripts\python.exe scripts/generer_supports.py pdf
.\.venv\Scripts\python.exe scripts/generer_supports.py
```

Le générateur utilise la copie locale des captures. Il ne télécharge rien et n’utilise pas de clé API.

## Intégrité

docs/INVENTAIRE_SHA256.json décrit les fichiers archivés et leurs empreintes. Ce fichier ne s’inclut pas lui-même ; il exclut également les dossiers réinstallables, les journaux et les métadonnées Git. Les fins de ligne CRLF des fichiers texte sont normalisées en LF avant le calcul ; les fichiers binaires sont vérifiés octet par octet. Lancer `python scripts/verifier_archive.py` pour vérifier l’intégrité et les liens locaux.
