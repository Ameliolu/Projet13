# Projet13
Ce projet permet de créer un site web destiné idéalement à une association. Le code de ce projet est entièrement libre de droits. En revanche, les ressources utilisées, notamment celles présente dans les dossiers "static", ont leurs propres régimes de droits.

Ce projet inclut notamment les fonctionalités suivantes :
- affichage des prochains cours et des actualités en fonction des informations en base de données ;
- interface d'administration personnalisé ;
- envoi de courriels depuis l'interface d'administration ;
- inscription depuis le site à la liste de diffusion d'une Newsletter.

Pour utiliser ce site, vous devez suivre les étapes ci-après :
1) Installez les librairies nécessaires :
```
pip install -r requirements.txt
```
2) Procédez aux migrations :
```
python manage.py makemigrations
python manage.py migrate
```
3) Accessoirement, il est conseillé pour vos développements de créer un profil administrateur avec la commande suivante :
```
python manage.py createsuperuser
```
4) Lancez le serveur local avec :
```
python manage.py runserver
```
5) Accédez à la plateforme via http://localhost:8000/
