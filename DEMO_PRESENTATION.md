# Demo et Slides

## Plan de presentation

### Slide 1 - Titre

- Nom du projet : Pharmacie en Ligne
- Nom de l'etudiant
- Classe : L3 RI
- Matiere : DEVNET

### Slide 2 - Probleme resolu

- Les clients ne savent pas toujours si leurs medicaments sont disponibles.
- Les pharmacies perdent du temps a traiter manuellement les demandes.
- Il faut une solution web simple, basee sur une architecture reseau.

### Slide 3 - Architecture du systeme

- Application Flask
- Base PostgreSQL en conteneur
- Microservice de notification
- Reseau Docker `pharma_net`

Schema a presenter :

```text
Client Web --> Flask App --> PostgreSQL
                 |
                 --> Notifier Service
```

### Slide 4 - Aspect reseau

- Communication HTTP entre `app` et `notifier`
- Communication entre `app` et `db` sur le reseau Docker
- Resolution par nom de service Docker : `db`, `notifier`
- Exemple d'API distribuee simple

### Slide 5 - Fonctionnement

- Le client saisit son nom et ses produits
- Il peut joindre une image ou un PDF
- L'application verifie le stock
- Le resultat est affiche
- Une notification est envoyee par microservice

### Slide 6 - Technologies utilisees

- Flask
- PostgreSQL
- Docker
- Docker Compose
- SQLAlchemy
- Requests
- Tesseract OCR
- GitHub Actions / Docker Hub

### Slide 7 - Conclusion

- Projet web fonctionnel
- Conteneurisation complete
- Communication reseau entre services
- Base de donnees en conteneur

## Script de demonstration

### 1. Montrer les fichiers du projet

Montrer :

- `Dockerfile`
- `docker-compose.yml`
- `app/`
- `notifier_service/`
- `.github/workflows/docker-image.yml`

### 2. Lancer le projet

```bash
docker compose up --build
```

### 3. Montrer les conteneurs

```bash
docker ps
```

Tu dois voir :

- `pharma_app`
- `pharma_db`
- `notifier_service`

### 4. Montrer le reseau Docker

```bash
docker network ls
docker network inspect pharma_net
```

Point a expliquer :

- les services sont connectes sur le meme reseau ;
- l'application contacte la base avec `db` ;
- l'application contacte le microservice avec `notifier`.

### 5. Tester les endpoints de sante

Dans le navigateur :

- `http://localhost:5000/health`
- `http://localhost:5001/health`

### 6. Faire une demande d'ordonnance

Depuis l'application :

- saisir un nom ;
- saisir un telephone ou email ;
- mettre par exemple `Paracetamol 500mg, Vitamine C 1g` ;
- valider.

### 7. Montrer la notification

Dans les logs du conteneur `notifier`, montrer que le message a ete recu.

Exemple :

```bash
docker logs notifier_service
```

### 8. Montrer la base de donnees

Option simple :

```bash
docker exec -it pharma_db psql -U pharma -d pharma_db
```

Puis :

```sql
SELECT * FROM product;
SELECT * FROM prescription;
SELECT * FROM notification;
```

### 9. Clore la demo

Rappeler que le projet valide :

- Flask
- base conteneurisee
- Docker
- communication reseau
- microservice

## Checklist finale aujourd'hui

- Completer ton nom dans `README.md`
- Pousser le projet sur GitHub
- Verifier les secrets GitHub Actions
- Verifier que l'image est bien publiee sur Docker Hub
- Faire une capture d'ecran de l'application
- Reviser la demo 2 fois avant la presentation
