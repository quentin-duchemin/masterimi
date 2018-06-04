# Présentation
API REST Django consistuant le Back de l'outil demandé par le département IMI pour aider les élèves à construire correctement leur 3A.

## Installation
```bash
virtualenv venv/
pip install -r requirements.txt
```

## Lancement
```bash
python manage.py runserver
```

Aller sur http://localhost:8000/api/   pour accéder à la racine de l'API.

## Commentaires sur le travail effectué
- La structure de la base de donnée est régie par le fichier model.py qui crée les modèles.
Jusqu'ici, j'ai pu créer les Serializers associés aux modèles permettant un passage des donn�es stockées en mémoire à leur traduction au format JSON et inversement. J'ai créé les vues associées.

- J'ai essayé de traduire correctement dans les serializers les relations entre modèles. C'est ce qui m'a posé un peu de souci avec également la création
et modification du profil utilisateur (d'ailleurs peux-tu me donner ton avis sur cette partie du code ? car je ne suis pas s�r d'avoir eu la bonne vision.)

Après ta validation du code actuel et correction des erreurs/manques qui tu me signaleras, je pense procéder à la gestion de permissions/autorisation sur l'accès
aux différentes vues (j'ai vu comment faire et ça n'a pas l'air difficile).
