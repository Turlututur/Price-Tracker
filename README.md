# Price-Tracker

## Pré-requis :
    Avoir php 7.4.26 d'installé 
    Avoir Composer d'installé (minimum version 2)

Si symfony n'est pas installé dans ce projet (pour x raison):

    $ composer update

Installer le serveur : 

    $ composer require symfony/web-server-bundle 


Attention : à executer si vous souhaitez utiliser votre propre BDD, ne modifiez rien si vous souhaitez utiliser la notre
    Dans le fichier .env il vous faut lier votre BDD (mysql) 

        DATABASE_URL="mysql://user:mdp@127.0.0.1:3306/Front_End?serverVersion=5.7&charset=utf8mb4"


    Il faut maintenant créer les bases et les remplir : 

        $ php bin/console doctrine:database:create
        $ php bin/console doctrine:schema:update --force


### Vous devriez maintenant pouvoir lancer cette application web : 

    $ php bin/console server:run
