# Examen Final - Clean Architecture - Réponses

## Partie 1 - Questions de compréhension (30 points)

### Q1. Rôle de l'architecte (2 pts)

L'architecte logiciel va au-delà du code en prenant des décisions stratégiques qui impactent la maintenabilité :

1. **Choix des patterns d'architecture** : Décider d'utiliser Clean Architecture vs MVC influence la testabilité et l'évolutivité
2. **Découpage en modules** : Séparer les responsabilités métier des détails techniques évite les couplages forts

### Q2. Principes SOLID (10 pts)

**SRP (Single Responsibility Principle)** : Une classe = une responsabilité
- **Violation** : `User` qui gère authentification + envoi email
- **Refactor** : Séparer en `User`, `AuthService`, `EmailService`

**OCP (Open/Closed Principle)** : Ouvert à l'extension, fermé à la modification
- **Violation** : `if/else` pour chaque type de paiement
- **Refactor** : Interface `PaymentProcessor` avec implémentations

**LSP (Liskov Substitution Principle)** : Les sous-classes doivent être substituables
- **Violation** : `Square` hérite de `Rectangle` mais change le comportement
- **Refactor** : Interface commune `Shape`

**ISP (Interface Segregation Principle)** : Pas de dépendance sur interfaces non utilisées
- **Violation** : `Printer` avec `scan()`, `fax()` pour un simple printer
- **Refactor** : Interfaces séparées `IPrinter`, `IScanner`

**DIP (Dependency Inversion Principle)** : Dépendre d'abstractions, pas de détails
- **Violation** : `OrderService` dépend directement de `MySQLDatabase`
- **Refactor** : Dépendre de `IDatabase` interface

### Q3. Principes de composants (6 pts)

**Cohésion :**
- **REP** → regrouper classes utilisées ensemble (ex: User + UserProfile dans même module)
- **CCP** → regrouper classes qui changent ensemble (ex: toutes les classes liées aux paiements)
- **CRP** → éviter de regrouper classes rarement utilisées ensemble (ex: User et Payment dans modules séparés)

**Couplage :**
- **ADP** → éviter cycles entre modules (ex: PIM ne doit pas dépendre de DAM et vice versa)
- **SDP** → éviter dépendances instables (ex: ne pas dépendre d'API externe instable)
- **SAP** → éviter dépendances inutiles (ex: module UI ne doit pas dépendre de base de données)

### Q4. Règles de dépendance (4 pts)

La règle dit que les dépendances pointent vers l'intérieur (vers les entités métier). Les détails (UI, DB, API) dépendent des abstractions (interfaces) définies par les couches internes. Cela permet de changer les détails sans impacter le métier.

### Q5. Tests et Clean Architecture (8 pts)

**Types de tests par couche :**
- Entités : Tests unitaires purs
- Use Cases : Tests unitaires avec mocks des interfaces
- Adaptateurs : Tests d'intégration
- Frameworks : Tests end-to-end

**Limiter les tests fragiles :**
- Mocker les dépendances externes
- Tester le comportement, pas l'implémentation
- Utiliser des interfaces stables

---

## Partie 2 - Étude de cas et conception (30 points)

### C1. Modélisation (10 pts)

**Architecture Clean Architecture MDM :**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PIM Module    │    │  MDM Core       │    │   DAM Module    │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Entities  │ │    │ │  Entities   │ │    │ │   Entities  │ │
│ │ - Product   │ │    │ │ - EAN       │ │    │ │ - Media     │ │
│ │ - Typology  │ │    │ │ - SKU       │ │    │ │ - Format    │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Use Cases   │ │    │ │ Use Cases   │ │    │ │ Use Cases   │ │
│ │ - Create    │ │    │ │ - Link      │ │    │ │ - Upload    │ │
│ │ - Update    │ │    │ │ - Validate  │ │    │ │ - Associate │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Interfaces  │ │    │ │ Interfaces  │ │    │ │ Interfaces  │ │
│ │ - IProduct  │ │    │ │ - IOrchestr │ │    │ │ - IMedia    │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Entités principales :**
- **PIM** : Product, Typology, DynamicField
- **DAM** : Media, MediaFormat, ProductMediaLink
- **MDM Core** : EAN, SKU, ValidationRule

**Flux de données :**
1. Upload média → Parse EAN/SKU → MDM Core → Association automatique

### C2. Justification des choix (10 pts)

**DIP + OCP :**
- Interfaces `IMediaProcessor` pour nouveaux formats
- `ITypologyHandler` pour nouveaux types produits
- Extension sans modification du code existant

**ADP :**
- PIM et DAM ne se connaissent pas directement
- Communication via MDM Core et événements
- Pas de cycles de dépendance

**Tests avec mocks :**
- `IProductRepository` dans DAM
- `ITypologyValidator` dans PIM
- `IMediaStorage` dans use cases

### C3. Découpage en composants (10 pts)

**Modules :**
1. **PIM Module** : Gestion produits + typologies (REP, CCP)
2. **DAM Module** : Gestion médias + associations (REP, CCP)  
3. **MDM Core** : Règles communes + orchestration (CRP, ADP)

**Justification :**
- **REP** : Classes utilisées ensemble dans même module
- **CCP** : Changements liés groupés (ex: tous les types de médias)
- **ADP** : Pas de cycles entre modules
- **SDP** : Dépendances stables via interfaces