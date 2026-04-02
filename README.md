# Projet d'Examen DEVNET - L3 RI

## Pharmacie en Ligne

Application web developpee avec Flask permettant a un client d'envoyer une ordonnance, de verifier la disponibilite des produits et de recevoir une notification. Le projet met en avant la communication entre services via Docker, l'utilisation d'une base PostgreSQL en conteneur et un microservice de notification.

## Problematique resolue

Dans une pharmacie, il est utile de pouvoir :

- recevoir des ordonnances a distance ;
- verifier rapidement si les produits sont disponibles ;
- notifier le client sans intervention manuelle ;
- conserver les demandes dans une base de donnees.

Cette application repond a ce besoin avec une architecture multi-services.

## Architecture

- `app` : application web Flask exposee sur le port `5000`
- `db` : base de donnees PostgreSQL exposee sur le port `5432`
- `notifier` : microservice Flask qui simule l'envoi de SMS ou d'emails sur le port `5001`
- `pharma_net` : reseau Docker dedie a la communication entre services

Flux principal :

1. Le client soumet une ordonnance dans l'application Flask.
2. L'application enregistre la demande dans PostgreSQL.
3. L'application verifie le stock disponible.
4. L'application appelle le microservice `notifier` via HTTP.
5. Le microservice retourne une reponse de confirmation.

## Technologies utilisees

- Python 3.11
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Docker / Docker Compose
- Requests
- Pillow / Tesseract OCR
- GitHub Actions pour la publication Docker Hub

## Fonctionnalites

- formulaire d'envoi d'ordonnance ;
- televersement d'image ou de PDF ;
- OCR sur les images d'ordonnance ;
- verification du stock en base ;
- mise a jour des quantites ;
- enregistrement des prescriptions et notifications ;
- appel HTTP a un microservice de notification ;
- conteneurisation complete du systeme.

## Lancement avec Docker

### Prerequis

- Docker Desktop installe et demarre
- Docker Compose disponible

### Demarrage

```bash
docker compose up --build
```

### Services accessibles

- Application web : [http://localhost:5000](http://localhost:5000)
- Microservice notifier : [http://localhost:5001/health](http://localhost:5001/health)
- Verification sante de l'app : [http://localhost:5000/health](http://localhost:5000/health)

### Arret

```bash
docker compose down
```

Pour supprimer aussi les volumes :

```bash
docker compose down -v
```

## Variables importantes

- `DATABASE_URL` : URL de connexion PostgreSQL
- `NOTIFIER_URL` : URL du microservice de notification
- `SECRET_KEY` : cle secrete Flask

## Base de donnees

La base de donnees utilisee en production Docker est PostgreSQL dans un conteneur dedie. En execution locale simple, l'application peut retomber sur SQLite, mais pour l'examen il faut utiliser le lancement Docker afin de respecter la contrainte "base de donnees en conteneur".

## Aspect reseau

Le projet exploite un reseau Docker nomme `pharma_net`. Les conteneurs communiquent entre eux par nom de service :

- `app` contacte `db` avec l'hote `db`
- `app` contacte `notifier` avec l'URL `http://notifier:5001/notify`

Cela montre la communication entre services distribues sur un reseau interne Docker.

## Docker Hub et CI/CD

Un workflow GitHub Actions est fourni dans `.github/workflows/docker-image.yml` pour construire et publier automatiquement l'image Docker sur Docker Hub a chaque push sur la branche `main`.

Secrets GitHub a configurer :

- `DOCKERHUB_USERNAME` ok
- `DOCKERHUB_TOKEN` ok

Image attendue :

```text
<dockerhub_username>/pharmacie-app:latest
```

## Verification rapide avant soutenance

- `docker compose up --build` demarre sans erreur
- les trois conteneurs sont visibles avec `docker ps`
- le reseau `pharma_net` apparait avec `docker network ls`
- l'application repond sur `http://localhost:5000`
- le notifier repond sur `http://localhost:5001/health`
- une ordonnance ajoute une ligne en base et declenche une notification

## Structure du projet

```text
pharmacie/
|-- app/
|   |-- __init__.py
|   |-- models.py
|   |-- routes.py
|   |-- templates/
|   `-- static/
|-- notifier_service/
|   `-- notify.py
|-- .github/workflows/
|   `-- docker-image.yml
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
`-- run.py
```

## Auteur

- Nom : A completer
- Classe : Licence 3 Reseaux et Informatique (L3 RI)
- Etablissement : ISI Keur Massar
