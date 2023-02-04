## Connection Scan Algorithm Implementation

### Fichiers importants : 

Les fichiers importants se trouvent dans le dossier playground:
  - `run.py` : où est implémenté l'algorithme Connection scan, basé sur l'article "J. Dibbelt, T. Pajor, B. Strasser, and D. Wagner. Connection scan algorithm. ACM Journal of Experimental Algorithmics, 23, 2018"
  - `utils.py` : Fonctions utilitaires pour l'algorithme
  - `landing_page.html` : Pour l'affichage du formulaire
  - `itinierary.html` : Pour l'affichage des itinéraires. Après le calcul des itinéraires, on affiche les 3 chemins calculés et on les classe par durée de trajet.
  - `views.py` : C'est le gestionnaire de requêtes. Le fichier gère les requêtes HTTP et renvoie l'affichage des modèles Django.

### Accès à l'application :
Pour l'instant, en lançant la commande `python manage.py runserver 0.0.0.0:8000`, l'application est accessible sur http://127.0.0.1:8000/playground/test1/

### Dataset  :

Les données utilisées sont au format GTFS d’Île-de-France Mobilité et sont utilisées pour ce projet. Le dataset contient plus de 1 900 lignes de transport, plus de 40 000 arrêts et environ 540 000 circulations sur l’ensemble de l’Île-de-France.

Les données GTFS proviennent de chacun des 75 opérateurs de transport en commun franciliens, qui transmettent à Île-de-France Mobilités les horaires prévus de leurs lignes. La base de données contient les horaires des trains, métros, RER, tramways et bus qui circulent dans la région Île-de-France.

Pour plus de détails, consultez la documentation d'Île-de-France Mobilité : [https://eu.ftp.opendatasoft.com/stif/GTFS/opendata_gtfs.pdf](https://eu.ftp.opendatasoft.com/stif/GTFS/opendata_gtfs.pdf

### Base de données :

Ce projet nécessite de convertir les données GTFS et de les mettre dans une base de données MySQL.

Il faut créer une base de données sur un serveur MySQL et fournir la configuration de celle-ci (port, mot de passe, etc.) à Django en modifiant le fichier `settings.py` qui se trouve dans le dossier `ItinerarySearch`.

Le script qui communique avec le serveur est `playground/request_db.py`.
