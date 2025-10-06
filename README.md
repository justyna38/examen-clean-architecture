# MDM System - Clean Architecture

## Architecture

Système MDM avec 3 modules :
- **PIM** : Gestion produits et typologies
- **DAM** : Gestion médias et associations
- **MDM Core** : Orchestration et règles communes

## Structure

```
exam/
├── pim/               # Module PIM (Product Information Management)
│   ├── entities/      # Product, Typology
│   ├── use_cases/     # CreateProduct, UpdateProduct
│   ├── interfaces/    # IProductRepository, ITypologyRepository
│   └── adapters/      # InMemoryProductRepository
├── dam/               # Module DAM (Digital Asset Management)
│   ├── entities/      # Media, MediaFormat
│   ├── use_cases/     # UploadMedia, AssociateMedia
│   ├── interfaces/    # IMediaRepository, IMediaStorage
│   └── adapters/      # InMemoryMediaRepository
├── mdm_core/          # Module MDM Core (Orchestrateur)
│   ├── orchestrator.py # MDMOrchestrator
│   └── interfaces/    # Interfaces partagées
├── shared/            # Code partagé
│   ├── security/      # Authentification
│   └── tests/         # Tests unitaires
└── main.py           # Application principale
```

## Principes appliqués

- **Clean Architecture** : Séparation en couches
- **SOLID** : DIP, OCP, SRP
- **ADP** : Pas de cycles entre modules
- **Tests** : Mocks pour isolation
- **CI/CD** : Pipeline automatisé

## 🚀 CI/CD Pipeline

Pipeline automatisé avec tests, sécurité, et déploiement automatique via GitHub Actions.

## Déploiement

```bash
# Déploiement local
docker-compose up -d

# Déploiement staging (automatique sur main)
git push origin main

# Déploiement production (via tag)
git tag v1.0.0
git push origin v1.0.0
```

## Tests

```bash
# Tests simples
pytest shared/tests/

# Tests avec couverture
pytest shared/tests/ --cov=pim --cov=dam --cov=mdm_core --cov-report=term-missing

## Réponses à l'examen

Les réponses aux questions des parties 1 et 2 se trouvent dans le fichier `REPONSES_EXAMEN.md`.