# 4A_SQR_CI_CD


 <img src="http://www.u-bourgogne.fr/wp-content/uploads/logo-couleur.jpg" width="50%" height="50%" />


KAMLI Younes et LE THIES Loann - SQR1

# Présentation du projet

L'objectif de ce projet est de créer une API Flask pour de la gestion CRUD d’un système de transaction.
Language utilisé : Python

Choix du sujet : 

Nous avons choisi le sujet guidé : Un chemin tout tracé. Le choix de ce sujet s'est fait rapidement car, après lecture des deux sujets, il nous paraissait trop compliqué de faire le sujet non guidé. 

Technologie utilisé:

Nous avons implémenter notre API à l'aide de WSL (Windows Subsytem for Linux), nous avons aussi utilisé Flask qui est un framework facilitant le développement d'une application web.

Choix de la fonction hachage : 

Après avoir consulté plusieurs sources, il en est ressorti que sha256 est plus utilisé que les autres fonctions de hachage de part sa longueur (plus long hash que certains) et donc plus compliqué à décrypter. Cet aspect n'est pas essentiel dans cet exercice mais sha256 nous paraissait être une solution adéquate et simple d'utilisation.

# Procédure pour exécuter l'API

## Prérequis
### **Lancer WSL (Windows Subsytem for Linux)**
### **Se placer dans le dossier du projet**

## Lancement de l'application
- Installation de flask 
```
pip install flask
```

- Lancer l'application localement sur Linux : 
```
export FLASK_APP=main.py
export FLASK_APP=development
flask run
```

## Test des routes
### Route E1 : Enregistrer une transaction
#### Pour enregistrer une transaction, nous avons besoin :
- De l'id de la personne donnant de l'argent
- De l'id de la personne recevant de l'argent
- Du moment où nous allons enregistrer la transaction
- La somme d'argent que P1 va donner à P2

Tout ceci est mis dans une commande curl
```
curl -X POST -d "personne1=1&personne2=2&temps=10&somme=50" http://localhost:5000/transaction
```

### Route E2 : Afficher une liste de toutes les transactions dans l’ordre chronologique
- Affichage en ligne de commande :
```
curl -X GET http://localhost:5000/transaction
```
- Affichage sur la page :

``` localhost:5000/transaction ```

### Route E3 :  Afficher une liste des transactions dans l’ordre chronologique liées à une personne
- Affichage en ligne de commande :

  Exemple pour récupérer la liste de P1
```
curl -X GET http://localhost:5000/personne?personne=1
```
- Affichage sur la page :

 ``` localhost:5000/personne?personne=1 ```

### Route E4 : Afficher le solde du compte de la personne
- Affichage en ligne de commande :

  Exemple pour récupérer le solde de P2
```
curl -X GET http://localhost:5000/solde?personne=2
```
- Affichage sur la page :

``` localhost:5000/solde?personne=2 ```
  
### Route E5 : Importer des données depuis un fichier csv
  - Utilisation de la route en ligne de commande :
```
curl -X POST -F 'file=@transaction.csv' http://localhost:5000/csv
```
  On peut vérifier l'ajout des transactions sur :
  
``` localhost:5000/csv ```
  
# Résultats des derniers builds

![Docker push GCR](https://github.com/youneskamli/4A_SQR_CI_CD/actions/workflows/Docker_push_GCR.yml/badge.svg)

![newImage](https://github.com/youneskamli/4A_SQR_CI_CD/actions/workflows/newImage.yml/badge.svg)

![newPush](https://github.com/youneskamli/4A_SQR_CI_CD/actions/workflows/newPush.yml/badge.svg)
